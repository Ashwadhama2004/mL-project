"""
Parser Agent for Math Mentor AI

This agent is responsible for understanding and structuring the input problem.
It cleans the text, detects the topic, extracts variables/constraints,
and identifies if clarification is needed.
"""

import re
from typing import Dict, Any, List, Optional

from utils.llm_client import get_llm_client
from utils.confidence import calculate_confidence, ConfidenceScore
from utils.logger import AgentLogger


class ParserAgent:
    """
    Parser Agent: Structures and understands the input problem.
    
    Responsibilities:
    - Clean spelling and grammar
    - Normalize mathematical notation
    - Detect problem type/topic
    - Extract variables and constraints
    - Check for ambiguity
    - Generate clarification questions if needed
    """
    
    TOPIC_KEYWORDS = {
        "algebra": ["equation", "solve", "roots", "quadratic", "polynomial", "factor", 
                   "expand", "simplify", "logarithm", "log", "exponent", "inequality"],
        "calculus": ["derivative", "differentiate", "integral", "integrate", "limit",
                    "continuous", "maximum", "minimum", "tangent", "area under"],
        "trigonometry": ["sin", "cos", "tan", "angle", "triangle", "radian", "degree",
                        "trigonometric", "inverse trig", "height", "distance"],
        "probability": ["probability", "chance", "dice", "card", "random", "expected",
                       "binomial", "bayes", "conditional", "independent"],
        "coordinate_geometry": ["line", "circle", "parabola", "ellipse", "hyperbola",
                               "slope", "intercept", "conic", "locus", "tangent to"],
        "linear_algebra": ["vector", "matrix", "determinant", "eigenvalue", "dot product",
                          "cross product", "plane", "coplanar", "shortest distance"],
        "complex_numbers": ["complex", "imaginary", "modulus", "argument", "conjugate",
                           "argand", "de moivre", "roots of unity"],
        "sequences_series": ["sequence", "series", "AP", "GP", "HP", "sum of", "nth term",
                            "arithmetic", "geometric", "harmonic"],
        "differential_equations": ["differential equation", "dy/dx", "separable", 
                                   "linear differential", "order", "degree of"],
        "permutations_combinations": ["permutation", "combination", "arrange", "select",
                                      "ways", "factorial", "nCr", "nPr"],
        "binomial_theorem": ["binomial", "expansion", "coefficient of", "general term",
                            "middle term", "greatest term"],
        "statistics": ["mean", "median", "mode", "variance", "standard deviation",
                      "correlation", "regression"],
    }
    
    def __init__(self, logger: AgentLogger = None):
        """
        Initialize the Parser Agent.
        
        Args:
            logger: Agent logger for execution tracing
        """
        self.llm = get_llm_client()
        self.logger = logger
    
    def _detect_topic_keywords(self, text: str) -> List[str]:
        """
        Detect topic based on keyword matching.
        
        Args:
            text: Problem text
            
        Returns:
            List of detected topics
        """
        text_lower = text.lower()
        detected = []
        
        for topic, keywords in self.TOPIC_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    detected.append(topic)
                    break
        
        return detected if detected else ["general"]
    
    def _normalize_math_notation(self, text: str) -> str:
        """
        Normalize mathematical notation in text.
        
        Args:
            text: Raw text
            
        Returns:
            Normalized text
        """
        normalized = text
        
        # Common replacements
        replacements = [
            (r'\bsquare root of\b', '√'),
            (r'\bsqrt\b', '√'),
            (r'\bcube root of\b', '∛'),
            (r'\bintegral of\b', '∫'),
            (r'\bsummation of\b', 'Σ'),
            (r'\bsigma\b', 'Σ'),
            (r'\bpi\b', 'π'),
            (r'\btheta\b', 'θ'),
            (r'\balpha\b', 'α'),
            (r'\bbeta\b', 'β'),
            (r'\bdelta\b', 'δ'),
            (r'\binfinity\b', '∞'),
            (r'\bless than or equal\b', '≤'),
            (r'\bgreater than or equal\b', '≥'),
            (r'\bnot equal\b', '≠'),
            (r'\bplus or minus\b', '±'),
            (r'\bx\s*\^\s*2\b', 'x²'),
            (r'\bx\s*\^\s*3\b', 'x³'),
            (r'\bx squared\b', 'x²'),
            (r'\bx cubed\b', 'x³'),
        ]
        
        for pattern, replacement in replacements:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        
        return normalized
    
    def _extract_variables(self, text: str) -> List[str]:
        """
        Extract mathematical variables from text.
        
        Args:
            text: Problem text
            
        Returns:
            List of variable names
        """
        # Common single-letter variables
        # Exclude common words like 'a', 'I'
        variable_pattern = r'\b([a-z])\b'
        matches = re.findall(variable_pattern, text)
        
        # Filter out common articles and pronouns
        exclude = {'a', 'i', 'o'}
        variables = [v for v in set(matches) if v not in exclude]
        
        # Also look for subscripted variables like x1, y2
        subscripted = re.findall(r'\b([a-z])[\d₁₂₃₄₅]+\b', text, re.IGNORECASE)
        variables.extend([v.lower() for v in subscripted])
        
        return sorted(set(variables))
    
    def parse(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and structure the input problem.
        
        Args:
            input_data: Dictionary containing:
                - raw_text: The problem text
                - source: "ocr" | "asr" | "text"
                
        Returns:
            Dictionary containing:
                - problem_text: Cleaned text
                - topic: Detected topic
                - variables: List of variables
                - constraints: List of constraints
                - needs_clarification: Boolean
                - clarification_question: If needed
                - confidence: Float
                - agent_trace: String description
        """
        raw_text = input_data.get("raw_text", "")
        source = input_data.get("source", "text")
        
        if self.logger:
            self.logger.start_agent("Parser", input_data, "Parsing input problem")
        
        try:
            # Step 1: Normalize notation
            normalized_text = self._normalize_math_notation(raw_text)
            
            # Step 2: Detect topics using keywords
            keyword_topics = self._detect_topic_keywords(normalized_text)
            
            # Step 3: Extract variables
            variables = self._extract_variables(normalized_text)
            
            # Step 4: Use LLM for deeper analysis
            system_prompt = """You are a mathematics problem parser. Analyze the given math problem and extract:
1. The cleaned, properly formatted problem text
2. The primary mathematical topic (one of: algebra, calculus, trigonometry, probability, coordinate_geometry, linear_algebra, complex_numbers, sequences_series, differential_equations, permutations_combinations, binomial_theorem, statistics, matrices_determinants, vectors_3d)
3. All variables used in the problem
4. Any constraints or conditions mentioned
5. Whether the problem is ambiguous and needs clarification
6. If ambiguous, what clarification question to ask

Be precise and thorough. If the problem is incomplete or unclear, identify exactly what information is missing."""
            
            analysis_prompt = f"""Analyze this math problem:

INPUT SOURCE: {source}
RAW TEXT: {raw_text}
NORMALIZED TEXT: {normalized_text}
DETECTED TOPICS (from keywords): {keyword_topics}
DETECTED VARIABLES: {variables}

Provide your analysis in this exact JSON format:
{{
    "cleaned_problem": "the cleaned, well-formatted problem text",
    "primary_topic": "main topic category",
    "secondary_topics": ["other relevant topics"],
    "variables": ["list", "of", "variables"],
    "constraints": ["list of constraints or conditions"],
    "is_ambiguous": true/false,
    "ambiguity_reason": "reason if ambiguous, null otherwise",
    "clarification_question": "question to ask if ambiguous, null otherwise",
    "problem_type": "equation/proof/word_problem/calculation/optimization/etc",
    "confidence": 0.0-1.0
}}"""
            
            analysis = self.llm.generate_json(analysis_prompt, system_prompt=system_prompt)
            
            # Calculate confidence
            confidence_factors = {
                "source_reliability": 1.0 if source == "text" else 0.8,
                "topic_detection": 0.9 if keyword_topics and keyword_topics[0] != "general" else 0.6,
                "llm_confidence": analysis.get("confidence", 0.7),
                "has_variables": 0.9 if variables else 0.5,
                "not_ambiguous": 0.1 if analysis.get("is_ambiguous", False) else 0.9
            }
            
            confidence = calculate_confidence(
                confidence_factors,
                source="parser",
                hitl_threshold=0.7
            )
            
            result = {
                "problem_text": analysis.get("cleaned_problem", normalized_text),
                "topic": analysis.get("primary_topic", keyword_topics[0] if keyword_topics else "general"),
                "secondary_topics": analysis.get("secondary_topics", keyword_topics[1:] if len(keyword_topics) > 1 else []),
                "variables": analysis.get("variables", variables),
                "constraints": analysis.get("constraints", []),
                "problem_type": analysis.get("problem_type", "unknown"),
                "needs_clarification": analysis.get("is_ambiguous", False),
                "clarification_question": analysis.get("clarification_question"),
                "ambiguity_reason": analysis.get("ambiguity_reason"),
                "confidence": confidence.score,
                "confidence_details": confidence.to_dict(),
                "agent_trace": f"Parsed problem: topic={analysis.get('primary_topic')}, "
                              f"variables={analysis.get('variables')}, "
                              f"ambiguous={analysis.get('is_ambiguous')}"
            }
            
            if self.logger:
                self.logger.complete_agent("Parser", result, result["agent_trace"])
                
                if result["needs_clarification"]:
                    self.logger.hitl_required(
                        "Parser",
                        result["ambiguity_reason"],
                        result["clarification_question"]
                    )
            
            return result
            
        except Exception as e:
            error_msg = f"Parser error: {str(e)}"
            if self.logger:
                self.logger.fail_agent("Parser", error_msg)
            
            # Return a fallback result
            return {
                "problem_text": raw_text,
                "topic": "general",
                "variables": self._extract_variables(raw_text),
                "constraints": [],
                "needs_clarification": True,
                "clarification_question": "Could you please rephrase the problem more clearly?",
                "confidence": 0.3,
                "agent_trace": f"Parser failed: {error_msg}",
                "error": error_msg
            }


def main():
    """Test the Parser Agent."""
    print("=" * 60)
    print("Math Mentor AI - Parser Agent Test")
    print("=" * 60)
    
    from utils.logger import create_session_logger
    
    logger = create_session_logger()
    parser = ParserAgent(logger=logger)
    
    # Test cases
    test_cases = [
        {
            "raw_text": "Solve x squared minus 5x plus 6 equals 0",
            "source": "asr"
        },
        {
            "raw_text": "Find the derivative of sin(x) * cos(x)",
            "source": "text"
        },
        {
            "raw_text": "Find the value",  # Ambiguous
            "source": "asr"
        },
        {
            "raw_text": "What is the probability of getting at least 2 heads when tossing 3 fair coins?",
            "source": "text"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['raw_text'][:50]}...")
        result = parser.parse(test)
        print(f"  Topic: {result['topic']}")
        print(f"  Variables: {result['variables']}")
        print(f"  Needs clarification: {result['needs_clarification']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        if result['needs_clarification']:
            print(f"  Question: {result['clarification_question']}")


if __name__ == "__main__":
    main()
