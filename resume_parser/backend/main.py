"""Main entry point for Uvicorn / Render deployments.
Re-exports the FastAPI app from app.main so that both `uvicorn main:app`
and `uvicorn app.main:app` work seamlessly.
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
