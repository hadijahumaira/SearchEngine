import os

# Ganti direktori_folder dengan direktori tempat Anda menyimpan file HTML
direktori_folder = "halaman_crawling/halaman"

# Ganti nama_file_txt dengan nama file teks yang Anda inginkan
nama_file_txt = "links.txt"

# Fungsi untuk mengambil semua file HTML dalam direktori


def ambil_file_html(direktori):
    file_html = []
    for root, dirs, files in os.walk(direktori):
        for file in files:
            if file.endswith(".html"):
                file_html.append(os.path.join(root, file))
    return file_html

# Fungsi untuk mengekstrak link dari file HTML dan menghindari anchor link


def ekstrak_link(file_html):
    links = []
    for file in file_html:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            # Anda dapat menggunakan ekspresi reguler atau pustaka parsing HTML seperti BeautifulSoup
            # di sini untuk mengekstrak link. Contoh sederhana:
            import re
            link_pattern = re.compile(r'href="(.*?)"')
            extracted_links = link_pattern.findall(content)
            for link in extracted_links:
                # Memeriksa apakah tautan mengandung tanda pagar
                if "#" not in link:
                    links.append(link)
    return links

# Fungsi untuk menulis link ke file teks dengan tanda kutip ganda dan koma


def tulis_ke_file_txt(links):
    with open(nama_file_txt, "w", encoding="utf-8") as f:
        for link in links:
            f.write(f'"{link}",\n')


if __name__ == "__main__":
    file_html = ambil_file_html(direktori_folder)
    links = ekstrak_link(file_html)
    tulis_ke_file_txt(links)
