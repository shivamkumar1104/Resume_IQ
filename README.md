# Resume Intelligence Platform (ResumeIQ) v3.0

An enterprise-grade AI candidate screening and talent evaluation engine featuring universal skill intelligence, ATS diagnostics, explainable fit scoring, and company template recommendations.

---

## 📁 Project Structure

```
resume_parser/
├── render.yaml                          # Render 1-click Blueprint deployment file
├── .gitignore                           # Git ignore rules for node_modules, venv, pycache
├── docs/                                # Architecture specifications & blueprint documentation
└── resume_parser/
    ├── backend/                         # FastAPI Python backend
    │   ├── app/
    │   │   ├── main.py                  # FastAPI application with CORS & lifespan
    │   │   ├── services/
    │   │   │   ├── ats_engine.py        # 7-point ATS compliance diagnostics
    │   │   │   ├── ingester.py          # PDF / DOCX text extraction
    │   │   │   ├── optimizer.py         # Grounded Google X-Y-Z improvement tips
    │   │   │   ├── parser.py            # Contact & structural entity extractor
    │   │   │   ├── scorer.py            # Blueprint-weighted fit formula
    │   │   │   ├── semantic_engine.py   # Semantic similarity (ST / TF-IDF)
    │   │   │   ├── skill_engine.py      # Universal skill intelligence engine
    │   │   │   └── template_engine.py   # Company resume template matching
    │   │   └── schemas/                 # Pydantic request/response schemas
    │   ├── main.py                      # Uvicorn entry point
    │   └── requirements.txt             # Python dependencies
    └── frontend/                        # React (Vite + TailwindCSS)
        ├── src/
        │   ├── components/              # UI components & dashboard
        │   ├── hooks/                   # useScreening custom hook
        │   └── utils/api.js             # API client
        └── package.json                 # Frontend dependencies
```

---

## 🚀 Local Development

### 1. Backend Setup (FastAPI)

```bash
cd resume_parser/backend

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies and spaCy language model
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- API Root: `http://localhost:8000`
- Interactive Swagger Docs: `http://localhost:8000/api/docs`
- Health check: `http://localhost:8000/api/health`

### 2. Frontend Setup (React + Vite)

```bash
cd resume_parser/frontend
npm install
npm run dev
```
- Frontend application runs on: `http://localhost:5173`

---

## 🌐 Deployment to Render

### Option A: 1-Click Blueprint (Recommended)
1. Push this repository to GitHub.
2. Log into [Render](https://render.com).
3. Click **New +** -> **Blueprint**.
4. Connect your GitHub repository.
5. Render will detect `render.yaml` and configure both the backend web service and the frontend static site automatically!
6. Click **Apply**.

---

### Option B: Manual Setup in Render Dashboard

#### Step 1: Deploy Backend Web Service
1. In Render, click **New +** -> **Web Service**.
2. Select your repository.
3. Configure settings:
   - **Name**: `resume-parser-backend`
   - **Language**: `Python 3`
   - **Root Directory**: `resume_parser/backend`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/api/health`
4. In **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.8`
   - `USE_SENTENCE_TRANSFORMERS`: `false` *(recommended for Render Free Tier 512MB RAM)*
   - `ALLOWED_ORIGINS`: `*`
5. Click **Create Web Service**. Note your backend URL (e.g. `https://resume-parser-backend.onrender.com`).

#### Step 2: Deploy Frontend Static Site
1. In Render, click **New +** -> **Static Site**.
2. Select your repository.
3. Configure settings:
   - **Name**: `resume-parser-frontend`
   - **Root Directory**: `resume_parser/frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Under **Redirects/Rewrites**:
   - Source: `/*`
   - Destination: `/index.html`
   - Action: `Rewrite`
5. Under **Environment Variables**, add:
   - `VITE_API_URL`: `https://your-backend-name.onrender.com` *(your Backend URL from Step 1)*
6. Click **Create Static Site**.

