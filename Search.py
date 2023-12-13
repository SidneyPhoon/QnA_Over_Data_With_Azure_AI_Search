from promptflow import tool
import requests, json
from promptflow.connections import CognitiveSearchConnection
 
def http_request(method, base_url, query_params=None, headers=None, json_body=None):
    try:
        if method in ('POST', 'PUT'):
            response = requests.post(base_url, params=query_params, headers=headers, json=json_body)
 
        elif method == 'GET':
            response = requests.get(base_url, headers=headers, params=query_params)
        
        status_code = response.status_code
        response_body = response.json()
 
    except Exception as e:
        status_code = 504
        response_body = str(e.args)
    
    return status_code, response_body
 
@tool
def vector_search(top_k: int, question: str, search: CognitiveSearchConnection) -> str:
    method = 'POST'
    index_name='hybrid-index-02'
    base_url = f'{search.api_base}/indexes/{index_name}/docs/search'
    query_params = {'api-version': search.api_version}
    print(search.api_version)
    headers = {'Content-Type': 'application/json', 'api-key': search.api_key}
    payload = {
      "search": question,
      "vectorQueries": [
        {
          "kind": "text",
          "text": question,
          "k": top_k,
          "fields": "vector"
        }
      ],
      "top": top_k,
      "queryType": "semantic",
      "semanticConfiguration": "hybrid-index-02-semantic-configuration",
      "captions": "extractive",
      "answers": "extractive|count-3",
      "queryLanguage": "en-US"
    }

    print(payload)
 
    status_code, res = http_request(method, base_url, query_params, headers, payload)
    
    if status_code == 200:
        return [i for i in res['value']]
    else:
        print(res)
        return []