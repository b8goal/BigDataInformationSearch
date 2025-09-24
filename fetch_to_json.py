import requests
from bs4 import BeautifulSoup
import json
import sys
import os

def fetch_content(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else url
        # 본문 추출: 가장 긴 <p> 태그 묶음
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        content = '\n'.join([p for p in paragraphs if len(p) > 30])
        if not content:
            content = soup.get_text(separator=' ', strip=True)
        return {"title": title, "content": content}
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        return None

def main():
    # 명령줄 인자 있으면 그걸 사용, 없으면 data/url.txt 읽기
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
        print(f"[명령줄 인자] {len(urls)}개 url 입력받음")
    else:
        url_txt = os.path.join('data', 'url.txt')
        if not os.path.exists(url_txt):
            print("사용법: python fetch_to_json.py url1 url2 ...  또는  data/url.txt 파일에 url 한 줄씩 입력")
            sys.exit(1)
        with open(url_txt, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"[data/url.txt] {len(urls)}개 url 읽음")
    results = []
    for url in urls:
        print(f"수집 중: {url}")
        doc = fetch_content(url)
        if doc:
            results.append(doc)
    os.makedirs('data', exist_ok=True)
    with open('data/result.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"총 {len(results)}개 문서 저장 완료: data/result.json")

if __name__ == "__main__":
    main()
