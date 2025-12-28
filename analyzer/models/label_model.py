import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from pathlib import Path
import pickle


class LabelKeywords:

    def __init__(self, csv: str | Path = None):

        if csv is None:
            csv = Path(__file__).resolve().parent / "skills_index_final.csv"
        self.df = pd.read_csv(csv)
        self.X = None
        self.y = None
        self.y_test = None
        self.X_test = None
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.label_encoder = LabelEncoder()
        self.model = LogisticRegression(max_iter = 1000)

    def get_X_y(self):

        self.X = self.embedder.encode(self.df['Skill'].tolist())
        
        self.y = self.label_encoder.fit_transform(self.df['Type of Skill'].values)

    def train(self):
        
        X_train, self.X_test, y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42, stratify=self.y)
        self.model.fit(X_train, y_train)
    
    def evaluate(self):

        y_pred = self.model.predict(self.X_test)
        return accuracy_score(self.y_test, y_pred), classification_report(self.y_test, y_pred)

    def predict(self, keyword):

        keyword_embedding = self.embedder.encode([keyword])

        proba = self.model.predict_proba(keyword_embedding)[0]
        if max(proba) < 0.85:
            return "Ambiguous"
        else:
            label = self.label_encoder.inverse_transform([proba.argmax()])[0]
            return label

if __name__ == "__main__":


    model = LabelKeywords()
    model.get_X_y()
    model.train()
    with open("skill_classifier.pkl", "wb") as f:
        pickle.dump(model, f)
    