import os
import pandas as pd
import numpy as np

# Menentukan direktori folder
folder = 'corpus4'

# Membuat list nama file dalam folder
files = os.listdir(folder)

# Membuat list path file dalam folder
paths = [os.path.join(folder, file) for file in files]

# Membaca isi dokumen dan melacak nama dokumen
documents = []
document_names = []  # Menyimpan nama dokumen yang mengandung kata tertentu
for path in paths:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        documents.append(content)
        document_names.append(os.path.basename(path))

# Membuat dataframe dari dokumen
df = pd.DataFrame({'nama_dokumen': document_names, 'dokumen': documents})

# Fungsi untuk menghitung Jaccard Similarity


def jaccard_similarity(query, document):
    query_tokens = set(query.lower().split())
    document_tokens = set(document.lower().split())
    intersection = len(query_tokens.intersection(document_tokens))
    union = len(query_tokens) + len(document_tokens) - intersection
    return intersection / union


# Mencari kata dalam dokumen dengan Jaccard Similarity
search_word = 'bocah'
similar_documents = []

for i, document in enumerate(df['dokumen']):
    similarity = jaccard_similarity(search_word, document)
    if similarity > 0:  # Menambahkan dokumen yang memiliki similarity lebih dari 0
        similar_documents.append((df['nama_dokumen'][i], similarity))

# Menampilkan hasil pencarian berdasarkan similarity tertinggi
similar_documents.sort(key=lambda x: x[1], reverse=True)
print(f"Dokumen-dokumen yang mirip dengan kata '{search_word}':")
for doc_name, similarity in similar_documents:
    document_url = f"https://www.viva.co.id/berita/nasional/{doc_name.replace(' ', '_').replace('.txt', '')}"
    print(
        f"- <a href='{document_url}'>{doc_name}</a> (Similarity: {similarity})")
