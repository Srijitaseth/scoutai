import re

MODEL_NAME = "all-MiniLM-L6-v2"
model = None


def _tokenize(text):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def _fallback_similarity(jd_text, resume_text):
    jd_tokens = _tokenize(jd_text)
    resume_tokens = _tokenize(resume_text)

    if not jd_tokens or not resume_tokens:
        return 0.0

    intersection = len(jd_tokens & resume_tokens)
    union = len(jd_tokens | resume_tokens)
    if union == 0:
        return 0.0

    return intersection / union


def get_model():
    global model

    if model is None:
        # Import lazily so deployments can run without the heavy embedding stack.
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(MODEL_NAME)

    return model


def calculate_semantic_similarity(jd_text, resume_text):
    try:
        embedding_model = get_model()
        jd_embedding = embedding_model.encode([jd_text])[0]
        resume_embedding = embedding_model.encode([resume_text])[0]

        jd_norm = float((jd_embedding ** 2).sum()) ** 0.5
        resume_norm = float((resume_embedding ** 2).sum()) ** 0.5
        if jd_norm == 0 or resume_norm == 0:
            similarity = 0.0
        else:
            similarity = float((jd_embedding * resume_embedding).sum()) / (jd_norm * resume_norm)
    except Exception:
        similarity = _fallback_similarity(jd_text, resume_text)

    similarity = max(0.0, min(1.0, similarity))

    return round(float(similarity) * 100, 2)
