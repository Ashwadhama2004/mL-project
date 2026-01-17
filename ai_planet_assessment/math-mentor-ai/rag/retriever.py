"""
RAG Retriever for Math Mentor AI

This module provides the retrieval interface for querying the FAISS index
and returning relevant knowledge chunks for problem-solving.
"""

import os
import json
import pickle
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    import faiss
except ImportError:
    print("Please install required packages: pip install sentence-transformers faiss-cpu")
    raise


class RAGRetriever:
    """Retrieves relevant knowledge chunks from the FAISS index."""
    
    def __init__(
        self,
        index_dir: str = None,
        model_name: str = "all-MiniLM-L6-v2",
        relevance_threshold: float = 0.5
    ):
        """
        Initialize the retriever.
        
        Args:
            index_dir: Path to the FAISS index directory
            model_name: Sentence transformer model (must match indexer)
            relevance_threshold: Minimum relevance score for results
        """
        # Get the project root directory
        self.project_root = Path(__file__).parent.parent
        
        self.index_dir = Path(index_dir) if index_dir else \
            self.project_root / "data" / "faiss_index"
        
        self.model_name = model_name
        self.relevance_threshold = relevance_threshold
        
        # Load components
        self._load_model()
        self._load_index()
        self._load_metadata()
        self._load_chunks()
    
    def _load_model(self) -> None:
        """Load the embedding model."""
        print(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
    
    def _load_index(self) -> None:
        """Load the FAISS index from disk."""
        index_path = self.index_dir / "index.faiss"
        
        if not index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found at {index_path}. "
                "Please run 'python -m rag.build_index' first."
            )
        
        self.index = faiss.read_index(str(index_path))
        print(f"Loaded FAISS index with {self.index.ntotal} vectors")
    
    def _load_metadata(self) -> None:
        """Load chunk metadata from disk."""
        metadata_path = self.index_dir / "metadata.json"
        
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found at {metadata_path}")
        
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
    
    def _load_chunks(self) -> None:
        """Load original chunks from disk."""
        chunks_path = self.index_dir / "chunks.pkl"
        
        if not chunks_path.exists():
            raise FileNotFoundError(f"Chunks not found at {chunks_path}")
        
        with open(chunks_path, "rb") as f:
            self.chunks = pickle.load(f)
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[List[str]] = None
    ) -> Dict:
        """
        Retrieve relevant knowledge chunks for a query.
        
        Args:
            query: The query text (problem description)
            top_k: Number of top results to return
            filters: Optional list of topic keywords to filter results
            
        Returns:
            Dictionary with retrieved chunks and metadata
        """
        # Generate query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        # Search the index (get more results if filtering)
        search_k = top_k * 3 if filters else top_k
        distances, indices = self.index.search(
            query_embedding.astype(np.float32),
            min(search_k, self.index.ntotal)
        )
        
        # Process results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx == -1:  # FAISS returns -1 for invalid results
                continue
            
            # Convert inner product to similarity score (already normalized, so this is cosine sim)
            relevance_score = float(distance)
            
            # Skip low relevance results
            if relevance_score < self.relevance_threshold:
                continue
            
            chunk_text = self.chunks[idx]
            chunk_metadata = self.metadata[idx]
            
            # Apply topic filters if provided
            if filters:
                # Check if any filter keyword appears in source or section
                source_section = f"{chunk_metadata['source']} {chunk_metadata['section']}".lower()
                if not any(f.lower() in source_section for f in filters):
                    continue
            
            results.append({
                "text": chunk_text,
                "source": chunk_metadata["source"],
                "section": chunk_metadata["section"],
                "subsection": chunk_metadata.get("subsection", ""),
                "relevance_score": relevance_score,
                "rank": len(results) + 1
            })
            
            if len(results) >= top_k:
                break
        
        return {
            "query": query,
            "filters": filters,
            "num_results": len(results),
            "chunks": results
        }
    
    def retrieve_with_context(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[List[str]] = None
    ) -> str:
        """
        Retrieve and format chunks as context for the LLM.
        
        Args:
            query: The query text
            top_k: Number of chunks to retrieve
            filters: Optional topic filters
            
        Returns:
            Formatted context string with citations
        """
        results = self.retrieve(query, top_k, filters)
        
        if not results["chunks"]:
            return "No relevant knowledge found in the knowledge base."
        
        context_parts = []
        for chunk in results["chunks"]:
            citation = f"[{chunk['source']}"
            if chunk["section"]:
                citation += f" > {chunk['section']}"
            if chunk["subsection"]:
                citation += f" > {chunk['subsection']}"
            citation += f"] (relevance: {chunk['relevance_score']:.2f})"
            
            context_parts.append(f"{citation}\n{chunk['text']}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def get_sources_summary(self, results: Dict) -> List[str]:
        """
        Get a summary of sources used.
        
        Args:
            results: Results from retrieve()
            
        Returns:
            List of source citations
        """
        sources = []
        for chunk in results["chunks"]:
            source = chunk["source"]
            if chunk["section"]:
                source += f" > {chunk['section']}"
            if chunk["subsection"]:
                source += f" > {chunk['subsection']}"
            sources.append(source)
        return sources
    
    def is_index_available(self) -> bool:
        """Check if the index is available and loaded."""
        return hasattr(self, 'index') and self.index is not None


# Singleton instance for the application
_retriever_instance = None

def get_retriever() -> RAGRetriever:
    """Get or create the singleton retriever instance."""
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = RAGRetriever()
    return _retriever_instance


def main():
    """Test the retriever with sample queries."""
    print("=" * 60)
    print("Math Mentor AI - RAG Retriever Test")
    print("=" * 60)
    
    retriever = RAGRetriever()
    
    # Test queries
    test_queries = [
        ("Find the roots of x^2 - 5x + 6 = 0", ["algebra"]),
        ("What is the derivative of sin(x)?", ["calculus"]),
        ("Calculate probability of getting at least one head in 3 coin tosses", ["probability"]),
        ("Find the area between y=x^2 and y=x", None),
    ]
    
    for query, filters in test_queries:
        print(f"\nQuery: {query}")
        print(f"Filters: {filters}")
        print("-" * 40)
        
        results = retriever.retrieve(query, top_k=3, filters=filters)
        
        for chunk in results["chunks"]:
            print(f"[{chunk['source']} > {chunk['section']}] "
                  f"(score: {chunk['relevance_score']:.3f})")
            print(f"  {chunk['text'][:150]}...")
            print()


if __name__ == "__main__":
    main()
