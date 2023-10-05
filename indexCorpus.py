import os
import string
import nltk
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

nltk.download('punkt')
nltk.download('stopwords')

def index_txt_files(input_folder, output_file):
    # Inisialisasi stemmer dan daftar stopwords
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stop_words = set(stopwords.words('indonesian'))

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(input_folder):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    # Baca setiap baris dalam file, hilangkan spasi di awal dan akhir,
                    # dan hapus baris kosong
                    lines = [line.strip() for line in infile if line.strip() != '']
                    # Gabungkan semua baris menjadi satu teks tanpa baris kosong
                    text = ' '.join(lines)

                    # Pisahkan teks menjadi kata-kata atau token
                    tokens = nltk.word_tokenize(text.lower())  # Ubah teks menjadi huruf kecil untuk konsistensi

                    # Hapus stopwords dan lakukan stemming pada setiap token
                    tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]

                    # Tulis token ke file output
                    outfile.write(' '.join(tokens) + '\n')

def main():
    input_folder = 'corpus2'
    output_file = 'index2.txt'
    index_txt_files(input_folder, output_file)
    print('Indeks file teks selesai.')

if __name__ == "__main__":
    main()
