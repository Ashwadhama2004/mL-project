"""Full pipeline test to identify where the error occurs."""
import sys
sys.path.insert(0, '.')

from utils.logger import create_session_logger

print("=" * 60)
print("Testing Full Agent Pipeline")
print("=" * 60)

logger = create_session_logger()

# Initialize components
print("\n1. Initializing RAG...")
from rag.retriever import get_retriever
retriever = get_retriever()
print(f"   RAG ready")

print("\n2. Testing Parser Agent...")
from agents.parser_agent import ParserAgent
parser = ParserAgent(logger=logger)
try:
    parser_result = parser.parse({
        "raw_text": "Solve x^2 - 5x + 6 = 0",
        "source": "text"
    })
    print(f"   Parser Result:")
    print(f"     - topic: {parser_result.get('topic')}")
    print(f"     - problem_text: {parser_result.get('problem_text')}")
    print(f"     - variables: {parser_result.get('variables')}")
    print(f"     - needs_clarification: {parser_result.get('needs_clarification')}")
except Exception as e:
    print(f"   Parser ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. Testing Router Agent...")
from agents.router_agent import RouterAgent
router = RouterAgent(logger=logger)
try:
    router_result = router.route(parser_result)
    print(f"   Router Result:")
    print(f"     - route: {router_result.get('route')}")
    print(f"     - use_rag: {router_result.get('use_rag')}")
    print(f"     - retrieval_filters: {router_result.get('retrieval_filters')}")
except Exception as e:
    print(f"   Router ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. Testing Solver Agent...")
from agents.solver_agent import SolverAgent
solver = SolverAgent(retriever=retriever, logger=logger)
try:
    solver_result = solver.solve(
        problem_text=parser_result.get("problem_text", "Solve x^2 - 5x + 6 = 0"),
        topic=parser_result.get("topic", "algebra"),
        retrieval_filters=router_result.get("retrieval_filters", []),
        use_python_tool=False,
        variables=parser_result.get("variables"),
        constraints=parser_result.get("constraints")
    )
    print(f"   Solver Result:")
    print(f"     - solution: {solver_result.get('solution')[:100]}..." if solver_result.get('solution') else "     - solution: None")
    print(f"     - steps: {len(solver_result.get('reasoning_steps', []))} steps")
    print(f"     - confidence: {solver_result.get('confidence')}")
    print(f"     - error: {solver_result.get('error')}")
except Exception as e:
    print(f"   Solver ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n5. Testing Verifier Agent...")
from agents.verifier_agent import VerifierAgent
verifier = VerifierAgent(logger=logger)
try:
    verifier_result = verifier.verify(
        problem_text=parser_result.get("problem_text", "Solve x^2 - 5x + 6 = 0"),
        solution=solver_result.get("solution", ""),
        reasoning_steps=solver_result.get("reasoning_steps", []),
        topic=parser_result.get("topic", "algebra"),
        constraints=parser_result.get("constraints"),
        solver_confidence=solver_result.get("confidence", 0.7)
    )
    print(f"   Verifier Result:")
    print(f"     - verdict: {verifier_result.get('verdict')}")
    print(f"     - confidence: {verifier_result.get('confidence')}")
    print(f"     - needs_hitl: {verifier_result.get('needs_hitl')}")
except Exception as e:
    print(f"   Verifier ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n6. Testing Explainer Agent...")
from agents.explainer_agent import ExplainerAgent
explainer = ExplainerAgent(logger=logger)
try:
    explainer_result = explainer.explain(
        problem_text=parser_result.get("problem_text", "Solve x^2 - 5x + 6 = 0"),
        solution=solver_result.get("solution", ""),
        reasoning_steps=solver_result.get("reasoning_steps", []),
        topic=parser_result.get("topic", "algebra"),
        used_rag_chunks=solver_result.get("used_rag_chunks"),
        difficulty_level="JEE-intermediate"
    )
    print(f"   Explainer Result:")
    print(f"     - final_explanation: {explainer_result.get('final_explanation', '')[:100]}...")
    print(f"     - steps: {len(explainer_result.get('steps', []))} steps")
    print(f"     - key_concepts: {explainer_result.get('key_concepts')}")
except Exception as e:
    print(f"   Explainer ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Pipeline Test Complete")
print("=" * 60)
