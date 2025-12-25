from PyPDF2 import PdfReader


def extract_text(file):

    file.seek(0)

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:

        text += page.extract_text() or ""

    file.seek(0)
    
    return text.strip()