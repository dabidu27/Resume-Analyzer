import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer

class ResumeAnalyzerTool:

    def __init__(self, resume_text, job_text):

        self.resume_text = resume_text
        self.job_text = job_text
        self.nlp = spacy.load("en_core_web_sm")

    def clean_text(self, text):

        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[()]', '', text)
        text = text.strip()

        return text.strip()

    def process_job_description(self):

        self.job_text = self.clean_text(self.job_text)
        doc = self.nlp(self.job_text)

        terms = []

        for token in doc:

            if token.pos_ in ['NOUN', 'PROPN']:

                if not token.is_stop and token.is_alpha and len(token) > 2:

                        terms.append(token.lemma_.lower())

        for chunk in doc.noun_chunks:

            lemmas = [token.lemma_ for token in chunk if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop and token.is_alpha]

            if len(lemmas) > 1:
                
                terms.append(" ".join(lemmas))

        return terms
    
    def rank_job_keywords(self):

        terms = self.process_job_description()

        vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=1)

        tfidf = vectorizer.fit_transform([" ". join(terms)])

        scores = zip(vectorizer.get_feature_names_out(), tfidf.toarray()[0])

        ranked = sorted(scores, key = lambda x: x[1], reverse = True)

        ranked = ranked[:20]

        keywords = [tpl[0] for tpl in ranked]
        return keywords

    
    def process_resume(self):

        self.resume_text = self.clean_text(self.resume_text)
        doc = self.nlp(self.resume_text)

        terms = []

        for token in doc:

            if token.pos_ in ['NOUN', 'PROPN']:

                if not token.is_stop and token.is_alpha and len(token) > 2:

                        terms.append(token.lemma_.lower())

        for chunk in doc.noun_chunks:

            lemmas = [token.lemma_ for token in chunk if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop and token.is_alpha]

            if len(lemmas) > 1:
                
                terms.append(" ".join(lemmas))

        return terms


    def analyze_resume(self):

        job_keywords = self.rank_job_keywords()
        resume_tokens = self.process_resume()

        print(job_keywords)
        print(resume_tokens)
        
        matched_keywords = []

        score = 0
        for keyword in resume_tokens:
            if keyword in job_keywords:
                score += 1
                matched_keywords.append(keyword)

        print(f"{(len(matched_keywords)/len(job_keywords)) * 100}%")
        return score, matched_keywords
