"""
Math Mentor AI - Main Streamlit Application

An intelligent math tutoring system for JEE-level problems with multimodal input,
RAG-based knowledge retrieval, multi-agent orchestration, human-in-the-loop verification,
and self-learning capabilities.
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Math Mentor AI",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .agent-trace {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .confidence-high { color: #4CAF50; }
    .confidence-medium { color: #FFC107; }
    .confidence-low { color: #f44336; }
    .step-box {
        background-color: #fff;
        border-left: 4px solid #1E88E5;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    .citation-box {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    defaults = {
        'problem_solved': False,
        'current_result': None,
        'agent_trace': [],
        'retrieved_chunks': [],
        'hitl_required': False,
        'hitl_question': None,
        'extracted_text': '',
        'show_edit': False,
        'last_problem_id': None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar():
    """Render the sidebar with settings."""
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        # Input mode selection
        input_mode = st.selectbox(
            "Input Mode",
            ["📝 Text", "🖼️ Image (OCR)", "🎤 Audio (ASR)"],
            index=0
        )
        
        st.markdown("---")
        
        # Model settings
        st.markdown("### 🤖 Model Settings")
        model_name = st.selectbox(
            "LLM Model",
            ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-pro"],
            index=0
        )
        
        # RAG settings
        st.markdown("### 📚 RAG Settings")
        top_k = st.slider("Top-K Results", 3, 10, 5)
        
        # Confidence thresholds
        st.markdown("### 📊 Thresholds")
        ocr_threshold = st.slider("OCR Confidence", 0.5, 1.0, 0.75)
        verifier_threshold = st.slider("Verifier Confidence", 0.5, 1.0, 0.70)
        
        st.markdown("---")
        
        # Stats
        st.markdown("### 📈 Memory Stats")
        try:
            from memory.memory_store import get_memory_store
            store = get_memory_store()
            stats = store.get_stats()
            st.metric("Total Problems", stats.get("total_problems", 0))
            st.metric("Avg Confidence", f"{stats.get('average_confidence', 0):.1%}")
        except Exception:
            st.info("Memory stats unavailable")
        
        return {
            "input_mode": input_mode,
            "model_name": model_name,
            "top_k": top_k,
            "ocr_threshold": ocr_threshold,
            "verifier_threshold": verifier_threshold
        }


def render_input_section(settings):
    """Render the input section based on selected mode."""
    st.markdown("## 📝 Input Your Problem")
    
    input_mode = settings["input_mode"]
    
    if "Text" in input_mode:
        problem_text = st.text_area(
            "Enter your math problem:",
            height=100,
            placeholder="e.g., Solve x² - 5x + 6 = 0"
        )
        return {"type": "text", "content": problem_text}
    
    elif "Image" in input_mode:
        uploaded_file = st.file_uploader(
            "Upload an image of your math problem",
            type=["png", "jpg", "jpeg"]
        )
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", width=400)
            return {"type": "image", "content": uploaded_file.getvalue()}
        return None
    
    elif "Audio" in input_mode:
        st.info("🎤 Audio input: Upload an audio file or record (recording coming soon)")
        uploaded_audio = st.file_uploader(
            "Upload an audio file",
            type=["wav", "mp3", "m4a"]
        )
        if uploaded_audio:
            st.audio(uploaded_audio)
            return {"type": "audio", "content": uploaded_audio.getvalue()}
        return None
    
    return None


def process_input(input_data, settings):
    """Process the input through the appropriate processor."""
    try:
        if input_data["type"] == "text":
            from input_processors.text import TextProcessor
            processor = TextProcessor()
            return processor.process(input_data["content"])
        
        elif input_data["type"] == "image":
            from input_processors.ocr import OCRProcessor
            processor = OCRProcessor(confidence_threshold=settings["ocr_threshold"])
            result = processor.process_bytes(input_data["content"])
            return {
                "clean_text": result.get("extracted_text", ""),
                "confidence": result.get("confidence", 0),
                "needs_human_review": result.get("needs_human_review", True),
                "source": "ocr"
            }
        
        elif input_data["type"] == "audio":
            from input_processors.asr import ASRProcessor
            processor = ASRProcessor()
            result = processor.process_bytes(input_data["content"])
            return {
                "clean_text": result.get("transcript", ""),
                "confidence": result.get("confidence", 0),
                "needs_human_review": result.get("needs_human_review", True),
                "source": "asr"
            }
    except Exception as e:
        st.error(f"Input processing error: {str(e)}")
        return None
    
    return None


def run_agent_pipeline(problem_text, source, settings):
    """Run the complete agent pipeline."""
    from utils.logger import create_session_logger
    
    logger = create_session_logger()
    trace = []
    
    try:
        # Initialize components with explicit error handling
        retriever = None
        try:
            from rag.retriever import RAGRetriever
            # Create new retriever instance to avoid caching issues
            retriever = RAGRetriever()
            print(f"[DEBUG] Retriever loaded with {retriever.index.ntotal} vectors")
        except Exception as e:
            print(f"[DEBUG] RAG initialization failed: {str(e)}")
            import traceback
            traceback.print_exc()
            trace.append({"agent": "RAG", "status": "⚠️ warning", "message": f"RAG not available: {str(e)}"})
        
        memory_store = None
        try:
            from memory.memory_store import get_memory_store
            memory_store = get_memory_store()
        except Exception:
            pass
        
        
        # 1. Parser Agent
        from agents.parser_agent import ParserAgent
        parser = ParserAgent(logger=logger)
        parser_result = parser.parse({
            "raw_text": problem_text,
            "source": source
        })
        
        trace.append({
            "agent": "Parser",
            "status": "✓ completed",
            "message": f"Detected: {parser_result.get('topic')}, Variables: {parser_result.get('variables')}"
        })
        
        # Check for HITL
        if parser_result.get("needs_clarification"):
            return {
                "hitl_required": True,
                "hitl_question": parser_result.get("clarification_question"),
                "trace": trace
            }
        
        # 2. Router Agent
        from agents.router_agent import RouterAgent
        router = RouterAgent(logger=logger)
        router_result = router.route(parser_result)
        
        trace.append({
            "agent": "Router",
            "status": "✓ completed",
            "message": f"Route: {router_result.get('route')}, RAG: {router_result.get('use_rag')}"
        })
        
        # 3. Solver Agent
        from agents.solver_agent import SolverAgent
        solver = SolverAgent(retriever=retriever, memory_store=memory_store, logger=logger)
        
        # Check memory for similar problems
        memory_hits = []
        if memory_store:
            try:
                memory_hits = memory_store.find_similar(
                    problem_text,
                    topic=parser_result.get("topic"),
                    threshold=0.85
                )
            except Exception:
                pass
        
        solver_result = solver.solve(
            problem_text=parser_result.get("problem_text", problem_text),
            topic=parser_result.get("topic", "general"),
            retrieval_filters=router_result.get("retrieval_filters", []),
            use_python_tool=router_result.get("use_python_tool", False),
            memory_hits=memory_hits,
            variables=parser_result.get("variables"),
            constraints=parser_result.get("constraints")
        )
        
        trace.append({
            "agent": "Solver",
            "status": "✓ completed",
            "message": f"Used {len(solver_result.get('used_rag_chunks', []))} RAG chunks"
        })
        
        # 4. Verifier Agent
        from agents.verifier_agent import VerifierAgent
        verifier = VerifierAgent(logger=logger)
        verifier_result = verifier.verify(
            problem_text=parser_result.get("problem_text", problem_text),
            solution=solver_result.get("solution", ""),
            reasoning_steps=solver_result.get("reasoning_steps", []),
            topic=parser_result.get("topic", "general"),
            constraints=parser_result.get("constraints"),
            solver_confidence=solver_result.get("confidence", 0.7)
        )
        
        trace.append({
            "agent": "Verifier",
            "status": "✓ completed" if verifier_result.get("verdict") == "pass" else "⚠️ uncertain",
            "message": f"Verdict: {verifier_result.get('verdict')}, Confidence: {verifier_result.get('confidence', 0):.0%}"
        })
        
        # Check for HITL
        if verifier_result.get("needs_hitl"):
            trace.append({
                "agent": "Verifier",
                "status": "⚡ HITL",
                "message": verifier_result.get("hitl_question", "Review required")
            })
        
        # 5. Explainer Agent
        from agents.explainer_agent import ExplainerAgent
        explainer = ExplainerAgent(logger=logger)
        explainer_result = explainer.explain(
            problem_text=parser_result.get("problem_text", problem_text),
            solution=solver_result.get("solution", ""),
            reasoning_steps=solver_result.get("reasoning_steps", []),
            topic=parser_result.get("topic", "general"),
            used_rag_chunks=solver_result.get("used_rag_chunks"),
            difficulty_level=router_result.get("expected_difficulty", "JEE-intermediate")
        )
        
        trace.append({
            "agent": "Explainer",
            "status": "✓ completed",
            "message": f"Generated {len(explainer_result.get('steps', []))} steps explanation"
        })
        
        # Store in memory
        problem_id = None
        if memory_store:
            try:
                problem_id = memory_store.store_problem(
                    input_type=source,
                    original_input=problem_text,
                    parsed_problem=parser_result,
                    topic=parser_result.get("topic", "general"),
                    retrieved_chunks=solver_result.get("used_rag_chunks", []),
                    final_answer=solver_result.get("solution", ""),
                    reasoning_steps=solver_result.get("reasoning_steps", []),
                    verifier_confidence=verifier_result.get("confidence", 0.7)
                )
            except Exception:
                pass
        
        return {
            "success": True,
            "trace": trace,
            "parser": parser_result,
            "router": router_result,
            "solver": solver_result,
            "verifier": verifier_result,
            "explainer": explainer_result,
            "problem_id": problem_id
        }
        
    except Exception as e:
        trace.append({
            "agent": "Pipeline",
            "status": "✗ failed",
            "message": str(e)
        })
        return {
            "success": False,
            "trace": trace,
            "error": str(e)
        }


def render_agent_trace(trace):
    """Render the agent execution trace."""
    st.markdown("### 🤖 Agent Execution Trace")
    
    for item in trace:
        status_color = "green" if "✓" in item["status"] else "orange" if "⚠" in item["status"] else "red"
        st.markdown(f"""
        <div class="agent-trace">
            <strong style="color: {status_color}">{item['status']}</strong> <strong>{item['agent']}</strong>: {item['message']}
        </div>
        """, unsafe_allow_html=True)


def render_retrieved_chunks(chunks):
    """Render retrieved RAG chunks."""
    if not chunks:
        return
    
    st.markdown("### 📚 Retrieved Context")
    
    with st.expander("View knowledge chunks used", expanded=False):
        for i, chunk in enumerate(chunks, 1):
            st.markdown(f"""
            <div class="citation-box">
                <strong>{i}. {chunk}</strong>
            </div>
            """, unsafe_allow_html=True)


def render_solution(result):
    """Render the solution with explanation."""
    explainer = result.get("explainer", {})
    verifier = result.get("verifier", {})
    
    # Confidence gauge
    confidence = verifier.get("confidence", 0.7)
    if confidence >= 0.8:
        conf_color = "confidence-high"
        conf_text = "High"
    elif confidence >= 0.6:
        conf_color = "confidence-medium"
        conf_text = "Medium"
    else:
        conf_color = "confidence-low"
        conf_text = "Low"
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### ✨ Solution")
    
    with col2:
        st.markdown(f"""
        <div style="text-align: right;">
            <span class="{conf_color}" style="font-size: 1.2rem; font-weight: bold;">
                {confidence:.0%} {conf_text}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Main explanation
    if explainer.get("final_explanation"):
        st.markdown(explainer["final_explanation"])
    else:
        # Fallback
        st.markdown(f"**Answer:** {result.get('solver', {}).get('solution', 'N/A')}")
    
    # Key concepts
    if explainer.get("key_concepts"):
        st.markdown("### 📚 Key Concepts")
        for concept in explainer["key_concepts"]:
            st.markdown(f"• {concept}")
    
    # Exam tips
    if explainer.get("exam_tips"):
        st.markdown("### 💡 JEE Exam Tips")
        for tip in explainer["exam_tips"]:
            st.markdown(f"• {tip}")


def render_feedback_section(problem_id):
    """Render the feedback section."""
    st.markdown("### 💬 Feedback")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("✅ Correct", use_container_width=True):
            if problem_id:
                try:
                    from memory.memory_store import get_memory_store
                    store = get_memory_store()
                    store.update_feedback(problem_id, "correct")
                    st.success("Thanks for your feedback!")
                except Exception:
                    pass
    
    with col2:
        if st.button("❌ Incorrect", use_container_width=True):
            st.session_state.show_correction = True
    
    if st.session_state.get("show_correction"):
        with col3:
            correction = st.text_input("Please provide the correct answer:")
            if st.button("Submit Correction"):
                if problem_id and correction:
                    try:
                        from memory.memory_store import get_memory_store
                        store = get_memory_store()
                        store.update_feedback(problem_id, "incorrect", correction)
                        st.success("Thanks! We'll learn from this.")
                        st.session_state.show_correction = False
                    except Exception:
                        pass


def main():
    """Main application entry point."""
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">🧮 Math Mentor AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Intelligent JEE Mathematics Tutoring with RAG & Multi-Agent System</div>',
        unsafe_allow_html=True
    )
    
    # Sidebar
    settings = render_sidebar()
    
    # Main content
    col_main, col_trace = st.columns([2, 1])
    
    with col_main:
        # Input section
        input_data = render_input_section(settings)
        
        # Solve button
        if st.button("🚀 Solve Problem", type="primary", use_container_width=True):
            if input_data and input_data.get("content"):
                with st.spinner("Processing input..."):
                    # Process input
                    processed = process_input(input_data, settings)
                    
                    if processed:
                        # Show extracted text for review if needed
                        if processed.get("needs_human_review"):
                            st.warning(f"⚠️ Low confidence ({processed.get('confidence', 0):.0%}). Please verify:")
                            edited_text = st.text_area(
                                "Edit extracted text if needed:",
                                value=processed.get("clean_text", ""),
                                height=100
                            )
                            if st.button("Continue with edited text"):
                                processed["clean_text"] = edited_text
                        
                        problem_text = processed.get("clean_text", "")
                        source = processed.get("source", "text")
                        
                        if problem_text:
                            with st.spinner("Running agent pipeline..."):
                                result = run_agent_pipeline(problem_text, source, settings)
                                st.session_state.current_result = result
                                st.session_state.problem_solved = True
            else:
                st.warning("Please enter a problem to solve.")
        
        # Results section
        if st.session_state.problem_solved and st.session_state.current_result:
            result = st.session_state.current_result
            
            st.markdown("---")
            
            if result.get("hitl_required"):
                st.warning(f"🤔 **Clarification Needed:** {result.get('hitl_question')}")
            elif result.get("success"):
                render_solution(result)
                
                # Retrieved chunks
                chunks = result.get("solver", {}).get("used_rag_chunks", [])
                render_retrieved_chunks(chunks)
                
                st.markdown("---")
                
                # Feedback
                render_feedback_section(result.get("problem_id"))
            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    with col_trace:
        if st.session_state.current_result:
            render_agent_trace(st.session_state.current_result.get("trace", []))


if __name__ == "__main__":
    main()
