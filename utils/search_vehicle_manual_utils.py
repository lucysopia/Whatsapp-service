import json
import os

import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from settings import logger

model = SentenceTransformer("all-MiniLM-L6-v2")
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_encoded_pdf_manuals() -> list:
    with open(f"{path}/static/manual_chunks.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    manual_data = []
    for entry in raw_data:
        if "embedding" in entry:
            entry["embedding"] = np.array(entry["embedding"])
            manual_data.append(entry)

    return manual_data


def search_manual(query, model_name, top_k=3) -> list:
    data = get_encoded_pdf_manuals()
    query_vec =   model.encode(query)
    similarities = []
    try:
        for entry in data:
            if entry.get("model") == model_name:
                score = cosine_similarity([query_vec], [entry["embedding"]])[0][0]
                similarities.append((score, entry))

        similarities.sort(reverse=True, key=lambda x: x[0])
        top_matches = similarities[:top_k]

        results = []
        for score, entry in top_matches:
            snippet = entry["content"][:800]
            page = entry.get("page", "?")
            title = entry.get("title", "Untitled")
            source = entry.get("source", "Unknown Manual")
            results.append(
                f" *{source}*\n Page {page} - {title}\n\n{snippet.strip()}\n"
            )
    except Exception as e:
        logger.error(e)
        results = "No results found"
    return results
