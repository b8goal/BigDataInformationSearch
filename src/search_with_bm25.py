from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
index_name = "korean_news"

# 검색어
search_query = "검색 엔진"

# Elasticsearch 검색 API 호출
res = es.search(
    index=index_name,
    query={
        "match": {
            "content": search_query
        }
    },
    size=5 # 상위 5개 결과만 가져오기
)

print(f"'{search_query}' 검색 결과 (상위 5개):")
print("-" * 50)

# 검색 결과 출력
for hit in res['hits']['hits']:
    score = hit['_score'] # 이것이 BM25 점수입니다.
    title = hit['_source']['title']
    print(f"점수: {score:.2f}  |  제목: {title}")

print("-" * 50)