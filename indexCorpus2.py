import os
import string
import nltk
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# nltk.download('punkt')
# nltk.download('stopwords')


def index_txt_files(input_folder, output_file, index_file):
    # Inisialisasi stemmer dan daftar stopwords
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stop_words = set(stopwords.words('indonesian'))

    word_index = {}  # Kamus untuk menyimpan indeks kata

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_num, filename in enumerate(os.listdir(input_folder), start=1):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    # Baca setiap baris dalam file, hilangkan spasi di awal dan akhir,
                    # dan hapus baris kosong
                    lines = [line.strip()
                             for line in infile if line.strip() != '']
                    # Gabungkan semua baris menjadi satu teks tanpa baris kosong
                    text = ' '.join(lines)

                    # Pisahkan teks menjadi kata-kata atau token
                    # Ubah teks menjadi huruf kecil untuk konsistensi
                    tokens = nltk.word_tokenize(text.lower())

                    # Hapus stopwords dan lakukan stemming pada setiap token
                    tokens = [stemmer.stem(
                        token) for token in tokens if token not in stop_words]

                    # Tulis token ke file output
                    outfile.write(' '.join(tokens) + '\n')

                    # Perbarui indeks kata
                    for i, token in enumerate(tokens):
                        if token not in word_index:
                            word_index[token] = {file_num: [i]}
                        else:
                            if file_num not in word_index[token]:
                                word_index[token][file_num] = [i]
                            else:
                                word_index[token][file_num].append(i)

    # Tulis indeks kata ke file dalam bentuk list
    with open(index_file, 'w', encoding='utf-8') as indexfile:
        for word, indices in word_index.items():
            index_list = [[file_num, index] for file_num,
                          index in indices.items()]  # Buat list dari kamus
            indexfile.write(f'{word}: {index_list}\n')


def main():
    input_folder = 'corpus2'
    output_file = 'indexWord.txt'
    index_file = 'index2.txt'
    index_txt_files(input_folder, output_file, index_file)
    print('Indeks file teks selesai.')


if __name__ == "__main__":
    main()
