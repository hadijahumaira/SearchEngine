import os
import re
from bs4 import BeautifulSoup

def clean_html_file(file_path, output_folder):
    with open(file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    cleaned_text = '\n'.join(p.get_text() for p in soup.find_all('p'))

    # Hapus kata "ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT", dan "[Gambas:Video CNN]"
    cleaned_text = cleaned_text.replace("ADVERTISEMENT", "").replace("SCROLL TO CONTINUE WITH CONTENT", "").replace("[Gambas:Video CNN]", "")

    # Hapus tanda baca dan baris baru yang lebih dari satu
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # menghapus tanda baca
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text)  # menghapus baris baru yang lebih dari satu

    txt_filename = os.path.splitext(os.path.basename(file_path))[0] + '.txt'
    txt_path = os.path.join(output_folder, txt_filename)
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(cleaned_text)

def main():
    folder_path = 'halaman_crawling/halaman'
    output_folder = 'corpus2'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            clean_html_file(file_path, output_folder)

    print('Pembersihan file HTML selesai.')

if __name__ == "__main__":
    main()
