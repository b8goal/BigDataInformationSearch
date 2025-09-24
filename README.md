# BigDataInformationSearch

## 1. 환경 구성

- Docker Compose로 Elasticsearch, Kibana 환경 구성
- Elasticsearch 8.11.4, Kibana 8.11.4 버전 사용
- Kibana와 Elasticsearch 연동 시 서비스 계정 토큰 방식 적용 (elastic/kibana)

### docker-compose.yml 주요 설정
- elasticsearch: xpack.security.enabled=false (보안 비활성화)
- kibana: ELASTICSEARCH_SERVICEACCOUNTTOKEN 환경변수에 서비스 토큰 입력

## 2. 데이터 준비

- data 폴더에 30개 이상의 한국어 문서(.txt) 또는 JSON 파일로 데이터 저장
- 각 문서는 뉴스, 블로그, 웹 등 다양한 출처에서 수집

### 데이터 저장 예시
```
data/news1.txt
data/blog1.txt
data/web1.txt
```
또는
```
data/result.json  # [{ "title": "...", "content": "..." }] 형태
```

## 3. 자동 데이터 수집 및 변환 스크립트

### fetch_to_json.py
- 여러 URL에서 웹페이지 제목/본문을 추출해 JSON 파일로 저장
- 두 가지 방식 지원:
  1. 명령줄에 URL 직접 입력
	  ```
	  python fetch_to_json.py https://news.naver.com/article/001/0012345678 https://blog.naver.com/abc/123456
	  ```
  2. data/url.txt 파일에 한 줄씩 URL 입력 후 실행
	  ```
	  python fetch_to_json.py
	  ```
	  (data/url.txt 예시)
	  https://news.naver.com/article/001/0012345678
	  https://blog.naver.com/abc/123456

실행 결과는 data/result.json 파일에 저장됨

---
추가 문의나 자동화, 데이터 변환 등 필요한 기능 있으면 언제든 말씀해 주세요!