import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from keybert import KeyBERT
import pickle
from pathlib import Path
from analyzer.ml_models.label_model import LabelKeywords


class ResumeAnalyzerTool:

    def __init__(self, resume_text, job_text):

        self.resume_text = resume_text
        self.job_text = job_text
        self.nlp = spacy.load("en_core_web_sm")
        predictor_path = Path(__file__).resolve().parent.parent / "ml_models" / "skill_classifier.pkl"
        with open(predictor_path, 'rb') as f:

            model_dict = pickle.load(f)
            self.predictor_model = model_dict['model']
            self.label_encoder = model_dict['label_encoder']
            self.embedder = model_dict['embedder']

    def clean_text(self, text):

        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[()]', '', text)

        return text.strip()

    def extract_keywords(self, text):

        doc = self.nlp(text)

        terms = []
        generic = {"company", "people", "world", "opportunity", "culture", "team", "time", "process"}

        for token in doc:

            if token.pos_ in ['NOUN', 'PROPN']:

                if not token.is_stop and token.is_alpha and len(token) > 2 and token.text not in generic:

                        terms.append(token.lemma_.lower())
        
        for token in doc.ents:

            if token.label_ in ['SKILL', 'PRODUCT', 'TECHNOLOGY']:

                terms.append(token.text.lower())

        for chunk in doc.noun_chunks:

            lemmas = [token.lemma_ for token in chunk if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop and token.is_alpha]

            if len(lemmas) > 1:
                
                terms.append(" ".join(lemmas).lower())

        return terms

    def process_resume(self):

        self.resume_text = self.clean_text(self.resume_text)
        doc = self.nlp(self.resume_text)
        tokens = set()
        for token in doc:

            if len(token) > 2 and token.is_alpha and not token.is_stop:
                tokens.add(token.text.lower())

        return tokens

    def predict_skill(self, keyword):

        keyword_embedding = self.embedder.encode([keyword])
        proba = self.predictor_model.predict_proba(keyword_embedding)[0]
    
        if max(proba) < 0.80:
            return "Ambiguous"
        else:
            prediction = proba.argmax()
            return self.label_encoder.inverse_transform([prediction])[0]

    def analyze_resume(self):

        job_keywords = set(self.extract_keywords(self.job_text))
        
        resume_tokens = set(self.extract_keywords(self.resume_text))
        
        hard_skills = []
        for keyword in job_keywords:
            if self.predict_skill(keyword) == 'Hard Skill':
                hard_skills.append(keyword)
        
        print(hard_skills)
        matched_keywords = set()

        score = 0
        for keyword in resume_tokens:
            for hard_skill in hard_skills:
                if keyword in hard_skill:
                    matched_keywords.add(keyword)
                    score += 1

        print(f"{(len(matched_keywords)/len(hard_skills)) * 100}%")
        return score, list(matched_keywords)
