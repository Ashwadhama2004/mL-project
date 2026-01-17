"""
Test Runner for Math Mentor AI

Run basic tests to verify the system is working correctly.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_environment():
    """Test that required packages are installed."""
    print("\n" + "=" * 60)
    print("Testing Environment")
    print("=" * 60)
    
    packages = [
        ("streamlit", "Streamlit"),
        ("google.generativeai", "Google Generative AI"),
        ("sentence_transformers", "Sentence Transformers"),
        ("faiss", "FAISS"),
        ("PIL", "Pillow"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_ok = True
    for module, name in packages:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            all_ok = False
    
    # Optional packages
    print("\nOptional packages:")
    optional = [
        ("easyocr", "EasyOCR"),
        ("whisper", "OpenAI Whisper"),
    ]
    for module, name in optional:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ⚠ {name} - not installed (optional)")
    
    return all_ok


def test_llm_client():
    """Test LLM client connection."""
    print("\n" + "=" * 60)
    print("Testing LLM Client")
    print("=" * 60)
    
    try:
        from utils.llm_client import LLMClient
        client = LLMClient()
        
        response = client.generate("What is 2 + 2? Answer with just the number.")
        print(f"  ✓ LLM connected successfully")
        print(f"  Response: {response.strip()}")
        return True
    except Exception as e:
        print(f"  ✗ LLM connection failed: {str(e)}")
        return False


def test_text_processor():
    """Test text input processor."""
    print("\n" + "=" * 60)
    print("Testing Text Processor")
    print("=" * 60)
    
    try:
        from input_processors.text import TextProcessor
        processor = TextProcessor()
        
        result = processor.process("Solve x^2 - 5x + 6 = 0")
        print(f"  ✓ Text processor working")
        print(f"  Input: 'Solve x^2 - 5x + 6 = 0'")
        print(f"  Clean: '{result.get('clean_text')}'")
        print(f"  Confidence: {result.get('confidence')}")
        return True
    except Exception as e:
        print(f"  ✗ Text processor failed: {str(e)}")
        return False


def test_calculator():
    """Test calculator tool."""
    print("\n" + "=" * 60)
    print("Testing Calculator Tool")
    print("=" * 60)
    
    try:
        from utils.tools import PythonCalculator
        calc = PythonCalculator()
        
        tests = [
            ("2 + 2", "4"),
            ("sqrt(16)", "4"),
            ("sin(0)", "0"),
            ("factorial(5)", "120"),
        ]
        
        all_ok = True
        for expr, expected in tests:
            result = calc.calculate(expr)
            if result["success"]:
                print(f"  ✓ {expr} = {result['formatted_result']}")
            else:
                print(f"  ✗ {expr} failed: {result['error']}")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"  ✗ Calculator failed: {str(e)}")
        return False


def test_memory_store():
    """Test memory store."""
    print("\n" + "=" * 60)
    print("Testing Memory Store")
    print("=" * 60)
    
    try:
        from memory.memory_store import MemoryStore
        
        # Use a test database
        test_db = project_root / "data" / "test_memory.db"
        store = MemoryStore(db_path=str(test_db))
        
        # Test storing
        problem_id = store.store_problem(
            input_type="text",
            original_input="Test problem",
            parsed_problem={"problem_text": "Test", "topic": "test"},
            topic="test",
            retrieved_chunks=[],
            final_answer="Test answer",
            reasoning_steps=["Step 1"],
            verifier_confidence=0.9
        )
        print(f"  ✓ Stored problem with ID: {problem_id}")
        
        # Test stats
        stats = store.get_stats()
        print(f"  ✓ Stats: {stats['total_problems']} problems in store")
        
        # Clean up test database
        if test_db.exists():
            os.remove(test_db)
        
        return True
    except Exception as e:
        print(f"  ✗ Memory store failed: {str(e)}")
        return False


def test_rag_index():
    """Test RAG index (if built)."""
    print("\n" + "=" * 60)
    print("Testing RAG Index")
    print("=" * 60)
    
    index_path = project_root / "data" / "faiss_index" / "index.faiss"
    
    if not index_path.exists():
        print("  ⚠ FAISS index not found")
        print("  Run: python -m rag.build_index")
        return False
    
    try:
        from rag.retriever import RAGRetriever
        retriever = RAGRetriever()
        
        result = retriever.retrieve("quadratic equation", top_k=3)
        print(f"  ✓ RAG retriever working")
        print(f"  Found {result['num_results']} chunks for 'quadratic equation'")
        
        if result["chunks"]:
            for chunk in result["chunks"][:2]:
                print(f"    - {chunk['source']} > {chunk['section']} ({chunk['relevance_score']:.2f})")
        
        return True
    except Exception as e:
        print(f"  ✗ RAG retriever failed: {str(e)}")
        return False


def test_parser_agent():
    """Test parser agent."""
    print("\n" + "=" * 60)
    print("Testing Parser Agent")
    print("=" * 60)
    
    try:
        from agents.parser_agent import ParserAgent
        parser = ParserAgent()
        
        result = parser.parse({
            "raw_text": "Solve x^2 - 5x + 6 = 0",
            "source": "text"
        })
        
        print(f"  ✓ Parser agent working")
        print(f"  Topic: {result.get('topic')}")
        print(f"  Variables: {result.get('variables')}")
        print(f"  Confidence: {result.get('confidence', 0):.2f}")
        
        return True
    except Exception as e:
        print(f"  ✗ Parser agent failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Math Mentor AI - System Tests")
    print("=" * 60)
    
    results = {}
    
    # Run tests
    results["Environment"] = test_environment()
    results["Text Processor"] = test_text_processor()
    results["Calculator"] = test_calculator()
    results["Memory Store"] = test_memory_store()
    results["RAG Index"] = test_rag_index()
    
    # LLM and Agent tests (may take longer)
    print("\n" + "-" * 60)
    print("Running LLM and Agent tests (may take a moment)...")
    print("-" * 60)
    
    results["LLM Client"] = test_llm_client()
    
    if results["LLM Client"]:
        results["Parser Agent"] = test_parser_agent()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready to use.")
        print("Run: streamlit run app.py")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
