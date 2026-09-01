# Resume Intelligence Platform

An enterprise-grade AI hiring platform that elevates resume parsing from a basic keyword-matching script into an intelligent talent evaluation engine.

## Prerequisites
- Node.js (v18+)
- Python 3.9+

## 1. Start the Backend (FastAPI)

```bash
cd backend
# Create virtual environment (optional but recommended)
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm

uvicorn app.main:app --reload
```
The backend will run on `http://localhost:8000`.
API docs are at `http://localhost:8000/api/docs`.

## 2. Start the Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```
The frontend will run on `http://localhost:5173`. Open it in your browser to try the app.
