from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(jd_text, resume_text):
    jd_embedding = model.encode([jd_text])
    resume_embedding = model.encode([resume_text])

    similarity = cosine_similarity(jd_embedding, resume_embedding)[0][0]

    return round(float(similarity) * 100, 2)