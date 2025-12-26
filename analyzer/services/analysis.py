import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from keybert import KeyBERT


class ResumeAnalyzerTool:

    def __init__(self, resume_text, job_text):

        self.resume_text = resume_text
        self.job_text = job_text
        self.nlp = spacy.load("en_core_web_sm")

    def clean_text(self, text):

        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[()]', '', text)
        text = text.strip()
        text = text.lower()

        return text.strip()
    
    def extract_keywords_keybert(self):

        model = KeyBERT()
        
        keywords_with_scores = model.extract_keywords(
            self.job_text,
            keyphrase_ngram_range=(1, 3),
            stop_words='english',
            top_n=20, 
            use_mmr=True,
            diversity=0.7 
        )
        
        keywords = [kw for kw, score in keywords_with_scores]
        
        return keywords


    def extract_keywords_spacy(self):

        doc = self.nlp(self.job_text)

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

        freq = Counter(terms)

        keywords = [(term, count) for term, count in freq.most_common(20)]

        keywords = [kw for kw, count in keywords]

        return keywords
    
    def extract_requirements_patterns(self):
        """
        Extract specific patterns that indicate requirements
        Things like "5+ years", "Bachelor's degree", "Python required"
        """
        requirements = []
        text_lower = self.job_text.lower()
        
        # Pattern 1: Years of experience
        exp_patterns = [
            r'(\d+\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience)',
            r'(experience\s+of\s+\d+\+?\s*(?:years?|yrs?))',
        ]
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            requirements.extend(matches)
        
        # Pattern 2: Degree requirements
        degree_pattern = r"(bachelor'?s?|master'?s?|phd|doctorate)\s+(?:degree\s+)?(?:in\s+)?(\w+)?"
        degrees = re.findall(degree_pattern, text_lower, re.IGNORECASE)
        requirements.extend([' '.join(d).strip() for d in degrees])
        
        # Pattern 3: "Required" or "Must have"
        required_pattern = r'(?:required|must\s+have|essential):\s*([^\n.]+)'
        required_items = re.findall(required_pattern, text_lower, re.IGNORECASE)
        for item in required_items:
            # Split by commas or "and"
            items = re.split(r',|\s+and\s+', item)
            requirements.extend([i.strip() for i in items if len(i.strip()) > 2])
        
        # Pattern 4: Bullet points (often requirements)
        bullet_pattern = r'[•\-\*]\s*([^\n]+)'
        bullets = re.findall(bullet_pattern, self.job_text)

        for b in bullets:

            b = b.lower().strip()
            if 1 <= len(b.split()) <= 6:
                requirements.append(b)
        
        print(requirements)
        return list(set(requirements))
    
    def extract_keywords_hybrid(self):

        self.job_text = self.clean_text(self.job_text)

        keywords_tfidf = self.extract_keywords_keybert()
        keywords_spacy = self.extract_keywords_spacy()
        keywords_requirements = self.extract_requirements_patterns()

        keywords = set()

        for keyword in keywords_tfidf:

            keywords.add(keyword)
        
        for keyword in keywords_spacy:

            keywords.add(keyword)

        for keyword in keywords_requirements:

            keywords.add(keyword)

        return keywords

    def process_resume(self):


        self.resume_text = self.clean_text(self.resume_text)
        doc = self.nlp(self.resume_text)
        tokens = set()
        for token in doc:

            if len(token) > 2 and token.is_alpha and not token.is_stop:
                tokens.add(token.text)

        return tokens


    def analyze_resume(self):

        job_keywords = self.extract_keywords_hybrid()
        resume_tokens = self.process_resume()
        
        matched_keywords = set()

        score = 0
        for keyword in resume_tokens:
            for job_keyword in job_keywords:
                if keyword in job_keyword:
                    matched_keywords.add(keyword)
                    score += 1

        print(f"{(len(matched_keywords)/len(job_keywords)) * 100}%")
        return score, list(matched_keywords)
