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
    job_description = """The PYTHON DEVELOPER (F/M) internship is part of DIGITAL HUB ROMANIA - FINANCE / DIR.SYSTEMES D'INFORMATION ROUMANIE

Welcome to the FUTURE

Be the creator of your own story - Drive Your Future!

If you are currently looking for an internship position in the field of software development with Python, apply to this ad and leave us your contact details, and our recruiters will contact you when opportunities that match your profile arise!

Top 5 reasons to apply for a Drive Your Future Internship position within Renault Group Romania:

You become a #CoolAutoMaker, like all of us. You will be part of the team that writes the history of mobility worldwide, from here, in Romania!
It is paid, of course. Moreover, the period in which you carry out the activity based on the internship contract is considered seniority;
Every day there is a mentor by your side, a person who will guide you and provide you with all the necessary support;
You will have access to our super learning resources – the Learning @ RenaultGroup platform; you will be able to take courses (technical and personal development) that will be useful for you in fulfilling your career plans.
Employment opportunity upon completion of the internship subject to the availability of vacancies.

Profile Sought

A technical profile, with a desire to explore and deepen through concrete, applied studies, concepts and methods in the area of ​​software development with Python.

So, whatever your profile, apply and be part of a passionate and constantly transforming industry, where every day brings new challenges and opportunities for professional and personal growth!

What Skills Will You Acquire After the Internship

Python Programming: language basics, data structures, OOP, best practices
Data manipulation and processing: using Pandas, NumPy, etc.
Database work: SQL/noSQL, connection and query
Application development: scripts, automation, mini-projects
Team collaboration, code versioning (Git), Agile methodologies
All applications will be considered regardless of nationality, gender, disability, age, race, color, religion, pregnancy status, gender identity or sexual orientation."""

    keywords = tfidf.extractKeywords(job_description)
    print(keywords)
    




    