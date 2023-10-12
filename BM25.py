import re
import os
import pandas as pd
from flask import Flask, request, render_template
from rank_bm25 import BM25Okapi

app = Flask(__name__)

# Menentukan direktori folder
folder = 'corpus4'

# Membaca dokumen dan membuat DataFrame
files = os.listdir(folder)
paths = [os.path.join(folder, file) for file in files]
documents = []
document_names = []
for path in paths:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        documents.append(content)
        document_names.append(os.path.basename(path))

df = pd.DataFrame({'nama_dokumen': document_names, 'dokumen': documents})

# Membangun indeks BM25
corpus = df['dokumen'].str.split()
bm25 = BM25Okapi(corpus)

# Menampilkan hasil pencarian berdasarkan skor BM25 tertinggi
@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_word = request.form['search_word']
        query = search_word.split()
        doc_scores = bm25.get_scores(query)
        similar_documents = []
        result_indices = doc_scores.argsort()[::-1]

        for index in result_indices:
            if doc_scores[index] > 0:
                document_name = df['nama_dokumen'][index]
                bm25_score = doc_scores[index]
                link = f"https://www.viva.co.id/berita/nasional/{document_name.replace(' ', '_').replace('.txt', '')}"
                similar_documents.append((document_name, bm25_score, link))

        return render_template('results.html', search_word=search_word, similar_documents=similar_documents)

    return render_template('search.html')

if __name__ == '__main__':
    app.run()