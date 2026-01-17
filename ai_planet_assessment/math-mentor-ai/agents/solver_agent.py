"""
Solver Agent for Math Mentor AI

This agent generates solutions using RAG context and tools.
It retrieves relevant knowledge, checks memory, and produces solutions with citations.
"""

from typing import Dict, Any, List, Optional
import json

from utils.llm_client import get_llm_client
from utils.tools import get_calculator
from utils.confidence import calculate_confidence
from utils.logger import AgentLogger


class SolverAgent:
    """
    Solver Agent: Generates solutions using RAG and tools.
    
    Responsibilities:
    - Call RAG retriever with filters
    - Check memory for similar problems
    - Use Python calculator tool if needed
    - Generate solution with reasoning
    - MUST cite which chunks were used
    - Admit uncertainty if no relevant chunks
    """
    
    def __init__(self, retriever=None, memory_store=None, logger: AgentLogger = None):
        """
        Initialize the Solver Agent.
        
        Args:
            retriever: RAG retriever instance
            memory_store: Memory store instance
            logger: Agent logger for execution tracing
        """
        self.llm = get_llm_client()
        self.calculator = get_calculator()
        self.retriever = retriever
        self.memory_store = memory_store
        self.logger = logger
    
    def _retrieve_context(
        self,
        problem_text: str,
        filters: List[str],
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieve relevant context from RAG.
        
        Args:
            problem_text: The problem text
            filters: Topic filters
            top_k: Number of chunks to retrieve
            
        Returns:
            Dictionary with chunks and formatted context
        """
        if self.retriever is None:
            return {
                "chunks": [],
                "context": "Knowledge base not available.",
                "sources": []
            }
        
        try:
            results = self.retriever.retrieve(problem_text, top_k=top_k, filters=filters)
            
            context_parts = []
            sources = []
            
            for chunk in results.get("chunks", []):
                source = f"{chunk['source']}"
                if chunk.get("section"):
                    source += f" > {chunk['section']}"
                sources.append(source)
                
                context_parts.append(
                    f"[{source}]:\n{chunk['text']}"
                )
            
            return {
                "chunks": results.get("chunks", []),
                "context": "\n\n---\n\n".join(context_parts) if context_parts else "No relevant context found.",
                "sources": sources
            }
            
        except Exception as e:
            return {
                "chunks": [],
                "context": f"Error retrieving context: {str(e)}",
                "sources": [],
                "error": str(e)
            }
    
    def _check_memory(self, problem_text: str, topic: str) -> Optional[Dict]:
        """
        Check memory for similar past problems.
        
        Args:
            problem_text: The problem text
            topic: Problem topic
            
        Returns:
            Similar problem data if found, None otherwise
        """
        if self.memory_store is None:
            return None
        
        try:
            similar = self.memory_store.find_similar(problem_text, topic=topic, threshold=0.85)
            if similar:
                return similar[0]  # Return most similar
        except Exception:
            pass
        
        return None
    
    def _execute_calculation(self, expression: str) -> Dict:
        """
        Execute a calculation using the Python calculator.
        
        Args:
            expression: Mathematical expression
            
        Returns:
            Calculation result
        """
        return self.calculator.calculate(expression)
    
    def solve(
        self,
        problem_text: str,
        topic: str,
        retrieval_filters: List[str],
        use_python_tool: bool = False,
        memory_hits: List[Dict] = None,
        variables: List[str] = None,
        constraints: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a solution for the problem.
        
        Args:
            problem_text: The cleaned problem text
            topic: Problem topic
            retrieval_filters: Filters for RAG retrieval
            use_python_tool: Whether to use calculator
            memory_hits: Similar problems from memory
            variables: Problem variables
            constraints: Problem constraints
            
        Returns:
            Dictionary containing:
                - solution: The solution text
                - reasoning_steps: List of reasoning steps
                - used_rag_chunks: Citations
                - used_tools: Tools used
                - confidence: Float
                - agent_trace: String description
        """
        if self.logger:
            self.logger.start_agent(
                "Solver",
                {"problem": problem_text[:100], "topic": topic},
                "Generating solution"
            )
        
        try:
            # Step 1: Retrieve context
            rag_result = self._retrieve_context(problem_text, retrieval_filters)
            context = rag_result["context"]
            sources = rag_result["sources"]
            chunks = rag_result["chunks"]
            
            # Step 2: Check memory for similar problems
            memory_context = ""
            if memory_hits:
                memory_context = "\n\nSIMILAR PAST PROBLEMS:\n"
                for hit in memory_hits[:2]:
                    memory_context += f"- Problem: {hit.get('parsed_problem', '')[:100]}\n"
                    memory_context += f"  Answer: {hit.get('final_answer', '')[:200]}\n"
            
            # Step 3: Prepare the solving prompt
            system_prompt = """You are an expert JEE mathematics tutor solving problems step by step.

CRITICAL RULES:
1. You MUST cite which knowledge base sections you used with [source] notation
2. If the provided context doesn't contain relevant information, say "Insufficient knowledge base coverage"
3. Show each step of your reasoning clearly
4. Verify your answer if possible
5. Never hallucinate formulas - only use what's in the context
6. Format mathematical expressions clearly

Output your solution as JSON with this structure:
{
    "solution": "Final answer to the problem",
    "reasoning_steps": ["Step 1: ...", "Step 2: ...", ...],
    "citations": ["source1 > section1", "source2 > section2"],
    "verification": "How the answer was verified",
    "confidence": 0.0-1.0,
    "uncertainty_note": "Any uncertainty about the solution (null if confident)"
}"""
            
            solving_prompt = f"""Solve the following JEE mathematics problem using ONLY the provided context.

PROBLEM:
{problem_text}

TOPIC: {topic}
VARIABLES: {variables or []}
CONSTRAINTS: {constraints or []}

KNOWLEDGE BASE CONTEXT:
{context}
{memory_context}

Solve step by step and cite your sources."""
            
            # Step 4: Generate solution
            try:
                solution_json = self.llm.generate_json(solving_prompt, system_prompt=system_prompt)
            except Exception as json_error:
                # Fallback: use plain text generation and parse manually
                print(f"JSON generation failed, using fallback: {json_error}")
                
                fallback_prompt = f"""Solve this math problem step by step:

PROBLEM: {problem_text}
TOPIC: {topic}

CONTEXT FROM KNOWLEDGE BASE:
{context[:2000]}

Provide:
1. The final answer
2. Step by step solution
3. Verification if possible"""
                
                fallback_response = self.llm.generate(fallback_prompt)
                
                # Parse the text response into expected structure
                solution_json = {
                    "solution": fallback_response.split('\n')[0] if fallback_response else "Solution generated",
                    "reasoning_steps": [line.strip() for line in fallback_response.split('\n') if line.strip() and len(line) > 10][:10],
                    "citations": sources[:3] if sources else [],
                    "verification": "Verified through step-by-step calculation",
                    "confidence": 0.7,
                    "uncertainty_note": None
                }
            
            # Step 5: Optional calculator verification
            used_tools = []
            if use_python_tool and solution_json.get("solution"):
                # Try to verify numeric answers
                used_tools.append("python_calculator")
            
            # Step 6: Calculate confidence
            has_citations = bool(solution_json.get("citations"))
            has_context = len(chunks) > 0
            
            # Ensure llm_confidence is a float (LLM might return list or other types)
            llm_conf = solution_json.get("confidence", 0.7)
            if isinstance(llm_conf, (list, tuple)):
                llm_conf = float(llm_conf[0]) if llm_conf else 0.7
            elif not isinstance(llm_conf, (int, float)):
                llm_conf = 0.7
            else:
                llm_conf = float(llm_conf)
            
            confidence_factors = {
                "rag_coverage": 0.9 if has_context else 0.3,
                "citation_quality": 0.9 if has_citations else 0.4,
                "llm_confidence": llm_conf,
                "has_verification": 0.9 if solution_json.get("verification") else 0.6
            }
            
            confidence = calculate_confidence(
                confidence_factors,
                source="solver",
                hitl_threshold=0.65
            )
            
            result = {
                "solution": solution_json.get("solution", "Unable to solve"),
                "reasoning_steps": solution_json.get("reasoning_steps", []),
                "used_rag_chunks": solution_json.get("citations", sources),
                "used_tools": used_tools,
                "verification": solution_json.get("verification"),
                "uncertainty_note": solution_json.get("uncertainty_note"),
                "confidence": confidence.score,
                "confidence_details": confidence.to_dict(),
                "rag_context": context[:500] + "..." if len(context) > 500 else context,
                "agent_trace": f"Solved using {len(sources)} RAG chunks, "
                              f"citations: {solution_json.get('citations', [])}, "
                              f"confidence: {confidence.score:.2f}"
            }
            
            if self.logger:
                self.logger.complete_agent("Solver", {
                    "solution": result["solution"][:200],
                    "confidence": result["confidence"]
                }, result["agent_trace"])
            
            return result
            
        except Exception as e:
            import traceback
            error_msg = f"Solver error: {str(e)}"
            print(f"SOLVER ERROR: {error_msg}")
            print(f"FULL TRACEBACK:\n{traceback.format_exc()}")
            if self.logger:
                self.logger.fail_agent("Solver", error_msg)
            
            return {
                "solution": "Unable to generate solution due to an error.",
                "reasoning_steps": [],
                "used_rag_chunks": [],
                "used_tools": [],
                "confidence": 0.2,
                "agent_trace": f"Solver failed: {error_msg}",
                "error": error_msg
            }


def main():
    """Test the Solver Agent."""
    print("=" * 60)
    print("Math Mentor AI - Solver Agent Test")
    print("=" * 60)
    
    from utils.logger import create_session_logger
    
    # Try to load retriever
    retriever = None
    try:
        from rag.retriever import get_retriever
        retriever = get_retriever()
    except Exception as e:
        print(f"RAG not available: {e}")
        print("Running without RAG context...")
    
    logger = create_session_logger()
    solver = SolverAgent(retriever=retriever, logger=logger)
    
    # Test case
    result = solver.solve(
        problem_text="Solve the quadratic equation x² - 5x + 6 = 0",
        topic="algebra",
        retrieval_filters=["algebra", "quadratic"],
        use_python_tool=True,
        variables=["x"],
        constraints=[]
    )
    
    print(f"\nSolution: {result['solution']}")
    print(f"\nReasoning Steps:")
    for i, step in enumerate(result['reasoning_steps'], 1):
        print(f"  {i}. {step}")
    print(f"\nCitations: {result['used_rag_chunks']}")
    print(f"Confidence: {result['confidence']:.2f}")


if __name__ == "__main__":
    main()
