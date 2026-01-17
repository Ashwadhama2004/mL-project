"""
Router Agent for Math Mentor AI

This agent decides the solution strategy based on the parsed problem.
It routes to appropriate solving approaches and sets up tool usage.
"""

from typing import Dict, Any, List
from utils.llm_client import get_llm_client
from utils.logger import AgentLogger


class RouterAgent:
    """
    Router Agent: Decides solution strategy.
    
    Responsibilities:
    - Map topic to solution approach
    - Decide which tools to use
    - Set RAG retrieval filters
    - Determine expected difficulty
    """
    
    # Topic to solver route mapping
    ROUTE_MAPPING = {
        "algebra": "algebraic_solver",
        "calculus": "calculus_solver",
        "trigonometry": "trigonometry_solver",
        "probability": "probability_solver",
        "coordinate_geometry": "geometry_solver",
        "linear_algebra": "vector_solver",
        "complex_numbers": "complex_solver",
        "sequences_series": "series_solver",
        "differential_equations": "ode_solver",
        "permutations_combinations": "counting_solver",
        "binomial_theorem": "binomial_solver",
        "statistics": "statistics_solver",
        "matrices_determinants": "matrix_solver",
        "vectors_3d": "vector_solver",
        "general": "general_solver"
    }
    
    # Topics that typically need Python calculator
    CALCULATOR_TOPICS = {
        "probability", "statistics", "permutations_combinations",
        "sequences_series", "binomial_theorem"
    }
    
    # Topics that typically need symbolic manipulation
    SYMBOLIC_TOPICS = {
        "algebra", "calculus", "differential_equations"
    }
    
    def __init__(self, logger: AgentLogger = None):
        """
        Initialize the Router Agent.
        
        Args:
            logger: Agent logger for execution tracing
        """
        self.llm = get_llm_client()
        self.logger = logger
    
    def _determine_difficulty(self, parser_output: Dict) -> str:
        """
        Estimate problem difficulty based on parser output.
        
        Args:
            parser_output: Output from Parser Agent
            
        Returns:
            Difficulty level string
        """
        # Simple heuristics
        variables = parser_output.get("variables", [])
        constraints = parser_output.get("constraints", [])
        problem_type = parser_output.get("problem_type", "")
        
        difficulty_score = 0
        
        # More variables = harder
        difficulty_score += min(len(variables), 3)
        
        # More constraints = harder
        difficulty_score += min(len(constraints), 2)
        
        # Optimization problems are harder
        if problem_type == "optimization":
            difficulty_score += 2
        elif problem_type == "proof":
            difficulty_score += 3
        
        # Map to difficulty level
        if difficulty_score <= 2:
            return "JEE-basic"
        elif difficulty_score <= 4:
            return "JEE-intermediate"
        else:
            return "JEE-advanced"
    
    def _get_retrieval_filters(self, parser_output: Dict) -> List[str]:
        """
        Determine RAG retrieval filters based on parsed problem.
        
        Args:
            parser_output: Output from Parser Agent
            
        Returns:
            List of filter keywords
        """
        filters = []
        
        # Primary topic
        topic = parser_output.get("topic", "")
        if topic:
            filters.append(topic)
        
        # Secondary topics
        secondary = parser_output.get("secondary_topics", [])
        filters.extend(secondary[:2])  # Limit to top 2
        
        # Problem type
        problem_type = parser_output.get("problem_type", "")
        if problem_type:
            filters.append(problem_type)
        
        return filters
    
    def route(self, parser_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decide the solution strategy based on parsed problem.
        
        Args:
            parser_output: Output from Parser Agent containing:
                - problem_text
                - topic
                - variables
                - constraints
                - problem_type
                
        Returns:
            Dictionary containing:
                - route: Solver route name
                - use_rag: Boolean
                - use_python_tool: Boolean
                - retrieval_filters: List of filter keywords
                - expected_difficulty: Difficulty level
                - strategy_notes: Additional notes
                - agent_trace: String description
        """
        if self.logger:
            self.logger.start_agent("Router", parser_output, "Deciding solution strategy")
        
        try:
            topic = parser_output.get("topic", "general")
            problem_text = parser_output.get("problem_text", "")
            problem_type = parser_output.get("problem_type", "unknown")
            
            # Determine route
            route = self.ROUTE_MAPPING.get(topic, "general_solver")
            
            # Determine tool usage
            use_python_tool = topic in self.CALCULATOR_TOPICS
            
            # Always use RAG for grounded responses
            use_rag = True
            
            # Get retrieval filters
            retrieval_filters = self._get_retrieval_filters(parser_output)
            
            # Estimate difficulty
            expected_difficulty = self._determine_difficulty(parser_output)
            
            # Use LLM for additional strategy insights
            system_prompt = """You are a math problem routing expert. Based on the problem details,
provide strategic advice for solving it. Focus on:
1. Key concepts to retrieve from knowledge base
2. Whether numerical verification would be helpful
3. Any special approaches or tricks for this problem type"""
            
            strategy_prompt = f"""Problem: {problem_text}
Topic: {topic}
Problem Type: {problem_type}
Variables: {parser_output.get('variables', [])}

Provide brief strategy notes (2-3 sentences) for solving this problem."""
            
            strategy_notes = self.llm.generate(strategy_prompt, system_prompt=system_prompt)
            strategy_notes = strategy_notes.strip()[:500]  # Limit length
            
            result = {
                "route": route,
                "use_rag": use_rag,
                "use_python_tool": use_python_tool,
                "retrieval_filters": retrieval_filters,
                "expected_difficulty": expected_difficulty,
                "strategy_notes": strategy_notes,
                "topic": topic,
                "agent_trace": f"Route: {route}, RAG: {use_rag}, Calculator: {use_python_tool}, "
                              f"Filters: {retrieval_filters}, Difficulty: {expected_difficulty}"
            }
            
            if self.logger:
                self.logger.complete_agent("Router", result, result["agent_trace"])
            
            return result
            
        except Exception as e:
            error_msg = f"Router error: {str(e)}"
            if self.logger:
                self.logger.fail_agent("Router", error_msg)
            
            # Fallback routing
            return {
                "route": "general_solver",
                "use_rag": True,
                "use_python_tool": True,
                "retrieval_filters": [parser_output.get("topic", "")],
                "expected_difficulty": "JEE-intermediate",
                "strategy_notes": "Using general approach due to routing error",
                "agent_trace": f"Router failed, using fallback: {error_msg}",
                "error": error_msg
            }


def main():
    """Test the Router Agent."""
    print("=" * 60)
    print("Math Mentor AI - Router Agent Test")
    print("=" * 60)
    
    from utils.logger import create_session_logger
    
    logger = create_session_logger()
    router = RouterAgent(logger=logger)
    
    # Test cases (simulated parser outputs)
    test_cases = [
        {
            "problem_text": "Solve x² - 5x + 6 = 0",
            "topic": "algebra",
            "variables": ["x"],
            "constraints": [],
            "problem_type": "equation"
        },
        {
            "problem_text": "Find the probability of getting at least 2 heads in 3 coin tosses",
            "topic": "probability",
            "variables": [],
            "constraints": ["fair coin", "3 tosses"],
            "problem_type": "calculation"
        },
        {
            "problem_text": "Find the maximum value of f(x) = x³ - 3x² + 2 on [0, 3]",
            "topic": "calculus",
            "variables": ["x"],
            "constraints": ["x ∈ [0, 3]"],
            "problem_type": "optimization"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['problem_text'][:50]}...")
        result = router.route(test)
        print(f"  Route: {result['route']}")
        print(f"  Use RAG: {result['use_rag']}")
        print(f"  Use Calculator: {result['use_python_tool']}")
        print(f"  Filters: {result['retrieval_filters']}")
        print(f"  Difficulty: {result['expected_difficulty']}")
        print(f"  Strategy: {result['strategy_notes'][:100]}...")


if __name__ == "__main__":
    main()
