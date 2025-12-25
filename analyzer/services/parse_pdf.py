from PyPDF2 import PdfReader

class PdfParser:

    def __init__(self, file):
        self.file = file
        
    def extract_text(self, file):

        file.seek(0)

        reader = PdfReader(file)
        text = ""

        for page in reader.pages:

            text += page.extract_text() or ""

        file.seek(0)
        
        return text.strip()