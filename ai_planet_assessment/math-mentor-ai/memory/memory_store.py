"""
Memory Store for Math Mentor AI

This module implements the self-learning memory system using SQLite.
It stores solved problems, user feedback, and enables pattern reuse.
"""

import sqlite3
import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np

# Lazy import for sentence transformers
_embedding_model = None


def get_embedding_model():
    """Lazy load the embedding model for similarity search."""
    global _embedding_model
    if _embedding_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            print("Loading embedding model for memory store...")
            _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except ImportError:
            print("Warning: sentence-transformers not installed. Similarity search disabled.")
            return None
    return _embedding_model


class MemoryStore:
    """
    Memory Store: Self-learning system with SQLite.
    
    Stores solved problems with embeddings for similarity search.
    Enables pattern reuse and learning from user feedback.
    """
    
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS solved_problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        input_type TEXT NOT NULL,
        original_input TEXT,
        parsed_problem TEXT,
        topic TEXT,
        retrieved_chunks TEXT,
        final_answer TEXT,
        reasoning_steps TEXT,
        verifier_confidence REAL,
        user_feedback TEXT,
        user_correction TEXT,
        embedding BLOB
    );
    
    CREATE INDEX IF NOT EXISTS idx_topic ON solved_problems(topic);
    CREATE INDEX IF NOT EXISTS idx_timestamp ON solved_problems(timestamp);
    CREATE INDEX IF NOT EXISTS idx_feedback ON solved_problems(user_feedback);
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the Memory Store.
        
        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            project_root = Path(__file__).parent.parent
            db_path = project_root / "data" / "memory_store.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._embedding_model = None
        
        # Initialize database
        self._init_db()
    
    @property
    def embedding_model(self):
        """Lazy-load embedding model."""
        if self._embedding_model is None:
            self._embedding_model = get_embedding_model()
        return self._embedding_model
    
    def _init_db(self):
        """Initialize the database schema."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.executescript(self.SCHEMA)
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        return sqlite3.connect(str(self.db_path))
    
    def _generate_embedding(self, text: str) -> Optional[bytes]:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Pickled embedding bytes, or None if model unavailable
        """
        if self.embedding_model is None:
            return None
        
        try:
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            return pickle.dumps(embedding)
        except Exception as e:
            print(f"Embedding generation failed: {e}")
            return None
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def store_problem(
        self,
        input_type: str,
        original_input: str,
        parsed_problem: Dict,
        topic: str,
        retrieved_chunks: List[str],
        final_answer: str,
        reasoning_steps: List[str],
        verifier_confidence: float
    ) -> int:
        """
        Store a solved problem.
        
        Args:
            input_type: "ocr" | "asr" | "text"
            original_input: Raw input text
            parsed_problem: Parsed problem dictionary
            topic: Problem topic
            retrieved_chunks: RAG chunks used
            final_answer: The solution
            reasoning_steps: List of steps
            verifier_confidence: Confidence score
            
        Returns:
            ID of stored problem
        """
        timestamp = datetime.now().isoformat()
        
        # Generate embedding from parsed problem text
        problem_text = parsed_problem.get("problem_text", original_input)
        embedding = self._generate_embedding(problem_text)
        
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO solved_problems (
                    timestamp, input_type, original_input, parsed_problem,
                    topic, retrieved_chunks, final_answer, reasoning_steps,
                    verifier_confidence, embedding
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    timestamp,
                    input_type,
                    original_input,
                    json.dumps(parsed_problem),
                    topic,
                    json.dumps(retrieved_chunks),
                    final_answer,
                    json.dumps(reasoning_steps),
                    verifier_confidence,
                    embedding
                )
            )
            return cursor.lastrowid
    
    def update_feedback(
        self,
        problem_id: int,
        feedback: str,
        correction: str = None
    ) -> bool:
        """
        Update user feedback for a problem.
        
        Args:
            problem_id: ID of the problem
            feedback: "correct" | "incorrect"
            correction: User's correction if incorrect
            
        Returns:
            True if updated successfully
        """
        with self._get_connection() as conn:
            conn.execute(
                """
                UPDATE solved_problems
                SET user_feedback = ?, user_correction = ?
                WHERE id = ?
                """,
                (feedback, correction, problem_id)
            )
            return conn.total_changes > 0
    
    def find_similar(
        self,
        problem_text: str,
        topic: str = None,
        threshold: float = 0.85,
        limit: int = 5
    ) -> List[Dict]:
        """
        Find similar past problems using embedding similarity.
        
        Args:
            problem_text: Problem to find similar ones for
            topic: Optional topic filter
            threshold: Minimum similarity threshold
            limit: Maximum results to return
            
        Returns:
            List of similar problem dictionaries
        """
        if self.embedding_model is None:
            return []
        
        # Generate query embedding
        try:
            query_embedding = self.embedding_model.encode(problem_text, convert_to_numpy=True)
        except Exception:
            return []
        
        # Fetch problems with embeddings
        with self._get_connection() as conn:
            if topic:
                cursor = conn.execute(
                    """
                    SELECT id, parsed_problem, final_answer, reasoning_steps,
                           verifier_confidence, user_feedback, embedding
                    FROM solved_problems
                    WHERE topic = ? AND embedding IS NOT NULL
                    ORDER BY timestamp DESC
                    LIMIT 100
                    """,
                    (topic,)
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT id, parsed_problem, final_answer, reasoning_steps,
                           verifier_confidence, user_feedback, embedding
                    FROM solved_problems
                    WHERE embedding IS NOT NULL
                    ORDER BY timestamp DESC
                    LIMIT 100
                    """
                )
            
            results = []
            for row in cursor:
                try:
                    stored_embedding = pickle.loads(row[6])
                    similarity = self._cosine_similarity(query_embedding, stored_embedding)
                    
                    if similarity >= threshold:
                        results.append({
                            "id": row[0],
                            "parsed_problem": json.loads(row[1]) if row[1] else {},
                            "final_answer": row[2],
                            "reasoning_steps": json.loads(row[3]) if row[3] else [],
                            "verifier_confidence": row[4],
                            "user_feedback": row[5],
                            "similarity": similarity
                        })
                except Exception:
                    continue
            
            # Sort by similarity and limit
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:limit]
    
    def get_corrections(self, topic: str = None, limit: int = 10) -> List[Dict]:
        """
        Get user corrections for learning.
        
        Args:
            topic: Optional topic filter
            limit: Maximum results
            
        Returns:
            List of correction dictionaries
        """
        with self._get_connection() as conn:
            if topic:
                cursor = conn.execute(
                    """
                    SELECT parsed_problem, final_answer, user_correction
                    FROM solved_problems
                    WHERE user_feedback = 'incorrect' AND user_correction IS NOT NULL
                          AND topic = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (topic, limit)
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT parsed_problem, final_answer, user_correction
                    FROM solved_problems
                    WHERE user_feedback = 'incorrect' AND user_correction IS NOT NULL
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (limit,)
                )
            
            return [
                {
                    "parsed_problem": json.loads(row[0]) if row[0] else {},
                    "wrong_answer": row[1],
                    "correct_answer": row[2]
                }
                for row in cursor
            ]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics for UI display.
        
        Returns:
            Statistics dictionary
        """
        with self._get_connection() as conn:
            # Total problems
            total = conn.execute(
                "SELECT COUNT(*) FROM solved_problems"
            ).fetchone()[0]
            
            # By topic
            topics = conn.execute(
                """
                SELECT topic, COUNT(*) as count
                FROM solved_problems
                GROUP BY topic
                ORDER BY count DESC
                """
            ).fetchall()
            
            # Feedback stats
            feedback = conn.execute(
                """
                SELECT user_feedback, COUNT(*) as count
                FROM solved_problems
                WHERE user_feedback IS NOT NULL
                GROUP BY user_feedback
                """
            ).fetchall()
            
            # Average confidence
            avg_confidence = conn.execute(
                "SELECT AVG(verifier_confidence) FROM solved_problems"
            ).fetchone()[0]
            
            return {
                "total_problems": total,
                "by_topic": {row[0]: row[1] for row in topics},
                "feedback": {row[0]: row[1] for row in feedback},
                "average_confidence": avg_confidence or 0.0
            }
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """
        Get recent solved problems.
        
        Args:
            limit: Number of problems to return
            
        Returns:
            List of problem dictionaries
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, timestamp, topic, parsed_problem, final_answer,
                       verifier_confidence, user_feedback
                FROM solved_problems
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,)
            )
            
            return [
                {
                    "id": row[0],
                    "timestamp": row[1],
                    "topic": row[2],
                    "parsed_problem": json.loads(row[3]) if row[3] else {},
                    "final_answer": row[4],
                    "confidence": row[5],
                    "feedback": row[6]
                }
                for row in cursor
            ]


# Singleton instance
_memory_instance = None

def get_memory_store() -> MemoryStore:
    """Get or create singleton memory store."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = MemoryStore()
    return _memory_instance


def main():
    """Test the Memory Store."""
    print("=" * 60)
    print("Math Mentor AI - Memory Store Test")
    print("=" * 60)
    
    store = MemoryStore()
    
    # Test storing a problem
    problem_id = store.store_problem(
        input_type="text",
        original_input="Solve x^2 - 5x + 6 = 0",
        parsed_problem={
            "problem_text": "Solve x² - 5x + 6 = 0",
            "topic": "algebra",
            "variables": ["x"]
        },
        topic="algebra",
        retrieved_chunks=["algebra > Quadratic Equations"],
        final_answer="x = 2 or x = 3",
        reasoning_steps=[
            "Factor: (x-2)(x-3) = 0",
            "Therefore x = 2 or x = 3"
        ],
        verifier_confidence=0.92
    )
    print(f"\nStored problem with ID: {problem_id}")
    
    # Test feedback
    store.update_feedback(problem_id, "correct")
    print("Updated feedback to 'correct'")
    
    # Test stats
    stats = store.get_stats()
    print(f"\nMemory Stats:")
    print(f"  Total problems: {stats['total_problems']}")
    print(f"  By topic: {stats['by_topic']}")
    print(f"  Average confidence: {stats['average_confidence']:.2f}")
    
    # Test similarity search
    similar = store.find_similar("Solve x^2 - 4 = 0", topic="algebra")
    print(f"\nSimilar problems found: {len(similar)}")
    for s in similar:
        print(f"  - {s['final_answer']} (similarity: {s['similarity']:.2f})")


if __name__ == "__main__":
    main()
