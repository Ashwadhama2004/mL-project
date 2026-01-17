# Math Mentor AI

An intelligent math tutoring system for JEE-level problems with multimodal input, RAG-based knowledge retrieval, multi-agent orchestration, human-in-the-loop verification, and self-learning capabilities.

## 🎯 Features

- **Multimodal Input**: Upload images (OCR), record audio (ASR), or type text directly
- **Multi-Agent Architecture**: 5 specialized agents (Parser, Router, Solver, Verifier, Explainer)
- **RAG-Powered**: Grounded knowledge retrieval from comprehensive JEE math knowledge base
- **Human-in-the-Loop**: Intelligent checkpoints for low-confidence scenarios
- **Self-Learning**: Memory system that learns from user feedback without retraining
- **Transparent UI**: See agent traces, retrieved chunks, and confidence scores

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE (Streamlit)              │
└────────────┬─────────────────────────────────────┬──────────────┘
             │                                     │
             ▼                                     ▼
┌──────────────────────────┐            ┌──────────────────────┐
│  INPUT PROCESSING        │            │   MEMORY LAYER       │
│  - OCR (EasyOCR)         │            │   - SQLite Store     │
│  - ASR (Whisper)         │            │   - Feedback Log     │
│  - Text (direct)         │            └──────────────────────┘
└────────────┬─────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│               AGENT ORCHESTRATION LAYER                         │
│  Parser → Router → Solver → Verifier → Explainer               │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────┐
│      RAG LAYER           │
│  - Knowledge Base (17 docs)│
│  - FAISS Index           │
│  - Semantic Retriever    │
└──────────────────────────┘
```

## � Screenshots

### Homepage
![Math Mentor AI Homepage](docs/app_homepage.png)

### Solution with Step-by-Step Explanation
![Solution showing x=2 and x=3 for quadratic equation](docs/app_solution.png)

### Demo Video
![Application Demo](docs/demo.webp)


## �🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

### 3. Build Knowledge Base Index

```bash
python -m rag.build_index
```

### 4. Run the Application

```bash
streamlit run app.py
```

## 📁 Project Structure

```
math-mentor-ai/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── agents/                    # Multi-agent system
│   ├── parser_agent.py        # Input structuring
│   ├── router_agent.py        # Intent classification
│   ├── solver_agent.py        # RAG + tool solving
│   ├── verifier_agent.py      # Quality assurance
│   └── explainer_agent.py     # Pedagogical explanation
├── input_processors/          # Multimodal input
│   ├── ocr.py                 # EasyOCR wrapper
│   ├── asr.py                 # Whisper wrapper
│   └── text.py                # Text validator
├── rag/                       # RAG system
│   ├── build_index.py         # Index builder
│   ├── retriever.py           # Query interface
│   └── knowledge_base/        # 17 markdown docs
├── memory/                    # Self-learning system
│   └── memory_store.py        # SQLite operations
├── utils/                     # Utilities
│   ├── llm_client.py          # Gemini API client
│   ├── tools.py               # Python calculator
│   ├── confidence.py          # Scoring utilities
│   └── logger.py              # Structured logging
└── data/                      # Persistent storage
    ├── faiss_index/           # Vector embeddings
    └── memory_store.db        # Problem history
```

## 🔧 Configuration

Edit `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
MODEL_NAME=gemini-2.5-flash
```

## 📚 Knowledge Base Topics

- Algebra, Calculus, Trigonometry
- Probability, Statistics
- Linear Algebra, Matrices & Determinants
- Coordinate Geometry, Vectors & 3D
- Complex Numbers, Sequences & Series
- Differential Equations
- Binomial Theorem, Permutations & Combinations
- Common Mistakes, Problem Templates, JEE Tips

## 🎨 UI Features

- **Input Mode Selector**: Text / Image / Audio
- **Agent Trace Panel**: See which agents ran and what they did
- **Retrieved Context**: View knowledge chunks used
- **Confidence Gauge**: Visual confidence indicator
- **Feedback System**: Mark solutions correct/incorrect
- **HITL Prompts**: Intervention when confidence is low

## 📄 License

MIT License
