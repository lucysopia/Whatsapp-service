# # This script processes various bus manuals in PDF format, extracting text, cleaning it,
# # chunking it by headers, and generating embeddings for each chunk using a pre-trained model.
# import os

# # PyMuPDF
# import re
# import pymupdf

# import json

# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("all-MiniLM-L6-v2")
# model = None


# def clean_text(text):
#     text = re.sub(r"\n+", "\n", text)
#     text = re.sub(r"\s{2,}", " ", text)
#     text = re.sub(r"Page\s*\d+", "", text, flags=re.IGNORECASE)
#     return text.strip()


# def chunk_text_by_headers(text):
#     lines = text.split("\n")
#     sections = []
#     current_title = "Introduction"
#     current_body = []

#     header_pattern = re.compile(r"^([A-Z][A-Z\s\d\-:]{3,}|[\d\.]{1,4}\s+[A-Z].*)$")

#     for line in lines:
#         if header_pattern.match(line.strip()):
#             if current_body:
#                 sections.append(
#                     (current_title.strip(), "\n".join(current_body).strip())
#                 )
#             current_title = line.strip()
#             current_body = []
#         else:
#             current_body.append(line)

#     if current_body:
#         sections.append((current_title.strip(), "\n".join(current_body).strip()))

#     return sections


# def preprocess_pdf(filepath):
#     doc = pymupdf.open(filepath)  # or open_pdf(filepath)
#     chunks = []

#     for i, page in enumerate(doc):
#         raw_text = page.get_text()
#         cleaned = clean_text(raw_text)
#         sections = chunk_text_by_headers(cleaned)

#         for title, content in sections:
#             text = content.strip()
#             if text:
#                 embedding = model.encode(text).tolist()
#                 bus_model = filepath.split("_")[0]
#                 chunks.append(
#                     {
#                         "page": i + 1,
#                         "title": title,
#                         "content": text,
#                         "embedding": embedding,
#                         "source": filepath,
#                         "model": bus_model,
#                     }
#                 )

#     return chunks


# def save_to_json(data, filename="manual_chunks.json"):
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)


# if __name__ == "__main__":
#     path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + "/static"
#     pdf_paths = [
#         f"{path}/BYD-K6_All_Systems_Service _Manual.pdf",
#         f"{path}/Zhongtong_Motor_User_Manual.pdf",
#         f"{path}/Kinglong_Air _Brake _System_Service_Manual.pdf",
#         f"{path}/Joylong_User_Manual.pdf",
#         f"{path}/Higer_All_parts_User_Manual.pdf",
#         f"{path}/BLK-E9_Air_Suspension_Maintenance_Manual.pdf",
#     ]

#     all_manual_data = []

#     for path in pdf_paths:
#         manual_data = preprocess_pdf(path)
#         all_manual_data.extend(manual_data)

#     save_to_json(all_manual_data)
#     print(
#         f"Processed and saved {len(all_manual_data)} chunks from {len(pdf_paths)} manuals."
#     )


# This script processes various bus manuals in PDF format, extracting text, cleaning it,
# chunking it by headers, and generating embeddings for each chunk using a pre-trained model.

import os
import re
import json
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def clean_text(text):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"Page\s*\d+", "", text, flags=re.IGNORECASE)
    return text.strip()

def chunk_text_by_headers(text):
    lines = text.split("\n")
    sections = []
    current_title = "Introduction"
    current_body = []

    header_pattern = re.compile(r"^([A-Z][A-Z\s\d\-:]{3,}|[\d\.]{1,4}\s+[A-Z].*)$")

    for line in lines:
        if header_pattern.match(line.strip()):
            if current_body:
                sections.append(
                    (current_title.strip(), "\n".join(current_body).strip())
                )
            current_title = line.strip()
            current_body = []
        else:
            current_body.append(line)

    if current_body:
        sections.append((current_title.strip(), "\n".join(current_body).strip()))

    return sections

def preprocess_pdf(filepath):
    doc = fitz.open(filepath)
    chunks = []
    filename = os.path.basename(filepath)
    bus_model = filename.split("_")[0]  # Extract model from filename

    for i, page in enumerate(doc):
        raw_text = page.get_text()
        cleaned = clean_text(raw_text)
        sections = chunk_text_by_headers(cleaned)

        for title, content in sections:
            text = content.strip()
            if text:
                embedding = model.encode(text).tolist()
                chunks.append(
                    {
                        "page": i + 1,
                        "title": title,
                        "content": text,
                        "embedding": embedding,
                        "source": filename,
                        "model": bus_model,
                    }
                )

    return chunks

def save_to_json(data, filename="manual_chunks.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
    pdf_paths = [
        f"{path}/BYD-K6_All_Systems_Service _Manual.pdf",
        f"{path}/Zhongtong_Motor_User_Manual.pdf",
        f"{path}/Kinglong_Air _Brake _System_Service_Manual.pdf",
        f"{path}/Joylong_User_Manual.pdf",
        f"{path}/Higer_All_parts_User_Manual.pdf",
        f"{path}/BLK-E9_Air_Suspension_Maintenance_Manual.pdf",
    ]

    all_manual_data = []

    for filepath in pdf_paths:
        manual_data = preprocess_pdf(filepath)
        all_manual_data.extend(manual_data)

    save_to_json(all_manual_data)
    print(f"✅ Processed and saved {len(all_manual_data)} chunks from {len(pdf_paths)} manuals.")
