from elasticsearch import Elasticsearch
import json
import os

# Elasticsearch 연결 (보안을 껐으므로 주소만 입력)
es = Elasticsearch("http://localhost:9200")

# ../data/result.json에서 데이터 읽기
data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'result.json'))
with open(data_path, 'r', encoding='utf-8') as f:
    docs = json.load(f)

index_name = "korean_news"

# 반복문을 통해 데이터 색인
for i, doc in enumerate(docs):
    res = es.index(index=index_name, id=i+1, document=doc)
    print(f"Indexed document {i+1}: {res['result']}")

print("모든 데이터 색인을 완료했습니다!")
