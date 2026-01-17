"""
RAG Index Builder for Math Mentor AI

This module handles the creation of the FAISS vector index from the knowledge base.
It loads markdown files, chunks them into semantic sections, generates embeddings,
and saves the index for retrieval.
"""

import os
import json
import pickle
import re
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    import faiss
except ImportError:
    print("Please install required packages: pip install sentence-transformers faiss-cpu")
    raise


class KnowledgeBaseIndexer:
    """Builds and manages the FAISS index for the knowledge base."""
    
    def __init__(
        self,
        knowledge_base_dir: str = None,
        index_dir: str = None,
        model_name: str = "all-MiniLM-L6-v2",
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        """
        Initialize the indexer.
        
        Args:
            knowledge_base_dir: Path to directory containing markdown files
            index_dir: Path to save the FAISS index
            model_name: Sentence transformer model for embeddings
            chunk_size: Target characters per chunk
            chunk_overlap: Overlap between chunks
        """
        # Get the project root directory
        self.project_root = Path(__file__).parent.parent
        
        self.knowledge_base_dir = Path(knowledge_base_dir) if knowledge_base_dir else \
            self.project_root / "rag" / "knowledge_base"
        self.index_dir = Path(index_dir) if index_dir else \
            self.project_root / "data" / "faiss_index"
        
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Load the embedding model
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        # Storage for chunks and metadata
        self.chunks: List[str] = []
        self.metadata: List[Dict] = []
        
    def load_markdown_files(self) -> List[Tuple[str, str]]:
        """
        Load all markdown files from the knowledge base directory.
        
        Returns:
            List of (filename, content) tuples
        """
        documents = []
        
        if not self.knowledge_base_dir.exists():
            raise FileNotFoundError(f"Knowledge base directory not found: {self.knowledge_base_dir}")
        
        md_files = list(self.knowledge_base_dir.glob("*.md"))
        print(f"Found {len(md_files)} markdown files")
        
        for file_path in md_files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            documents.append((file_path.stem, content))
            print(f"  Loaded: {file_path.name} ({len(content)} chars)")
        
        return documents
    
    def extract_sections(self, content: str, filename: str) -> List[Dict]:
        """
        Extract sections from markdown content based on headers.
        
        Args:
            content: Markdown content
            filename: Source filename for metadata
            
        Returns:
            List of section dictionaries with text and metadata
        """
        sections = []
        
        # Split by headers (##, ###)
        # Pattern matches headers and captures the header text
        header_pattern = r'^(#{2,4})\s+(.+)$'
        
        lines = content.split('\n')
        current_section = {
            "text": "",
            "source": filename,
            "section": "Introduction",
            "subsection": ""
        }
        
        for line in lines:
            header_match = re.match(header_pattern, line)
            
            if header_match:
                # Save current section if it has content
                if current_section["text"].strip():
                    sections.append(current_section.copy())
                
                header_level = len(header_match.group(1))
                header_text = header_match.group(2).strip()
                
                if header_level == 2:
                    current_section = {
                        "text": "",
                        "source": filename,
                        "section": header_text,
                        "subsection": ""
                    }
                else:
                    current_section = {
                        "text": "",
                        "source": filename,
                        "section": current_section["section"],
                        "subsection": header_text
                    }
            else:
                current_section["text"] += line + "\n"
        
        # Don't forget the last section
        if current_section["text"].strip():
            sections.append(current_section)
        
        return sections
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Split text into chunks of appropriate size.
        
        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of chunk dictionaries
        """
        chunks = []
        
        # Clean the text
        text = text.strip()
        if not text:
            return chunks
        
        # If text is small enough, keep as single chunk
        if len(text) <= self.chunk_size:
            chunks.append({
                "text": text,
                **metadata
            })
            return chunks
        
        # Split into paragraphs first (preserve semantic units)
        paragraphs = re.split(r'\n\n+', text)
        
        current_chunk = ""
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # If adding this paragraph exceeds limit, save current and start new
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    **metadata
                })
                # Start new chunk with overlap from end of previous
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                current_chunk = overlap_text + para
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                **metadata
            })
        
        return chunks
    
    def process_documents(self, documents: List[Tuple[str, str]]) -> None:
        """
        Process all documents into chunks with metadata.
        
        Args:
            documents: List of (filename, content) tuples
        """
        self.chunks = []
        self.metadata = []
        
        for filename, content in documents:
            # Extract sections
            sections = self.extract_sections(content, filename)
            
            # Chunk each section
            for section in sections:
                section_text = section.pop("text")
                section_chunks = self.chunk_text(section_text, section)
                
                for chunk in section_chunks:
                    self.chunks.append(chunk["text"])
                    self.metadata.append({
                        "source": chunk["source"],
                        "section": chunk["section"],
                        "subsection": chunk.get("subsection", ""),
                        "text": chunk["text"][:200] + "..."  # Preview
                    })
        
        print(f"Created {len(self.chunks)} chunks from {len(documents)} documents")
    
    def build_index(self) -> faiss.Index:
        """
        Build FAISS index from chunks.
        
        Returns:
            FAISS index
        """
        if not self.chunks:
            raise ValueError("No chunks to index. Run process_documents first.")
        
        print(f"Generating embeddings for {len(self.chunks)} chunks...")
        embeddings = self.model.encode(
            self.chunks,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
        index.add(embeddings.astype(np.float32))
        
        print(f"Built FAISS index with {index.ntotal} vectors")
        return index
    
    def save_index(self, index: faiss.Index) -> None:
        """
        Save the FAISS index and metadata to disk.
        
        Args:
            index: FAISS index to save
        """
        # Create directory if it doesn't exist
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_path = self.index_dir / "index.faiss"
        faiss.write_index(index, str(index_path))
        print(f"Saved FAISS index to {index_path}")
        
        # Save metadata
        metadata_path = self.index_dir / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        print(f"Saved metadata to {metadata_path}")
        
        # Save chunks for retrieval
        chunks_path = self.index_dir / "chunks.pkl"
        with open(chunks_path, "wb") as f:
            pickle.dump(self.chunks, f)
        print(f"Saved chunks to {chunks_path}")
    
    def build_and_save(self) -> None:
        """Complete pipeline: load, process, build, and save."""
        print("=" * 60)
        print("Math Mentor AI - Knowledge Base Indexer")
        print("=" * 60)
        
        # Load documents
        documents = self.load_markdown_files()
        
        # Process into chunks
        self.process_documents(documents)
        
        # Build index
        index = self.build_index()
        
        # Save everything
        self.save_index(index)
        
        print("=" * 60)
        print("Index building complete!")
        print(f"Total chunks indexed: {len(self.chunks)}")
        print(f"Index saved to: {self.index_dir}")
        print("=" * 60)


def main():
    """Main entry point for building the index."""
    indexer = KnowledgeBaseIndexer()
    indexer.build_and_save()


if __name__ == "__main__":
    main()
