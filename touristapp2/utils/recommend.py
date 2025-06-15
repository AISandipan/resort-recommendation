import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Load CSV
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "resorts_data.csv")

df = pd.read_csv(file_path)
df.fillna("", inplace=True)

# Combine text for similarity
df["combined_text"] = df["Description"] + " " + df["Review Highlights"]

# TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["combined_text"])

# Cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_all_resorts():
    return df["Resort Name"].tolist()

def get_recommendations(resort_name, top_n=3):
    if resort_name not in df["Resort Name"].values:
        return []

    idx = df[df["Resort Name"] == resort_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    recommendations = []
    for i, score in sim_scores:
        rec = {
            "name": df.iloc[i]["Resort Name"],
            "region": df.iloc[i]["Region"],
            "rating": df.iloc[i]["Google Rating"],
            "description": df.iloc[i]["Description"],
            "highlights": df.iloc[i]["Review Highlights"],
            "similarity": round(score, 2)
        }
        recommendations.append(rec)

    return recommendations
