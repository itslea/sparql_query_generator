import requests
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg
import helpers.time_taker as tt
import helpers.graph_creator as gc
import statistics
from timeit import default_timer as timer


endpoint_url = 'http://localhost:8890/sparql?'  # 'https://dbpedia.org/sparql' 'http://192.168.1.24:8890/sparql?' 'http://localhost:8890/sparql?'
queries = 10
triples_per_query = 5
triples_per_query_max = 30  # 10
triples_step = 5
timelog = tt.TimeTaker()
none_counter = 0
x_index = list(range(triples_per_query, triples_per_query_max + triples_step, triples_step))

# --------------------- SUBJECT ---------------------
gen_name = "Star-Subject"
y_gen_ssg = []
y_ev_ssg = []
y_answers_ssg = []

while triples_per_query <= triples_per_query_max:
    i = 0
    temp_gen_time = []
    temp_ev_time = []
    temp_answers = []
    while i < queries:
        timelog.start_timer()
        gen_query = ssg.StarSubjectGenerator(endpoint_url).generate_query(1, triples_per_query, 0.5, 0.5)
        if gen_query is None:
            none_counter += 1
            if none_counter == 2:
                print("Vorzeitig beendet, break")
                break
        else:
            exec_time = timelog.stop_timer()
            # print(exec_time)
            for query in gen_query:
                ev_query = str(query)
                timelog.start_timer()
                ev_request = requests.get(endpoint_url, params={'format': 'json', 'query': ev_query})
                ev_time = timelog.stop_timer()
                if ev_request.status_code == 500:
                    print(ev_request)
                    print(ev_request.reason)
                    print(ev_query)
                    ev_time = 400
                    ev_answers = 0
                    temp_gen_time.append(exec_time)
                    temp_ev_time.append(ev_time)
                    temp_answers.append(ev_answers)
                    timelog.message_log(gen_name, triples_per_query, exec_time, ev_time, ev_answers)
                    i += 1
                else:
                    print(ev_request)
                    ev_result = ev_request.json()
                    if ("^^" in ev_query and len(ev_result['results']['bindings']) == 0) or len(ev_result['results']['bindings']) == 0:
                        print("AUSGELASSEN:", ev_query)
                        print("AUSGELASSEN:", ev_request)
                        print("AUSGELASSEN:", ev_result)
                    else:
                        temp_gen_time.append(exec_time)
                        temp_ev_time.append(ev_time)
                        ev_answers = len(ev_result['results']['bindings'])
                        temp_answers.append(ev_answers)
                        timelog.message_log(gen_name, triples_per_query, exec_time, ev_time, ev_answers)
                        i += 1

    y_gen_ssg.append(statistics.median(temp_gen_time))
    y_ev_ssg.append(statistics.median(temp_ev_time))
    y_answers_ssg.append(statistics.median(temp_answers))
    triples_per_query += triples_step

print(y_gen_ssg, y_ev_ssg)
print("---------------- OBJECT -----------------")

# --------------------- OBJECT ---------------------
gen_name = "Star-Object"
y_gen_sog = []
y_ev_sog = []
y_answers_sog = []
triples_per_query = 5

while triples_per_query <= triples_per_query_max:
    i = 0
    temp_gen_time = []
    temp_ev_time = []
    temp_answers = []
    while i < queries:
        timelog.start_timer()
        gen_query = sog.StarObjectGenerator(endpoint_url).generate_query(1, triples_per_query, 0.5, 0.5)
        if gen_query is None:
            none_counter += 1
            if none_counter == 2:
                print("Vorzeitig beendet, break")
                break
        else:
            exec_time = timelog.stop_timer()
            # print(exec_time)
            for query in gen_query:
                ev_query = str(query)
                timelog.start_timer()
                ev_request = requests.get(endpoint_url, params={'format': 'json', 'query': ev_query})
                ev_time = timelog.stop_timer()
                if ev_request.status_code == 500:
                    print(ev_request)
                    print(ev_request.reason)
                    print(ev_query)
                    ev_time = 400
                    ev_answers = 0
                    temp_gen_time.append(exec_time)
                    temp_ev_time.append(ev_time)
                    temp_answers.append(ev_answers)
                    timelog.message_log(gen_name, triples_per_query, exec_time, ev_time, ev_answers)
                    i += 1
                else:
                    print(ev_request)
                    ev_result = ev_request.json()
                    if ("^^" in ev_query and len(ev_result['results']['bindings']) == 0) or len(ev_result['results']['bindings']) == 0:
                        print("AUSGELASSEN:", ev_query)
                        print("AUSGELASSEN:", ev_request)
                        print("AUSGELASSEN:", ev_result)
                    else:
                        temp_gen_time.append(exec_time)
                        temp_ev_time.append(ev_time)
                        ev_answers = len(ev_result['results']['bindings'])
                        temp_answers.append(ev_answers)
                        timelog.message_log(gen_name, triples_per_query, exec_time, ev_time, ev_answers)
                        i += 1

    y_gen_sog.append(statistics.median(temp_gen_time))
    y_ev_sog.append(statistics.median(temp_ev_time))
    y_answers_sog.append(statistics.median(temp_answers))
    triples_per_query += triples_step

print(y_gen_sog, y_ev_sog)
print("---------------- PATH -----------------")

# --------------------- PATH ---------------------
gen_name = "Path"
y_gen_pg = []
y_ev_pg = []
y_answers_pg = []
triples_per_query = 5

while triples_per_query <= triples_per_query_max:
    i = 0
    temp_gen_time = []
    temp_ev_time = []
    temp_answers = []
    while i < queries:
        timelog.start_timer()
        gen_query = pg.PathGenerator(endpoint_url).generate_query(1, triples_per_query, 0.5, 0.5)
        if gen_query is None:
            none_counter += 1
            if none_counter == 2:
                print("Vorzeitig beendet, break")
                break
        else:
            exec_time = timelog.stop_timer()
            # print(exec_time)
            for query in gen_query:
                ev_query = str(query)
                timelog.start_timer()
                ev_request = requests.get(endpoint_url, params={'format': 'json', 'query': ev_query})
                ev_time = timelog.stop_timer()
                if ev_request.status_code == 500:
                    print(ev_request)
                    print(ev_request.reason)
                    print(ev_query)
                    ev_time = 400
                    ev_answers = 0
                    temp_gen_time.append(exec_time)
                    temp_ev_time.append(ev_time)
                    temp_answers.append(ev_answers)
                    timelog.message_log(gen_name, triples_per_query, exec_time, ev_time, ev_answers)
                    i += 1
                else:
                    print(ev_request)
                    ev_result = ev_request.json()
                    if ("^^" in ev_query and len(ev_result['results']['bindings']) == 0) or len(ev_result['results']['bindings']) == 0:
                        print("AUSGELASSEN:", ev_query)
                        print("AUSGELASSEN:", ev_request)
                        print("AUSGELASSEN:", ev_result)
                    else:
                        temp_gen_time.append(exec_time)
                        temp_ev_time.append(ev_time)
                        ev_answers = len(ev_result['results']['bindings'])
                        temp_answers.append(ev_answers)
                        timelog.message_log(gen_name, triples_per_query, exec_time, ev_time, ev_answers)
                        i += 1

    y_gen_pg.append(statistics.median(temp_gen_time))
    y_ev_pg.append(statistics.median(temp_ev_time))
    y_answers_pg.append(statistics.median(temp_answers))
    triples_per_query += triples_step

print(y_gen_pg, y_ev_pg)
print("---------------- MIXED -----------------")

# --------------------- MIXED ---------------------
gen_name = "Mixed"
y_gen_mg = []
y_ev_mg = []
y_answers_mg = []
triples_per_query = 5

while triples_per_query <= triples_per_query_max:
    i = 0
    temp_gen_time = []
    temp_ev_time = []
    temp_answers = []
    while i < queries:
        timelog.start_timer()
        gen_query = mg.MixedGenerator(endpoint_url).generate_query(1, triples_per_query, 0.5, 0.5)
        if gen_query is None:
            none_counter += 1
            if none_counter == 2:
                print("Vorzeitig beendet, break")
                break
        else:
            exec_time = timelog.stop_timer()
            # print(exec_time)
            for query in gen_query:
                ev_query = str(query)
                timelog.start_timer()
                ev_request = requests.get(endpoint_url, params={'format': 'json', 'query': ev_query})
                ev_time = timelog.stop_timer()
                if ev_request.status_code == 500:
                    print(ev_request)
                    print(ev_request.reason)
                    print(ev_query)
                    ev_time = 400
                    ev_answers = 0
                    temp_gen_time.append(exec_time)
                    temp_ev_time.append(ev_time)
                    temp_answers.append(ev_answers)
                    timelog.message_log(gen_name, triples_per_query, exec_time, ev_time, ev_answers)
                    i += 1
                else:
                    print(ev_request)
                    ev_result = ev_request.json()
                    if ("^^" in ev_query and len(ev_result['results']['bindings']) == 0) or len(ev_result['results']['bindings']) == 0:
                        print("AUSGELASSEN:", ev_query)
                        print("AUSGELASSEN:", ev_request)
                        print("AUSGELASSEN:", ev_result)
                    else:
                        temp_gen_time.append(exec_time)
                        temp_ev_time.append(ev_time)
                        ev_answers = len(ev_result['results']['bindings'])
                        temp_answers.append(ev_answers)
                        timelog.message_log(gen_name, triples_per_query, exec_time, ev_time, ev_answers)
                        i += 1

    y_gen_mg.append(statistics.median(temp_gen_time))
    y_ev_mg.append(statistics.median(temp_ev_time))
    y_answers_mg.append(statistics.median(temp_answers))
    triples_per_query += triples_step

print(y_gen_mg, y_ev_mg)
gc.Graph_Creator().create_generation_graph(x_index, y_gen_ssg, y_gen_sog, y_gen_pg, y_gen_mg)
gc.Graph_Creator().create_evaluation_graph(x_index, y_ev_ssg, y_ev_sog, y_ev_pg, y_ev_mg)
gc.Graph_Creator().create_answers_graph(x_index, y_answers_ssg, y_answers_sog, y_answers_pg, y_answers_mg)
