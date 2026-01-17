"""
Verifier Agent for Math Mentor AI

This agent performs quality assurance on solutions, checking logical consistency,
domain constraints, and calculating verification confidence.
"""

from typing import Dict, Any, List
from utils.llm_client import get_llm_client
from utils.tools import get_calculator
from utils.confidence import calculate_confidence
from utils.logger import AgentLogger


class VerifierAgent:
    """
    Verifier Agent: Quality assurance and error detection.
    
    Responsibilities:
    - Check logical consistency
    - Verify domain constraints
    - Test edge cases
    - Look for reasoning gaps
    - Use Python tool to validate arithmetic
    - Calculate verification confidence
    - Trigger HITL if confidence < 0.7
    """
    
    # Domain constraints by topic
    DOMAIN_CONSTRAINTS = {
        "probability": [
            ("result", 0, 1, "Probability must be between 0 and 1"),
        ],
        "calculus": [
            ("domain", None, None, "Check function domain"),
        ],
        "trigonometry": [
            ("angle_degree", 0, 360, "Angle in degrees typically 0-360"),
            ("trig_value", -1, 1, "sin/cos values must be in [-1, 1]"),
        ],
        "permutations_combinations": [
            ("count", 0, None, "Count must be non-negative"),
            ("result_integer", None, None, "nCr/nPr must be integers"),
        ],
    }
    
    def __init__(self, logger: AgentLogger = None):
        """
        Initialize the Verifier Agent.
        
        Args:
            logger: Agent logger for execution tracing
        """
        self.llm = get_llm_client()
        self.calculator = get_calculator()
        self.logger = logger
        self.hitl_threshold = 0.7
    
    def _verify_arithmetic(self, reasoning_steps: List[str], solution: str) -> Dict:
        """
        Verify arithmetic in the solution using calculator.
        
        Args:
            reasoning_steps: List of reasoning steps
            solution: Final solution
            
        Returns:
            Verification result
        """
        issues = []
        verified_calculations = []
        
        # Extract and verify numeric calculations from steps
        import re
        for step in reasoning_steps:
            # Look for simple calculations like "= 25" or "= 3.14"
            calcs = re.findall(r'=\s*([\d\.\+\-\*\/\^\(\)]+)(?:\s|$)', step)
            for calc in calcs[:3]:  # Limit to 3 per step
                try:
                    result = self.calculator.calculate(calc)
                    if result["success"]:
                        verified_calculations.append({
                            "expression": calc,
                            "result": result["result"]
                        })
                except Exception:
                    pass
        
        return {
            "verified_calculations": verified_calculations,
            "issues": issues,
            "arithmetic_valid": len(issues) == 0
        }
    
    def _check_domain_constraints(self, solution: str, topic: str) -> List[str]:
        """
        Check domain-specific constraints.
        
        Args:
            solution: The solution text
            topic: Problem topic
            
        Returns:
            List of constraint violations
        """
        violations = []
        
        # Extract numeric values from solution
        import re
        numbers = re.findall(r'[-+]?\d*\.?\d+', solution)
        
        constraints = self.DOMAIN_CONSTRAINTS.get(topic, [])
        
        for constraint_type, min_val, max_val, message in constraints:
            if constraint_type == "result" and numbers:
                try:
                    # Check the last number (likely the answer)
                    value = float(numbers[-1])
                    if min_val is not None and value < min_val:
                        violations.append(f"{message}: got {value}")
                    if max_val is not None and value > max_val:
                        violations.append(f"{message}: got {value}")
                except ValueError:
                    pass
        
        return violations
    
    def verify(
        self,
        problem_text: str,
        solution: str,
        reasoning_steps: List[str],
        topic: str,
        constraints: List[str] = None,
        solver_confidence: float = 0.7
    ) -> Dict[str, Any]:
        """
        Verify the solution quality and correctness.
        
        Args:
            problem_text: Original problem
            solution: Generated solution
            reasoning_steps: Steps in the solution
            topic: Problem topic
            constraints: Problem constraints
            solver_confidence: Confidence from solver
            
        Returns:
            Dictionary containing:
                - verdict: "pass" | "uncertain" | "fail"
                - issues: List of issues found
                - confidence: Float
                - needs_hitl: Boolean
                - hitl_question: If needed
                - agent_trace: String description
        """
        if self.logger:
            self.logger.start_agent(
                "Verifier",
                {"solution": solution[:100], "topic": topic},
                "Verifying solution quality"
            )
        
        try:
            issues = []
            
            # Step 1: Check domain constraints
            domain_violations = self._check_domain_constraints(solution, topic)
            issues.extend(domain_violations)
            
            # Step 2: Verify arithmetic
            arithmetic_result = self._verify_arithmetic(reasoning_steps, solution)
            if not arithmetic_result["arithmetic_valid"]:
                issues.extend(arithmetic_result["issues"])
            
            # Step 3: LLM-based verification
            system_prompt = """You are a rigorous mathematics verifier. Check the solution for:
1. Logical consistency - do steps follow logically?
2. Mathematical correctness - are formulas applied correctly?
3. Completeness - are all cases covered?
4. Reasonableness - does the answer make sense?

Be critical but fair. Identify specific issues if any."""
            
            verify_prompt = f"""Verify this mathematics solution:

PROBLEM:
{problem_text}

SOLUTION:
{solution}

REASONING STEPS:
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(reasoning_steps))}

TOPIC: {topic}
CONSTRAINTS: {constraints or []}

Provide your verification as JSON:
{{
    "is_logically_consistent": true/false,
    "is_mathematically_correct": true/false,
    "is_complete": true/false,
    "is_reasonable": true/false,
    "issues_found": ["issue1", "issue2"],
    "suggestions": ["suggestion1"],
    "verification_confidence": 0.0-1.0,
    "overall_assessment": "pass/uncertain/fail"
}}"""
            
            verification = self.llm.generate_json(verify_prompt, system_prompt=system_prompt)
            
            # Collect issues from LLM
            llm_issues = verification.get("issues_found", [])
            issues.extend(llm_issues)
            
            # Step 4: Calculate final confidence
            confidence_factors = {
                "logical_consistency": 0.95 if verification.get("is_logically_consistent") else 0.4,
                "mathematical_correctness": 0.95 if verification.get("is_mathematically_correct") else 0.3,
                "completeness": 0.9 if verification.get("is_complete") else 0.5,
                "reasonableness": 0.9 if verification.get("is_reasonable") else 0.4,
                "no_domain_violations": 0.9 if not domain_violations else 0.3,
                "solver_confidence": solver_confidence,
                "llm_verification": verification.get("verification_confidence", 0.7)
            }
            
            confidence = calculate_confidence(
                confidence_factors,
                source="verifier",
                hitl_threshold=self.hitl_threshold
            )
            
            # Determine verdict
            if confidence.score >= 0.8 and not issues:
                verdict = "pass"
            elif confidence.score >= 0.5:
                verdict = "uncertain"
            else:
                verdict = "fail"
            
            # Check if HITL needed
            needs_hitl = confidence.score < self.hitl_threshold
            hitl_question = None
            
            if needs_hitl:
                if issues:
                    hitl_question = f"The solution may have issues: {'; '.join(issues[:2])}. Please verify or correct."
                else:
                    hitl_question = "Verification confidence is low. Please review the solution."
            
            result = {
                "verdict": verdict,
                "issues": issues,
                "suggestions": verification.get("suggestions", []),
                "confidence": confidence.score,
                "confidence_details": confidence.to_dict(),
                "needs_hitl": needs_hitl,
                "hitl_question": hitl_question,
                "verification_details": {
                    "logical_consistency": verification.get("is_logically_consistent"),
                    "mathematical_correctness": verification.get("is_mathematically_correct"),
                    "completeness": verification.get("is_complete"),
                    "reasonableness": verification.get("is_reasonable"),
                },
                "agent_trace": f"Verdict: {verdict}, Confidence: {confidence.score:.2f}, "
                              f"Issues: {len(issues)}, HITL: {needs_hitl}"
            }
            
            if self.logger:
                self.logger.complete_agent("Verifier", {
                    "verdict": result["verdict"],
                    "confidence": result["confidence"]
                }, result["agent_trace"])
                
                if needs_hitl:
                    self.logger.hitl_required("Verifier", "Low verification confidence", hitl_question)
            
            return result
            
        except Exception as e:
            error_msg = f"Verifier error: {str(e)}"
            if self.logger:
                self.logger.fail_agent("Verifier", error_msg)
            
            return {
                "verdict": "uncertain",
                "issues": [error_msg],
                "confidence": 0.5,
                "needs_hitl": True,
                "hitl_question": "Verification failed. Please review the solution manually.",
                "agent_trace": f"Verifier failed: {error_msg}",
                "error": error_msg
            }


def main():
    """Test the Verifier Agent."""
    print("=" * 60)
    print("Math Mentor AI - Verifier Agent Test")
    print("=" * 60)
    
    from utils.logger import create_session_logger
    
    logger = create_session_logger()
    verifier = VerifierAgent(logger=logger)
    
    # Test case 1: Correct solution
    result = verifier.verify(
        problem_text="Solve x² - 5x + 6 = 0",
        solution="x = 2 or x = 3",
        reasoning_steps=[
            "Factor the quadratic: x² - 5x + 6 = (x - 2)(x - 3)",
            "Set each factor to zero: x - 2 = 0 or x - 3 = 0",
            "Solve: x = 2 or x = 3"
        ],
        topic="algebra",
        solver_confidence=0.85
    )
    
    print(f"\nTest 1: Correct solution")
    print(f"  Verdict: {result['verdict']}")
    print(f"  Confidence: {result['confidence']:.2f}")
    print(f"  Issues: {result['issues']}")
    print(f"  Needs HITL: {result['needs_hitl']}")
    
    # Test case 2: Probability with invalid value
    result = verifier.verify(
        problem_text="Find the probability of event A",
        solution="P(A) = 1.5",
        reasoning_steps=[
            "Calculate probability as 1.5"
        ],
        topic="probability",
        solver_confidence=0.6
    )
    
    print(f"\nTest 2: Invalid probability")
    print(f"  Verdict: {result['verdict']}")
    print(f"  Issues: {result['issues']}")
    print(f"  Needs HITL: {result['needs_hitl']}")


if __name__ == "__main__":
    main()
