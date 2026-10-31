"""Semantic embedding and similarity calculation engine."""

import os
import numpy as np
from typing import Tuple, List, Optional
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class SemanticEngine:
    """Computes dense vector embeddings and semantic cosine similarity."""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SemanticEngine, cls).__new__(cls)
        return cls._instance

    def load_model(self):
        """Pre-load SentenceTransformer model into memory at server boot."""
        if self._model is None:
            use_st = os.getenv("USE_SENTENCE_TRANSFORMERS", "true").lower() in ("true", "1", "yes")
            if not use_st:
                self._model = "TFIDF_FALLBACK"
                return

            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            except Exception:
                self._model = "TFIDF_FALLBACK"

    def compute_similarity(self, resume_text: str, jd_text: str) -> float:
        """
        Calculate semantic similarity between resume and job description.
        Returns percentage float between 0.0 and 100.0.
        """
        if not resume_text.strip() or not jd_text.strip():
            return 0.0

        if self._model is None:
            self.load_model()

        if self._model != "TFIDF_FALLBACK" and self._model is not None:
            try:
                embeddings = self._model.encode([resume_text, jd_text], convert_to_numpy=True)
                sim = cosine_similarity(embeddings[0:1], embeddings[1:2])[0][0]
                # Normalize float between 0.0 and 1.0 -> 0-100%
                return round(float(np.clip(sim, 0.0, 1.0)) * 100, 2)
            except Exception:
                pass

        # TF-IDF Fallback
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(np.clip(sim, 0.0, 1.0)) * 100, 2)
