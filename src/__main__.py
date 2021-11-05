import requests

query_object = "SELECT DISTINCT *  FROM <http://dbpedia.org> WHERE{?s ?p ?o.} LIMIT 100"  # noqa: E501
req_object = requests.get('http://localhost:8890/sparql', params={'format': 'json', 'query': query_object})
resultobj = req_object.json()

print(resultobj)
