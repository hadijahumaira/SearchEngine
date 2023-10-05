import requests
from bs4 import BeautifulSoup
import random
import os
import re

def get_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links
    else:
        print("Gagal mengambil halaman web.")
        return []

def save_article(link, session):
    response = session.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        filename = re.sub(r'[\/:*?"<>|]', '', title) + '.html'
        with open(os.path.join('halaman_crawling/halaman', filename), 'w', encoding='utf-8') as file:
            file.write(response.text)
            return True
    else:
        print(f"Gagal mengakses tautan berita {link}")
        return False

def is_valid_link(link):
    pattern = r'https://www.cnnindonesia.com/internasional/\d{14}-\d+-\d+/[a-z0-9-]+'
    return re.match(pattern, link) is not None

def main():
    url = 'https://www.cnnindonesia.com/internasional/indeks/6'
    links = get_links(url)
    random.shuffle(links)

    if not os.path.exists('halaman_crawling/halaman'):
        os.makedirs('halaman_crawling')

    saved_count = 0
    with requests.Session() as session:
        for link in links:
            if is_valid_link(link) and save_article(link, session):
                saved_count += 1
                print(f"{saved_count} berita disimpan")
                if saved_count >= 100:
                    break

    print(f"Total {saved_count} tautan berita berhasil diakses dan disimpan.")

if __name__ == "__main__":
    main()
