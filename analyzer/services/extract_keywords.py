import pickle
from pathlib import Path
from analyzer.services.tfidf_model import TfidfModel
import pytextrank
import spacy
from sentence_transformers import SentenceTransformer
from analyzer.models.label_model import LabelKeywords

def clean(text):
    
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    terms = []
    generic = {"company", "people", "world", "opportunity", "culture", "team", "time", "process"}

    for token in doc:

            if token.pos_ in ['NOUN', 'PROPN']:

                if not token.is_stop and token.is_alpha and len(token) > 2 and token.text not in generic:

                        terms.append(token.lemma_)
            
    for token in doc.ents:

            if token.label_ in ['SKILL', 'PRODUCT', 'TECHNOLOGY']:

                terms.append(token.text)

    for chunk in doc.noun_chunks:

        lemmas = [token.lemma_ for token in chunk if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop and token.is_alpha]

        if len(lemmas) > 1:
                    
            terms.append(" ".join(lemmas))

    return terms

if __name__ == "__main__":

    predictor_path = Path(__file__).resolve().parent.parent / "models" / "skill_classifier.pkl"

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

keywords = clean(job_description)

with open(predictor_path, 'rb') as f:
     predictor_model = pickle.load(f)

hard_skills = []
soft_skills = []
ambiguous = []

for keyword in keywords:
    
    keyword_label = predictor_model.predict(keyword)
    if keyword_label == 'Hard Skill':
         hard_skills.append(keyword)
    elif keyword_label == 'Soft Skill':
         soft_skills.append(keyword)
    elif keyword_label == 'Ambiguous':
        ambiguous.append(keyword)

print(soft_skills)
print(hard_skills)
print(ambiguous)
