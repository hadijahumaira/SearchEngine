from flask import Flask, request, render_template
import os
import pandas as pd

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


# Fungsi untuk menghitung Jaccard Similarity
def jaccard_similarity(query, document):
    query_tokens = set(query.lower().split())
    document_tokens = set(document.lower().split())
    intersection = len(query_tokens.intersection(document_tokens))
    union = len(query_tokens) + len(document_tokens) - intersection
    return intersection / union


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_word = request.form['search_word']
        similar_documents = []

        for i, document in enumerate(df['dokumen']):
            similarity = jaccard_similarity(search_word, document)
            if similarity > 0:
                similar_documents.append((df['nama_dokumen'][i], similarity))

        similar_documents.sort(key=lambda x: x[1], reverse=True)

        return render_template('results2.html', search_word=search_word, similar_documents=similar_documents)

    return render_template('search.html')


if __name__ == '__main__':
    app.run()
