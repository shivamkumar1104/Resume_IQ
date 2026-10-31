"""Universal Domain-Agnostic Skill Intelligence Engine."""

import re
from typing import List, Dict, Set, Tuple, Optional, Any
import spacy
from spacy.matcher import PhraseMatcher

# Canonical Skill Taxonomy & Aliases across Multi-Domains
CANONICAL_TAXONOMY = {
    # Software Engineering & Web
    "React.js": {"aliases": ["react", "reactjs", "react.js"], "category": "Frontend Framework"},
    "Next.js": {"aliases": ["nextjs", "next.js", "next"], "category": "Frontend Framework"},
    "TypeScript": {"aliases": ["ts", "typescript"], "category": "Programming Language"},
    "JavaScript": {"aliases": ["js", "javascript", "ecmascript"], "category": "Programming Language"},
    "Node.js": {"aliases": ["node", "nodejs", "node.js"], "category": "Backend Runtime"},
    "Express.js": {"aliases": ["express", "expressjs", "express.js"], "category": "Backend Framework"},
    "Python": {"aliases": ["python", "python3"], "category": "Programming Language"},
    "Java": {"aliases": ["java", "core java"], "category": "Programming Language"},
    "C++": {"aliases": ["c++", "cpp"], "category": "Programming Language"},
    "C#": {"aliases": ["c#", "csharp", ".net"], "category": "Programming Language"},
    "FastAPI": {"aliases": ["fastapi", "fast-api"], "category": "Backend Framework"},
    "Django": {"aliases": ["django", "drf", "django rest framework"], "category": "Backend Framework"},
    "REST APIs": {"aliases": ["rest", "restful", "rest api", "rest apis", "restful apis"], "category": "Architecture"},
    "GraphQL": {"aliases": ["graphql", "graph ql"], "category": "Architecture / API"},
    
    # Databases & Storage
    "PostgreSQL": {"aliases": ["postgres", "postgresql", "psql"], "category": "Database"},
    "MongoDB": {"aliases": ["mongodb", "mongo"], "category": "Database"},
    "MySQL": {"aliases": ["mysql"], "category": "Database"},
    "Redis": {"aliases": ["redis"], "category": "Database / Cache"},
    
    # DevOps, Cloud & Infrastructure
    "Docker": {"aliases": ["docker", "containerization", "containers"], "category": "DevOps"},
    "Kubernetes": {"aliases": ["kubernetes", "k8s"], "category": "Cloud / Orchestration"},
    "AWS": {"aliases": ["aws", "amazon web services", "ec2", "s3", "lambda"], "category": "Cloud Computing"},
    "Google Cloud Platform": {"aliases": ["gcp", "google cloud", "google cloud platform"], "category": "Cloud Computing"},
    "Azure": {"aliases": ["azure", "microsoft azure"], "category": "Cloud Computing"},
    "Terraform": {"aliases": ["terraform", "iac"], "category": "DevOps / Infrastructure"},
    "CI/CD": {"aliases": ["ci/cd", "continuous integration", "github actions", "jenkins", "gitlab ci"], "category": "DevOps"},
    "Git": {"aliases": ["git", "github", "gitlab"], "category": "Version Control"},
    
    # Data Science & AI / ML
    "Machine Learning": {"aliases": ["machine learning", "ml", "predictive modeling"], "category": "AI / ML"},
    "Deep Learning": {"aliases": ["deep learning", "dl", "neural networks"], "category": "AI / ML"},
    "Natural Language Processing": {"aliases": ["natural language processing", "nlp", "text processing"], "category": "AI / ML"},
    "Large Language Models": {"aliases": ["llm", "llms", "large language models", "generative ai", "genai"], "category": "AI / ML"},
    "PyTorch": {"aliases": ["pytorch", "torch"], "category": "ML Framework"},
    "TensorFlow": {"aliases": ["tensorflow", "tf", "keras"], "category": "ML Framework"},
    "Scikit-Learn": {"aliases": ["scikit-learn", "sklearn"], "category": "ML Framework"},
    "Pandas": {"aliases": ["pandas"], "category": "Data Analysis"},
    "NumPy": {"aliases": ["numpy"], "category": "Scientific Computing"},
    
    # Design / Product
    "Figma": {"aliases": ["figma"], "category": "Product Design"},
    "UI/UX Design": {"aliases": ["ui/ux", "ui design", "ux design", "user experience", "user interface", "wireframing"], "category": "Design"},
    
    # Mechanical & Engineering
    "AutoCAD": {"aliases": ["autocad", "cad"], "category": "Engineering CAD"},
    "SolidWorks": {"aliases": ["solidworks"], "category": "Engineering CAD"},
    "ANSYS": {"aliases": ["ansys", "finite element analysis", "fea"], "category": "Engineering Simulation"},
    
    # Healthcare & Biotech
    "CRISPR": {"aliases": ["crispr", "crispr-cas9"], "category": "Biotechnology"},
    "Genomics": {"aliases": ["genomics", "bioinformatics", "rna sequencing", "next-generation sequencing"], "category": "Life Sciences"}
}

# Pre-compile alias lookup
ALIAS_TO_CANONICAL: Dict[str, str] = {}
for canonical, data in CANONICAL_TAXONOMY.items():
    ALIAS_TO_CANONICAL[canonical.lower()] = canonical
    for alias in data["aliases"]:
        ALIAS_TO_CANONICAL[alias.lower()] = canonical


class UniversalSkillEngine:
    """Extracts, normalizes, categorizes, and grounds skills with sentence-level evidence."""

    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            self.nlp = spacy.blank("en")
            if "sentencizer" not in self.nlp.pipe_names:
                try:
                    self.nlp.add_pipe("sentencizer")
                except Exception:
                    pass
            
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        # Register all known aliases in PhraseMatcher
        patterns = [self.nlp.make_doc(alias) for alias in ALIAS_TO_CANONICAL.keys()]
        self.matcher.add("CANONICAL_SKILLS", patterns)

    def extract_skills_with_evidence(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract canonical skills along with confidence and sentence-level evidence.
        """
        if not text:
            return []

        doc = self.nlp(text)
        matches = self.matcher(doc)

        found_skills: Dict[str, Dict[str, Any]] = {}

        # 1. Match dictionary & alias skills
        for match_id, start, end in matches:
            span_text = doc[start:end].text.strip().lower()
            canonical = ALIAS_TO_CANONICAL.get(span_text, span_text.title())
            
            # Find the enclosing sentence for grounded evidence
            try:
                sentence = doc[start:end].sent.text.strip()
            except Exception:
                sentence = doc[max(0, start-10):min(len(doc), end+10)].text.strip()
            
            category = CANONICAL_TAXONOMY.get(canonical, {}).get("category", "General Technical")
            
            if canonical not in found_skills:
                found_skills[canonical] = {
                    "skill": canonical,
                    "category": category,
                    "confidence": 0.95,
                    "evidence": sentence
                }

        # 2. Dynamic Unknown Technical Term Discovery via Noun Chunks / Proper Nouns (open-ended)
        chunks = []
        if self.nlp.has_pipe("parser"):
            try:
                chunks = list(doc.noun_chunks)
            except Exception:
                chunks = []

        for chunk in chunks:
            chunk_str = chunk.text.strip()
            chunk_lower = chunk_str.lower()
            # If multi-word capitalized or technical candidate not yet matched
            if (len(chunk_str.split()) in (1, 2) and 
                chunk_str[0].isupper() and 
                len(chunk_str) > 2 and 
                chunk_lower not in ALIAS_TO_CANONICAL):
                
                # Check if it looks like a technology / framework / skill term
                if not any(token.is_stop or token.is_punct for token in chunk):
                    # Add as open-ended discovered skill
                    candidate_name = chunk_str.title()
                    if candidate_name not in found_skills and len(candidate_name) < 25:
                        try:
                            sent_text = chunk.sent.text.strip()
                        except Exception:
                            sent_text = chunk_str
                        found_skills[candidate_name] = {
                            "skill": candidate_name,
                            "category": "Domain Specific / Discovered",
                            "confidence": 0.82,
                            "evidence": sent_text
                        }

        return list(found_skills.values())
