import pdfplumber

def extract_text_from_pdf(pdf_file) -> str:
    extracted_text = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text(layout = True)
            if text:
                extracted_text.append(text)
    return "\n".join(extracted_text)

