import re
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text

def extract_keywords(text, top_n=5):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
    X = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out().tolist()
