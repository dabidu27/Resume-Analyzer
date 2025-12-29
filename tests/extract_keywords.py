import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pickle
from analyzer.services.tfidf_model import TfidfModel
import pytextrank
import spacy
from sentence_transformers import SentenceTransformer
from analyzer.ml_models.label_model import LabelKeywords

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

    return set(terms)

if __name__ == "__main__":

    predictor_path = Path(__file__).resolve().parent.parent / "analyzer" / "ml_models" / "skill_classifier.pkl"

    job_description = """What You'll Do:

    Deliver features with needed quality & timelines
    Design features & solutions taking into account future usage & all other constraints
    Improve solution quality
    Provide estimations for features delivery with required accuracy
    Participate in design and code review
    Integrate with internal and external services
    Monitor efficiency and performance
    Support and develop multiple projects, depending on team
    Troubleshoot various project errors & issues
    When needed, write clear & cohesive technical specification
    Write automated tests to ensure high quality of work


Who You Are:

    2+ Years of experience
    Ability to work independently and dig into a problem
    Ability to work according to agreed deadlines
    Ability to write clear, self-documented code
    Basic data structures and algorithms, time-space complexity
    Basic Network understanding (HTTP - is a must)
    Decent Python 3 knowledge, core concepts and low-level implementation
    Good written communication skills in English
    Experience in developing REST APIs (Django, DRF, preferably)
    Experience in devising feature design, producing quality documentation & decomposition with estimation
    Experience using continuous integration and automation processes
    Experience with relational databases (preferably PostgreSQL)
    Experience with Unix systems
    Knowledge of design patterns & principles (OOP, SOLID)
    Passion for writing maintainable tests (unit, functional, end-to-end, mocks)


We acknowledge that many candidates may not meet every single role requirement listed above. If your experience looks a little different from our requirements but you believe that you can still bring value to the role, we’d love to see your application!

We acknowledge that many candidates may not meet every single role requirement listed above. If your experience looks a little different from our requirements but you believe that you can still bring value to the role, we’d love to see your application!

Who We Are:

Criteo is a leader in commerce media, helping brands, agencies, and publishers create meaningful consumer connections through AI-powered advertising solutions. We’re shaping a more open and sustainable digital future for advertising.

At Criteo, our culture is as unique as it is diverse. From our offices across the globe or from the comfort of home, our 3,600 Criteos collaborate together to build an open, impactful, and forward-thinking environment.

We foster a workplace where everyone is valued, and employment decisions are based solely on skills, qualifications, and business needs—never on non-job-related factors or legally protected characteristics.

What We Offer:

🏢 Ways of working – Our hybrid model blends home with in-office experiences, making space for both.

📈 Grow with us – Learning, mentorship & career development programs.

💪 Your wellbeing matters – Health benefits, wellness perks & mental health support.

🤝 A team that cares – Diverse, inclusive, and globally connected.

💸 Fair pay & perks – Attractive salary, with performance-based rewards and family-friendly policies, plus the potential for equity depending on role and level.

Additional benefits may vary depending on the country where you work and the nature of your employment with Criteo."""

keywords = clean(job_description)
print(f"\n=== EXTRACTED KEYWORDS ===\n{sorted(keywords)}\n")

with open(predictor_path, 'rb') as f:
     model_dict = pickle.load(f)
     predictor_model = model_dict['model']
     label_encoder = model_dict['label_encoder']
     embedder = model_dict['embedder']

hard_skills = []
soft_skills = []
ambiguous = []

for keyword in keywords:
    
    keyword_embedding = embedder.encode([keyword])
    proba = predictor_model.predict_proba(keyword_embedding)[0]
    #the prediction returns an array containing 2 numbers: probability of label being hard skill and probability of skill being soft skill
    prediction = proba.argmax() #returns the index of the number with the higher probability => 0 for hard skill, 1 for soft skill
    keyword_label = label_encoder.inverse_transform([prediction])[0] #converts 0 back to hard skill and 1 back to soft skill
    confidence = max(proba) #return the highest probability in the prediction array (not the index, as .argmax())
    if confidence < 0.65:
         keyword_label = 'ambiguous'
    #if prediction array is  proba = [0.85, 0.5] => proba.argmax() = 0 => confidence = max(proba) = 0.85

    print(f"{keyword:30} -> {keyword_label:15} (confidence: {confidence:.2f})")

    if keyword_label.lower() == 'hard skill':
         hard_skills.append(keyword)
    elif keyword_label.lower() == 'soft skill':
         soft_skills.append(keyword)
    elif keyword_label == 'ambiguous':
        ambiguous.append(keyword)

print(soft_skills)
print(hard_skills)
print(ambiguous)