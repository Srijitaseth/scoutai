from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "all-MiniLM-L6-v2"
model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer(MODEL_NAME)

    return model


def calculate_semantic_similarity(jd_text, resume_text):
    embedding_model = get_model()
    jd_embedding = embedding_model.encode([jd_text])
    resume_embedding = embedding_model.encode([resume_text])

    similarity = cosine_similarity(jd_embedding, resume_embedding)[0][0]

    return round(float(similarity) * 100, 2)
