import requests
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg
from helpers.data_handler import DataHandler
import helpers.timetaker as tt 
import helpers.graph_creator as gg
from timeit import default_timer as timer

queries = 10
triples_per_query = 40
triples_per_query_max = 5
timelog = tt.TimeTaker("MixedGen")
none_counter = 0


mg_query = mg.generate_query(queries, triples_per_query, 0.5, 0.5)
print(mg_query)
# second_query.encode('utf-8')
# second_result = requests.get('https://dbpedia.org/sparql', params={'format': 'json', 'query': second_query})
# second_data = second_result.json()
# print(second_data)

ssg_queries = []

while triples_per_query >= triples_per_query_max:
    # timelog.start_timer()
    start_time = timer()
    mg_query = mg.generate_query(queries, triples_per_query, 0.5, 0.5)
    # print(mg_query)
    if mg_query is None:
        none_counter += 1
        print("uff")
        if none_counter == 2:
            print("Vorzeitig beendet")
            break
    else:
        exec_time = timer() - start_time
        print(exec_time)
        ssg_queries.append(mg_query)
        triples_per_query -= 5
    print("ein while durchlauf zu ende")

second_query = ssg_queries[0][0]
second_query.encode('utf-8')
second_timer = timer()
second_result = requests.get('https://dbpedia.org/sparql', params={'format': 'json', 'query': second_query})
second_data = second_result.json()
print("Query exec: ", timer() - second_timer)

# ssg_query = ssg.generate_query(queries, triples_per_query, 0.5, 0.5)
# sog_query = sog.generate_query(queries, triples_per_query, 0.5, 0.5)
# pq = pg.generate_query(queries, triples_per_query, 0.5, 0.5)
