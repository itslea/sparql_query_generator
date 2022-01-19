# SPARQL Query Generator

Seminar on Knowledge Graphs

## Query generation (def generate_query(...))

1. RDF data is fetched in data_handler.py
2. Data is transformed into triple patterns in def create_triple_patterns(...) and triple constants will be replaced with variables
3. Operators UNION, DISTINCT, and OPTIONAL are being created in operator_handler.py based on the obtained triple patterns, and variables for SELECT will be choosen
4. Query is being put together as a string and then returned

### Special Case: MixedGenerator

The MixedGenerator chooses two of the three shape types in random order (subject & object, object & subject, subject & path, path & subject, path & object or object & path) in data_handler.py. The number of triples will get divided between the two shapes (minimum is 2 each). The data for the first shape will be fetched and a "connecting" object will be choosen. That object will be used for the data fetching of the second shape. The two data lists will be joined and returned to the generator. From here on it works like the other generators.

## Datatype Error

Datatypes like float will be rounded when fetched from the endpoint in JSON serialization (doesn't happen with turtle serialization).
Example:
The endpoint returns the following JSON object to given subject "<http://dbpedia.org/resource/The_Mall_of_New_Hampshire__The_Mall_of_New_Hampshire__1>":

```json
{"p": {"type": "uri", "value": "http://www.w3.org/2003/01/geo/wgs84_pos#long"}, "o": {"type": "typed-literal", "datatype": "http://www.w3.org/2001/XMLSchema#float", "value": "-71.4328"}}
```

The generator will create a query based on the JSON object:

```sparql
SELECT * FROM <http://dbpedia.org> WHERE { <http://dbpedia.org/resource/The_Mall_of_New_Hampshire__The_Mall_of_New_Hampshire__1> ?p "-71.4328"^^<http://www.w3.org/2001/XMLSchema#float> }
```

If this query will now be sent back to the endpoint it won't return any answers, because the float number has been rounded while fetching it.
