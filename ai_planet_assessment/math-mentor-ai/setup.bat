@echo off
echo ============================================
echo Math Mentor AI - Setup Script
echo ============================================

echo.
echo Step 1: Activating virtual environment...
call math\Scripts\activate.bat

echo.
echo Step 2: Installing core dependencies...
pip install streamlit google-generativeai sentence-transformers faiss-cpu pillow python-dotenv numpy

echo.
echo Step 3: Building RAG index...
python -m rag.build_index

echo.
echo ============================================
echo Setup complete!
echo Run: streamlit run app.py
echo ============================================
pause
