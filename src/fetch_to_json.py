import requests
from bs4 import BeautifulSoup
import json
import sys
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_content(url):
    try:
        if isinstance(url, tuple):
            real_url, custom_title = url
        else:
            real_url, custom_title = url, None
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(real_url, timeout=10, verify=False, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = custom_title if custom_title else (soup.title.string.strip() if soup.title else real_url)
        
        try:
            if isinstance(url, tuple):
                real_url, custom_title = url
            else:
                real_url, custom_title = url, None
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            resp = requests.get(real_url, timeout=10, verify=False, headers=headers)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = custom_title if custom_title else (soup.title.string.strip() if soup.title else real_url)

            # 사이트별 본문 추출 최적화
            if "chiefexe.com" in real_url:
                article = soup.find("div", class_="article-view-content")
                if not article:
                    article = soup.find("div", id="article-view-content-div")
                if not article:
                    article = soup.find("section", class_="article-view-content")
                if article:
                    content = article.get_text(separator=' ', strip=True)
                else:
                    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
                    content = max(paragraphs, key=len) if paragraphs else soup.get_text(separator=' ', strip=True)
            elif "ifs.or.kr" in real_url:
                article = soup.find("div", class_="read_body")
                if not article:
                    article = soup.find("div", id="bo_v_con")
                if article:
                    content = article.get_text(separator='\n', strip=True)
                else:
                    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
                    content = max(paragraphs, key=len) if paragraphs else soup.get_text(separator=' ', strip=True)
            elif "n.news.naver.com" in real_url:
                article = soup.find("div", id="newsct_article")
                if not article:
                    article = soup.find("div", id="articeBody")
                if not article:
                    article = soup.find("div", id="dic_area")
                if article:
                    content = article.get_text(separator=' ', strip=True)
                else:
                    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
                    content = max(paragraphs, key=len) if paragraphs else soup.get_text(separator=' ', strip=True)
            elif "v.daum.net" in real_url:
                article = soup.find("div", id="harmonyContainer")
                if article:
                    content = article.get_text(separator=' ', strip=True)
                else:
                    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
                    content = max(paragraphs, key=len) if paragraphs else soup.get_text(separator=' ', strip=True)
                # 다음 뉴스 특유의 불필요 안내/요약/메타정보 패턴 제거
                daum_remove_patterns = [
                    r"^요약보기.*$", r"^자동요약.*$", r"^기사 제목과 주요 문장을 기반으로 자동요약한 결과입니다.*$",
                    r"^전체 맥락을 이해하기 위해서는 본문 보기를 권장합니다.*$", r"^관련 기사.*$", r"^사진.*$",
                    r"^\s*\d{4}\.\s*\d{1,2}\.\s*\d{1,2}\.\s*\d{1,2}:\d{2}.*$"
                ]
            else:
                blog_selectors = [
                    ("div", "articleView"), ("div", "article_content"), ("div", "article-body"),
                    ("div", "post-content"), ("div", "blogview_content"), ("div", "se-main-container"),
                    ("section", "wrap_body"), ("section", "article"), ("div", "content"),
                    ("div", "entry-content"), ("div", "postArticle-content"), ("div", "main-content"),
                    ("article", None)
                ]
                article = None
                for tag, cname in blog_selectors:
                    if cname:
                        found = soup.find(tag, class_=cname)
                        if not found:
                            found = soup.find(tag, id=cname)
                    else:
                        found = soup.find(tag)
                    if found and len(found.get_text(strip=True)) > 100:
                        article = found
                        break
                if article:
                    content = article.get_text(separator='\n', strip=True)
                else:
                    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
                    content = max(paragraphs, key=len) if paragraphs else soup.get_text(separator=' ', strip=True)

            # 본문에서 title 중복, 불필요한 개행/특수문자/광고/댓글/메타정보 등 필터링
            import re
            if title and content:
                content = content.replace(title, "")
            remove_patterns = [
                r"^▲.*$", r"^\s*댓글.*$", r"^\s*답변달기.*$", r"^\s*P by.*$", r"^\s*\(elma.dev\).*$", r"^\s*\|.*$",
                r"^\s*\d+일전.*$", r"^\s*★.*$", r"^\s*favorite.*$", r"^\s*[-]+$", r"^\s*\[.*\]$",
                r"^\s*인증 이메일 클릭후.*$", r"^\s*Hacker News 의견.*$", r"^https?://.*$",
                r"^\s*[-]+$", r"^\s*\*+$", r"^\s*\(.*\)$", r"^\s*\[.*\]$",
                r"^\s*[-=]{3,}$", r"^\s*\d+\s*$"
            ]
            if "v.daum.net" in real_url:
                remove_patterns += daum_remove_patterns
            lines = content.splitlines()
            filtered = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                skip = False
                for pat in remove_patterns:
                    if re.match(pat, line):
                        skip = True
                        break
                if not skip:
                    filtered.append(line)
            content = ' '.join(filtered)
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', content)
            return {"title": title, "content": content.strip()}
        except Exception as e:
            print(f"[ERROR] {url}: {e}")
            return None
        return {"title": title, "content": content.strip()}
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        return None

def main():
    # 명령줄 인자 있으면 그걸 사용, 없으면 data/url.txt 읽기
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
        print(f"[명령줄 인자] {len(urls)}개 url 입력받음")
        url_tuples = [(u, None) for u in urls]
    else:
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        url_txt = os.path.join(data_dir, 'url.txt')
        if not os.path.exists(url_txt):
            print("사용법: python fetch_to_json.py url1 url2 ...  또는  data/url.txt 파일에 url 한 줄씩 입력")
            sys.exit(1)
        url_tuples = []
        with open(url_txt, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '#' in line:
                    url_part, title_part = line.split('#', 1)
                    url = url_part.strip()
                    title = title_part.strip()
                    if url:
                        url_tuples.append((url, title))
                else:
                    url_tuples.append((line, None))
        print(f"[data/url.txt] {len(url_tuples)}개 url 읽음")
    results = []
    for url_tuple in url_tuples:
        print(f"수집 중: {url_tuple[0]}")
        doc = fetch_content(url_tuple)
        if doc:
            results.append(doc)
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    os.makedirs(data_dir, exist_ok=True)
    result_json_path = os.path.join(data_dir, 'result.json')
    with open(result_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"총 {len(results)}개 문서 저장 완료: {result_json_path}")

if __name__ == "__main__":
    main()
