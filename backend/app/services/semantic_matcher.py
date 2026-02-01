from typing import List, Dict
import torch

from ..models.embeddings import get_embedding_model


def semantic_match(
    resume_sentences: List[str],
    jd_sentences: List[str],
    threshold: float = 0.45
) -> Dict[str, object]:

    model = get_embedding_model()

    resume_emb = model.encode(resume_sentences, convert_to_tensor=True)
    jd_emb = model.encode(jd_sentences, convert_to_tensor=True)

    # Normalize embeddings
    resume_emb = torch.nn.functional.normalize(resume_emb, p=2, dim=1)
    jd_emb = torch.nn.functional.normalize(jd_emb, p=2, dim=1)

    similarity_matrix = torch.matmul(jd_emb, resume_emb.T)

    matches = []

    for i, jd_sentence in enumerate(jd_sentences):
        max_score = torch.max(similarity_matrix[i]).item()
        # print(f"\nJD: {jd_sentence}")
        # print(f"Max similarity: {round(max_score, 3)}")

        if max_score >= threshold:
            matches.append({
                "jd_sentence": jd_sentence,
                "similarity": round(max_score, 2)
            })

    score = round(len(matches) / len(jd_sentences), 2) if jd_sentences else 0.0

    return {
        "semantic_score": score,
        "matched_requirements": matches
    }
