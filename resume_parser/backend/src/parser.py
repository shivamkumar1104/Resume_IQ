import re
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

DEFAULT_SKILLS = [
    "Python", "Java", "C++", "SQL", "JavaScript", "React", "Node.js",
    "Machine Learning", "Deep Learning", "NLP", "PyTorch", "TensorFlow",
    "Scikit-Learn", "Pandas", "NumPy", "Docker", "Kubernetes", "AWS", "Git"
]
def extract_contact_info(text:str) -> dict:
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\(?\d{3}\)?[-\s.]\d{3}[-\s.]?\d{4}'

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    return {
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None
    }

def extract_skills(text: str, custom_skills_list: list = None) -> list:
    skills_to_search = custom_skills_list or DEFAULT_SKILLS
    matcher = PhraseMatcher(nlp.vocab, attr = "LOWER")

    patterns = [nlp.make_doc(skill) for skill in skills_to_search]
    matcher.add("SKILLS_PATTERNS", patterns)

    doc = nlp(text)
    matches = matcher(doc)

    extracted = set()
    for match_id, start, end in matches:
        extracted.add(doc[start:end].text.title())
    
    return list(extracted)
    