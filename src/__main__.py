import requests
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg
import helpers.timetaker as tt 
from timeit import default_timer as timer

queries = 1
triples_per_query = 5
triples_per_query_max = 5
timelog = tt.TimeTaker()
none_counter = 0
gen_name = "Star-Subject"

gen_queries = []

# execution time of generation of queries
while triples_per_query >= triples_per_query_max:
    timelog.start_timer()
    ssg_query = ssg.generate_query(queries, triples_per_query, 0.5, 0.1)
    if ssg_query is None:
        none_counter += 1
        if none_counter == 2:
            print("Vorzeitig beendet")
            break
    else:
        exec_time = timelog.stop_timer("generation", triples_per_query, gen_name)
        print(exec_time)
        for query in ssg_query:
            gen_queries.append({"query": query, "triples": triples_per_query})
        triples_per_query -= 5
    print("ein while durchlauf zu ende")

print(gen_queries)

# execution time of sending queries back to endpoint + number of answers produced by it
for elem in gen_queries:
    print("Vorher: " + elem['query'])
    ev_query = elem['query'].encode('utf-8')
    timelog.start_timer()
    ev_request = requests.get('https://dbpedia.org/sparql', params={'format': 'json', 'query': ev_query})
    print(ev_request)
    ev_time = timelog.stop_timer("execution", elem['triples'], gen_name)
    ev_result = ev_request.json()
    # print(ev_result)
    ev_answers = len(ev_result['results']['bindings'])  # anzahl der antworten pro query
    timelog.message_log(elem['triples'], " answers: " + str(ev_answers))


