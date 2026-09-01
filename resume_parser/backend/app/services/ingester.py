"""Document ingestion: extracts raw text from PDF and DOCX files."""

import io
from typing import Union


def extract_text_from_pdf(file_input: Union[bytes, object]) -> str:
    """Extract text from PDF bytes or file-like object using pdfplumber."""
    import pdfplumber
    extracted = []
    if isinstance(file_input, bytes):
        file_input = io.BytesIO(file_input)
    with pdfplumber.open(file_input) as pdf:
        for page in pdf.pages:
            text = page.extract_text(layout=True)
            if text:
                extracted.append(text)
    return "\n".join(extracted)


def extract_text_from_docx(file_input: Union[bytes, object]) -> str:
    """Extract text from DOCX bytes or file-like object using python-docx."""
    try:
        from docx import Document
    except ImportError:
        raise RuntimeError("python-docx is required for DOCX support. Run: pip install python-docx")
    if isinstance(file_input, bytes):
        file_input = io.BytesIO(file_input)
    doc = Document(file_input)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Dispatch text extraction based on file extension."""
    fname_lower = filename.lower()
    if fname_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif fname_lower.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {filename}. Only PDF and DOCX are supported.")
