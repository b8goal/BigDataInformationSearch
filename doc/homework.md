Local 또는 클라우드에 도커 기반의 ElasticSearch + Kibana를 설치하고
- 30개 이상의 한국어 중심 문서/월/블로그뉴스 등으로 구성된 검색엔진 구축
	- Python Client 를 사용하여 개발
	- Kibana를 적용하여 Bulk 텍스트 처리 및 색인
	- 데이터 색인과 텍스트 분석(참고: https://esbook.kimjmin.net/06-text-analysis)
		- 쿼리 분석과 색인: 사용자 정의 custom analyzer 사용 (한국어 형태소 Non Tokenizer 사용)
	- 검색과 쿼리(https://esbook.kimjmin.net/05-search)
		- 검색모델: Elasticsearch BM25 모델 score 확인
		- Score에 따라 Top- 5 출력

- 검색엔진 구측 후 실험하고 레포트 제출
	- 제출사항
		- Python api 연동 source 코드
		- 검색 query와 검색결과 출력파일
		- 검색 성능 측정(Precision@K, MAP MRR, nDCG)
		- 검색엔진 구축 레포트(구축방법, 검색엔진 실행 화면, 검색성능 평가, 결론 및 문제점)