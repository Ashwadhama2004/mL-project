"""
Explainer Agent for Math Mentor AI

This agent converts verified solutions into student-friendly explanations
with pedagogical formatting suitable for JEE exam preparation.
"""

from typing import Dict, Any, List
from utils.llm_client import get_llm_client
from utils.logger import AgentLogger


class ExplainerAgent:
    """
    Explainer Agent: Converts solutions to student-friendly explanations.
    
    Responsibilities:
    - Restructure into pedagogical steps
    - Add context and intuition
    - Use JEE exam-style language
    - Avoid jargon overload
    - Make it exam-writable
    """
    
    def __init__(self, logger: AgentLogger = None):
        """
        Initialize the Explainer Agent.
        
        Args:
            logger: Agent logger for execution tracing
        """
        self.llm = get_llm_client()
        self.logger = logger
    
    def explain(
        self,
        problem_text: str,
        solution: str,
        reasoning_steps: List[str],
        topic: str,
        used_rag_chunks: List[str] = None,
        difficulty_level: str = "JEE-intermediate"
    ) -> Dict[str, Any]:
        """
        Generate a student-friendly explanation.
        
        Args:
            problem_text: Original problem
            solution: The solution
            reasoning_steps: Steps from solver
            topic: Problem topic
            used_rag_chunks: Citations used
            difficulty_level: JEE difficulty level
            
        Returns:
            Dictionary containing:
                - final_explanation: Student-friendly version
                - steps: Structured steps
                - key_concepts: Learning points
                - difficulty_level: JEE level
                - exam_tips: Tips for similar problems
                - agent_trace: String description
        """
        if self.logger:
            self.logger.start_agent(
                "Explainer",
                {"solution": solution[:100], "topic": topic},
                "Creating student-friendly explanation"
            )
        
        try:
            system_prompt = """You are an expert JEE mathematics tutor creating clear, educational explanations.

Your explanations should:
1. Start with a brief problem overview
2. Break down the solution into clear, numbered steps
3. Explain the "why" behind each step, not just the "what"
4. Highlight key formulas and concepts used
5. Use simple language - avoid unnecessary jargon
6. Add intuition and visual descriptions where helpful
7. End with key takeaways and exam tips
8. Format for easy reading (use bullet points, bold key terms)

Remember: Students should be able to reproduce this solution in an exam after reading your explanation."""
            
            explain_prompt = f"""Create a student-friendly explanation for this JEE mathematics problem.

PROBLEM:
{problem_text}

TOPIC: {topic}
DIFFICULTY: {difficulty_level}

SOLUTION:
{solution}

ORIGINAL REASONING:
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(reasoning_steps))}

KNOWLEDGE SOURCES USED:
{', '.join(used_rag_chunks) if used_rag_chunks else 'Standard mathematical principles'}

Provide your explanation as JSON:
{{
    "problem_overview": "Brief 1-2 sentence summary of what we're solving",
    "approach": "Brief description of the approach we'll use",
    "steps": [
        {{
            "step_number": 1,
            "action": "What we do in this step",
            "explanation": "Why we do it and how",
            "formula_used": "Formula if any (null if none)"
        }}
    ],
    "final_answer": "The final answer, clearly stated",
    "key_concepts": ["Concept 1", "Concept 2"],
    "exam_tips": ["Tip 1 for similar problems", "Tip 2"],
    "common_mistakes_to_avoid": ["Mistake 1", "Mistake 2"],
    "alternative_approaches": "Brief note on other ways to solve (optional)"
}}"""
            
            explanation = self.llm.generate_json(explain_prompt, system_prompt=system_prompt)
            
            # Format the final explanation
            final_explanation = self._format_explanation(explanation)
            
            result = {
                "final_explanation": final_explanation,
                "problem_overview": explanation.get("problem_overview", ""),
                "approach": explanation.get("approach", ""),
                "steps": explanation.get("steps", []),
                "final_answer": explanation.get("final_answer", solution),
                "key_concepts": explanation.get("key_concepts", []),
                "exam_tips": explanation.get("exam_tips", []),
                "common_mistakes": explanation.get("common_mistakes_to_avoid", []),
                "alternative_approaches": explanation.get("alternative_approaches"),
                "difficulty_level": difficulty_level,
                "agent_trace": f"Generated explanation with {len(explanation.get('steps', []))} steps, "
                              f"{len(explanation.get('key_concepts', []))} key concepts"
            }
            
            if self.logger:
                self.logger.complete_agent("Explainer", {
                    "steps_count": len(result["steps"]),
                    "concepts_count": len(result["key_concepts"])
                }, result["agent_trace"])
            
            return result
            
        except Exception as e:
            error_msg = f"Explainer error: {str(e)}"
            if self.logger:
                self.logger.fail_agent("Explainer", error_msg)
            
            # Fallback: Return original solution with basic formatting
            return {
                "final_explanation": f"**Problem:** {problem_text}\n\n**Solution:**\n{solution}",
                "steps": [{"step_number": i+1, "action": step} for i, step in enumerate(reasoning_steps)],
                "key_concepts": [],
                "exam_tips": [],
                "difficulty_level": difficulty_level,
                "agent_trace": f"Explainer failed, using fallback: {error_msg}",
                "error": error_msg
            }
    
    def _format_explanation(self, explanation: Dict) -> str:
        """
        Format the explanation dictionary into readable text.
        
        Args:
            explanation: Explanation dictionary from LLM
            
        Returns:
            Formatted explanation string
        """
        parts = []
        
        # Problem overview
        if explanation.get("problem_overview"):
            parts.append(f"**📌 Problem Overview**\n{explanation['problem_overview']}")
        
        # Approach
        if explanation.get("approach"):
            parts.append(f"**🎯 Approach**\n{explanation['approach']}")
        
        # Steps
        steps = explanation.get("steps", [])
        if steps:
            step_text = "**📝 Step-by-Step Solution**\n"
            for step in steps:
                step_num = step.get("step_number", "")
                action = step.get("action", "")
                explain = step.get("explanation", "")
                formula = step.get("formula_used")
                
                step_text += f"\n**Step {step_num}:** {action}\n"
                if explain:
                    step_text += f"_{explain}_\n"
                if formula:
                    step_text += f"📐 Formula: `{formula}`\n"
            
            parts.append(step_text)
        
        # Final answer
        if explanation.get("final_answer"):
            parts.append(f"**✅ Final Answer**\n{explanation['final_answer']}")
        
        # Key concepts
        concepts = explanation.get("key_concepts", [])
        if concepts:
            concept_list = "\n".join(f"• {c}" for c in concepts)
            parts.append(f"**📚 Key Concepts Used**\n{concept_list}")
        
        # Exam tips
        tips = explanation.get("exam_tips", [])
        if tips:
            tips_list = "\n".join(f"💡 {t}" for t in tips)
            parts.append(f"**🎓 JEE Exam Tips**\n{tips_list}")
        
        # Common mistakes
        mistakes = explanation.get("common_mistakes_to_avoid", [])
        if mistakes:
            mistakes_list = "\n".join(f"⚠️ {m}" for m in mistakes)
            parts.append(f"**🚫 Common Mistakes to Avoid**\n{mistakes_list}")
        
        return "\n\n---\n\n".join(parts)


def main():
    """Test the Explainer Agent."""
    print("=" * 60)
    print("Math Mentor AI - Explainer Agent Test")
    print("=" * 60)
    
    from utils.logger import create_session_logger
    
    logger = create_session_logger()
    explainer = ExplainerAgent(logger=logger)
    
    result = explainer.explain(
        problem_text="Solve x² - 5x + 6 = 0",
        solution="x = 2 or x = 3",
        reasoning_steps=[
            "Identify this as a quadratic equation in standard form ax² + bx + c = 0",
            "Here a=1, b=-5, c=6",
            "Factor: x² - 5x + 6 = (x - 2)(x - 3)",
            "Set each factor to zero",
            "x - 2 = 0 gives x = 2",
            "x - 3 = 0 gives x = 3"
        ],
        topic="algebra",
        used_rag_chunks=["algebra > Quadratic Equations"],
        difficulty_level="JEE-basic"
    )
    
    print("\nFinal Explanation:")
    print("=" * 40)
    print(result["final_explanation"])
    print("\n" + "=" * 40)
    print(f"Key Concepts: {result['key_concepts']}")
    print(f"Exam Tips: {result['exam_tips']}")


if __name__ == "__main__":
    main()
