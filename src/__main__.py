import requests
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg
import helpers.time_taker as tt
import helpers.graph_creator as gc
from timeit import default_timer as timer


#test_query= "SELECT DISTINCT * FROM <http://dbpedia.org> WHERE { <http://dbpedia.org/resource/The_Mall_of_New_Hampshire__The_Mall_of_New_Hampshire__1> ?p4 \"-71.4328\"^^<http://www.w3.org/2001/XMLSchema#float> }"
# print("Vorher: " + test_query)
#test_query = "SELECT * FROM <http://dbpedia.org> WHERE { ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o1 . ?s <http://www.w3.org/2002/07/owl#sameAs> ?o2 . ?s ?p1 ?o3 . ?s ?p2 ?o4 . ?s ?p3 <http://dbpedia.org/resource/Human_Drama> . ?s <http://www.w3.org/2002/07/owl#sameAs> ?o5 . ?s ?p4 'Mark Balderas (born September 10, 1959 in Encino, California) is the keyboardist for the rock band Human Drama from 1986 to 1991 and from 1993 to 2005 and has been currently active with the band since 2012.'@en . ?s ?p5 <http://dbpedia.org/resource/Category:Los_Angeles_Pierce_College_people> . ?s ?p6 ?o6 . ?s ?p7 ?o7 . }"

# ev_query = str(tes).encode('utf-8')
#ev_request = requests.get('https://dbpedia.org/sparql', params={'format': 'json', 'query': str(test_query)})
#print(ev_request)
#ev_result = ev_request.json()
#print(ev_result)
#print(ev_request.apparent_encoding)
# ev_answers = len(ev_result['results']['bindings'])  # anzahl der antworten pro query

endpoint_url = 'https://dbpedia.org/sparql'  # 'https://dbpedia.org/sparql' #'https://dbpedia.org/sparql' #  'http://192.168.1.24:8890/sparql?' #'https://dbpedia.org/sparql'  # 'http://localhost:8890/sparql?'
queries = 10
triples_per_query = 5
triples_per_query_max = 5 # 10
timelog = tt.TimeTaker()
none_counter = 0
gen_name = "Star-Subject"

# gen_queries = []

x_gen_ssg = []
y_gen_ssg = []
x_ev_ssg = []
y_ev_ssg = []
while triples_per_query <= triples_per_query_max:
    i = 0
    temp_gen_time = 0
    temp_ev_time = 0
    while i < queries:
        timelog.start_timer()
        ssg_query = ssg.StarSubjectGenerator(endpoint_url).generate_query(1, triples_per_query, 0.5, 0.5)
        if ssg_query is None:
            none_counter += 1
            if none_counter == 2:
                print("Vorzeitig beendet, break")
                break
        else:
            exec_time = timelog.stop_timer()
            # print(exec_time)
            for query in ssg_query:
                ev_query = str(query)
                timelog.start_timer()
                ev_request = requests.get(endpoint_url, params={'format': 'json', 'query': ev_query})
                print(ev_request)
                ev_time = timelog.stop_timer()
                ev_result = ev_request.json()
                if ("^^" in ev_query and len(ev_result['results']['bindings']) == 0) or len(ev_result['results']['bindings']) == 0:
                    print("AUSGELASSEN:", ev_query)
                    print("AUSGELASSEN:", ev_request)
                    print("AUSGELASSEN:", ev_result)
                else:
                    temp_gen_time += exec_time
                    temp_ev_time += ev_time
                    ev_answers = len(ev_result['results']['bindings'])
                    timelog.message_log(gen_name, triples_per_query, exec_time, ev_time, ev_answers)
                    i += 1
    x_gen_ssg.append(triples_per_query)
    y_gen_ssg.append(temp_gen_time / queries)
    x_ev_ssg.append(triples_per_query)
    y_ev_ssg.append(temp_ev_time / queries)
    triples_per_query += 5

gc.Graph_Creator().create_generation_graph(x_gen_ssg, y_gen_ssg, None, None, None, None, None, None)
gc.Graph_Creator().create_evaluation_graph(x_gen_ssg, y_gen_ssg, None, None, None, None, None, None)
