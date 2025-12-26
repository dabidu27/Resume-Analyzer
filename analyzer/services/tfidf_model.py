import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import re
import pickle

class TfidfModel:

    def __init__(self, csv=None):

        default_csv = Path(__file__).resolve().parents[2] / "job_title_des.csv"
        self.csv = Path(csv) if csv else default_csv
        self.df = None
        self.model = None
        self.tfidf_matrix = None
        self.job_descriptions = None
        
    def getJobDescriptions(self):

        self.df = pd.read_csv(self.csv)
        job_descriptions = self.df['Job Description'].tolist()
        return job_descriptions
    
    def cleanJobDescription(self, text):
        text = text.lower()

        text = re.sub(r'\S+@\S+', ' ', text)

        text = re.sub(r'http\S+|www\S+', ' ', text)

        boilerplate_patterns = [
            r'about us.*',
            r'about the company.*',
            r'who we are.*',
            r'what we offer.*',
            r'benefits.*',
            r'equal opportunity employer.*',
            r'we are an equal opportunity employer.*'
        ]
        for pattern in boilerplate_patterns:
            text = re.sub(pattern, ' ', text)

        hr_phrases = [
            r'you will be responsible for',
            r'responsibilities include',
            r'the ideal candidate',
            r'job responsibilities',
            r'requirements include'
        ]
        for phrase in hr_phrases:
            text = re.sub(phrase, ' ', text)

        text = re.sub(r'\b\d+\+?\s+years?\b', ' ', text)

        text = re.sub(r'\b(19|20)\d{2}\b', ' ', text)

        text = re.sub(r'[^a-z\s]', ' ', text)

        text = re.sub(r'\s+', ' ', text).strip()

        return text


    def train(self):

        raw_descriptions = self.getJobDescriptions()
        self.job_descriptions = [self.cleanJobDescription(job_description) for job_description in raw_descriptions]

        self.model = TfidfVectorizer(stop_words='english', max_df = 0.85, min_df = 2, ngram_range=(1,3))
        self.tfidf_matrix = self.model.fit_transform(self.job_descriptions)
    
    def extractKeywords(self, job_description, top_n = 10):

        clean_job_description = self.cleanJobDescription(job_description)
        vector = self.model.transform([clean_job_description])

        scores = vector.toarray()[0]
        features = self.model.get_feature_names_out()

        keywords_with_scores = list(zip(features, scores))
        keywords_with_scores = [(feature, score) for feature, score in keywords_with_scores if score > 0]
        keywords_with_scores.sort(key = lambda x: x[1], reverse = True)

        keywords = keywords_with_scores[:top_n]
        return keywords

if __name__ == "__main__":

    tfidf = TfidfModel()
    tfidf.train()

    model_path = Path(__file__).resolve().parent.parent / "models" / "tfidf_model.pkl"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(tfidf.model, f)
    




    