import os
import pandas as pd
from rank_bm25 import BM25Okapi

# Menentukan direktori folder
folder = 'corpus2'

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

# Membangun indeks BM25
corpus = df['dokumen'].str.split()
bm25 = BM25Okapi(corpus)

# Mencari kata dalam dokumen dengan BM25
search_word = 'contoh'
query = search_word.split()
doc_scores = bm25.get_scores(query)

# Menampilkan hasil pencarian berdasarkan skor BM25 tertinggi
result_indices = doc_scores.argsort()[::-1]
print(f"Dokumen-dokumen yang relevan dengan kata '{search_word}':")
for index in result_indices:
    print(f"- {df['nama_dokumen'][index]} (BM25 Score: {doc_scores[index]:.2f})")
