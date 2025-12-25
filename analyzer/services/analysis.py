import spacy

class ResumeAnalyzerTool:


    def __init__(self, resume_text, job_text):

        self.resume_text = resume_text
        self.job_text = job_text

    def process_job_description(self):

        nlp = spacy.load("en_core_web_sm")

        doc = nlp(self.job_text)

        keywords = set()

        for token in doc:

            if token.pos_ in ['NOUN', 'VERB', 'PROPN']:

                if not token.is_stop and token.is_alpha:
                    keywords.add(token.lemma_.lower())

        for chunk in doc.noun_chunks:

            keywords.add(chunk.text.lower())
        
        return keywords
    
    def process_resume(self):

        nlp = spacy.load("en_core_web_sm")

        doc = nlp(self.resume_text)

        keywords = set()

        for token in doc:

            if token.pos_ in ['NOUN', 'VERB', 'PROPN']:

                if not token.is_stop and token.is_alpha:
                    keywords.add(token.lemma_.lower())

        for chunk in doc.noun_chunks:

            keywords.add(chunk.text.lower())
        
        return keywords


    def analyze_resume(self):

        job_keywords = self.process_job_description()
        resume_keywords = self.process_resume()

        print(job_keywords)
        print(resume_keywords)

        matched_keywords = []

        score = 0
        for keyword in resume_keywords:
            if keyword in job_keywords:
                score += 1
                matched_keywords.append(keyword)

        return score, matched_keywords