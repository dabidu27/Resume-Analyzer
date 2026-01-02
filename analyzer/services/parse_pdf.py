from PyPDF2 import PdfReader


class PdfParser:

    def __init__(self, file):
        self.file = file

    def extract_text(self):

        self.file.seek(0)

        reader = PdfReader(self.file)
        text = ""

        for page in reader.pages:

            text += page.extract_text() or ""

        self.file.seek(0)

        return text.strip()
