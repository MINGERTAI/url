import requests
from bs4 import BeautifulSoup
import os

def fetch_and_save(url, output_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            file_url = url + href
            file_path = os.path.join(output_dir, href)
            try:
                # 尝试下载文件
                with requests.get(file_url, stream=True) as file_response:
                    with open(file_path, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"Downloaded {href}")
            except Exception as e:
                print(f"Failed to download {href}: {e}")

if __name__ == '__main__':
    fetch_and_save('http://example.com/', './out/test/')
