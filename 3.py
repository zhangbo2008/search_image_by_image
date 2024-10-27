# 链接es

from elasticsearch import Elasticsearch
 
# 连接到Elasticsearch
es =  Elasticsearch("http://192.168.2.21:9200/")  # 默认端口是9200，如果不是，请替换端口号
 
# 获取所有数据
response = es.search(body={"query": {"match_all": {}}})
 
# 打印所有获取到的文档
for hit in response['hits']['hits']:
    print(hit)