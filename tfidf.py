import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

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

# Membuat TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Menghitung TF-IDF dari dokumen
tfidf = vectorizer.fit_transform(df['dokumen'])

# Mencari kata dalam dokumen
search_word = 'jerawat'
search_word_index = vectorizer.vocabulary_.get(
    search_word, -1)  # Periksa jika kata ada dalam vocabulary
if search_word_index != -1:
    search_word_tfidf = tfidf[:, search_word_index]

    # Menggunakan numpy untuk mendapatkan indeks dokumen yang mengandung kata tersebut
    relevant_document_indices = np.nonzero(search_word_tfidf)[0]

    # Menampilkan hasil pencarian
    print(f"Kata '{search_word}' ditemukan dalam dokumen berikut:")
    for index in relevant_document_indices:
        print(df['nama_dokumen'][index])
else:
    print(f'Kata "{search_word}" tidak ditemukan dalam dokumen.')
