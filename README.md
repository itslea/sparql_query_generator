# SPARQL Query Generator

Seminar on Knowledge Graphs

## Query generation

1. RDF data will be fetched in data_handler.py
2. f

### Datatype Error

Datatypes like float will be rounded when fetched from the endpoint in JSON serialization (doesn't happen with turtle serialization).
Example:
The endpoint returns the following JSON object to given subject <http://dbpedia.org/resource/The_Mall_of_New_Hampshire__The_Mall_of_New_Hampshire__1>:

```json
{"p": {"type": "uri", "value": "http://www.w3.org/2003/01/geo/wgs84_pos#long"}, "o": {"type": "typed-literal", "datatype": "http://www.w3.org/2001/XMLSchema#float", "value": "-71.4328"}} 
```

The generator will generate a query based on the JSON object:

```sparql
SELECT * FROM <http://dbpedia.org> WHERE { <http://dbpedia.org/resource/The_Mall_of_New_Hampshire__The_Mall_of_New_Hampshire__1> ?p "-71.4328"^^<http://www.w3.org/2001/XMLSchema#float> }
```

If this query will now be sent back to the endpoint it won't return any answers, because the float number has been rounded while fetching it.
