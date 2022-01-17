import requests
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg
import helpers.time_taker as tt
import helpers.graph_creator as gc
import statistics
import os


endpoint_url = 'http://localhost:8890/sparql?'  'https://dbpedia.org/sparql' 'http://192.168.1.24:8890/sparql?' 'http://localhost:8890/sparql?'
dir_path = os.path.dirname(__file__)

# query = pg.PathGenerator(endpoint_url).generate_query(1, 25, 0.5, 0.5)
# print(query)

queries = 5
triples_per_query = 2
triples_per_query_max = 20  # 10
triples_step = 2
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
                else:
                    print(ev_request)
                    ev_result = ev_request.json()
                    if ("^^" in ev_query and len(ev_result['results']['bindings']) == 0) or len(ev_result['results']['bindings']) == 0:
                        print("AUSGELASSEN:", ev_query)
                        print("AUSGELASSEN:", ev_request)
                        print("AUSGELASSEN:", ev_result)
                    else:
                        with open(os.path.join(dir_path, "queries/star_subject_queries.rq"), "a", encoding="utf-8") as text_file:
                            text_file.write(ev_query + "\n")
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

timelog.add_log(str(y_gen_ssg) + str(y_ev_ssg) + str(y_answers_ssg))
print(y_gen_ssg, y_ev_ssg, y_answers_ssg)
print("---------------- OBJECT -----------------")

# --------------------- OBJECT ---------------------
gen_name = "Star-Object"
y_gen_sog = []
y_ev_sog = []
y_answers_sog = []
triples_per_query = 2

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
                else:
                    with open(os.path.join(dir_path, "queries/star_object_queries.rq"), "a", encoding="utf-8") as text_file:
                        text_file.write(ev_query + "\n")
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

timelog.add_log(str(y_gen_sog) + str(y_ev_sog) + str(y_answers_sog))
print(y_gen_sog, y_ev_sog, y_answers_sog)
print("---------------- PATH -----------------")

# --------------------- PATH ---------------------
gen_name = "Path"
y_gen_pg = []
y_ev_pg = []
y_answers_pg = []
triples_per_query = 2

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
                else:
                    with open(os.path.join(dir_path, "queries/path_queries.rq"), "a", encoding="utf-8") as text_file:
                        text_file.write(ev_query + "\n")
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

timelog.add_log(str(y_gen_pg) + str(y_ev_pg) + str(y_answers_pg))
print(y_gen_pg, y_ev_pg, y_answers_pg)
print("---------------- MIXED -----------------")

# --------------------- MIXED ---------------------
gen_name = "Mixed"
y_gen_mg = []
y_ev_mg = []
y_answers_mg = []
triples_per_query = 4  # mixed needs at least 4 triples to function

y_gen_mg.append(None)
y_ev_mg.append(None)
y_answers_mg.append(None)

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
                if ev_request.status_code != 200:
                    print(ev_request)
                    print(ev_request.reason)
                    print(ev_query)
                else:
                    with open(os.path.join(dir_path, "queries/mixed_queries.rq"), "a", encoding="utf-8") as text_file:
                        text_file.write(ev_query + "\n")
                    print(ev_request)
                    ev_result = ev_request.json()
                    if ("^^" in ev_query and len(ev_result['results']['bindings']) == 0) or len(ev_result['results']['bindings']) == 0:
                        print("AUSGELASSEN:", ev_query)
                        print("AUSGELASSEN:", ev_request)
                        print("AUSGELASSEN:", ev_result)
                    else:
                        with open("mixed_queries.rq", "w") as text_file:
                            text_file.write(ev_query)
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

timelog.add_log(str(y_gen_mg) + str(y_ev_mg) + str(y_answers_mg))
print(y_gen_mg, y_ev_mg, y_answers_mg)

gc.Graph_Creator().create_generation_graph(x_index, y_gen_ssg, y_gen_sog, y_gen_pg, y_gen_mg)
gc.Graph_Creator().create_evaluation_graph(x_index, y_ev_ssg, y_ev_sog, y_ev_pg, y_ev_mg)
gc.Graph_Creator().create_answers_graph(x_index, y_answers_ssg, y_answers_sog, y_answers_pg, y_answers_mg)

# y_gen_ssg = [0.05544090000000068, 0.10855860000000206, 0.10896109999999837, 0.05642330000000584, 0.1134168000000102, 0.22117339999999786, 0.10700219999995397, 0.1103114000000005, 0.16433180000001357, 0.26416390000008505]
# y_gen_sog = [5.304825100000016, 5.29280360000007, 5.251365300000089, 5.258288300000004, 5.255307199999834, 5.243016000000125, 5.239419300000009, 5.200968300000113, 5.239564099999825, 5.231398699999772]
# y_gen_pg = [0.21206609999990178, 0.22853429999986474, 0.801322600000276, 0.8295269000000189, 3.1706067000000075, 4.363702300000114, 11.255400700000337, 51.71303690000059, 67.43576399999984, 158.37519760000032]
# y_gen_mg = [None, 5.241343100000009, 6.3774686000000145, 5.295652199999978, 0.4566115999999738, 5.710891800000013, 5.494324500000062, 5.730959600000006, 11.182035600000063, 10.982859700000063]

# gc.Graph_Creator().create_generation_graph(x_index, y_gen_ssg, y_gen_sog, y_gen_pg, y_gen_mg)

# y_ev_ssg = [0.019325200000000153, 0.1969510000000021, 0.09373589999999865, 0.7447933999999918, 0.8692357000000044, 0.7197749000000044, 0.7948807999999872, 2.4181901999999695, 1.7210011000000804, 1.9349771000000828]
# y_ev_sog = [0.12130760000013652, 0.4248233999999229, 0.433659999999918, 0.5670482000000447, 0.5378825000000234, 2.7613800999999967, 1.2566928000001099, 0.5118390999996336, 53.67777100000012, 62.46001100000012]
# y_ev_pg = [0.16346999999996115, 0.013109399999848392, 0.8231983000000582, 0.13343639999993684, 0.8788864999996804, 0.7249760999998216, 0.5151095000001078, 4.3485610999996425, 1.0440162999993845, 0.34165609999945445]
# y_ev_mg = [None, 0.31367119999999993, 0.037512400000011326, 0.6444377999999915, 0.0975945000000138, 1.055790600000023, 1.367515400000002, 4.005718499999944, 34.89313510000011, 0.843095500000345]

# gc.Graph_Creator().create_evaluation_graph(x_index, y_ev_ssg, y_ev_sog, y_ev_pg, y_ev_mg)

# y_answers_ssg = [0.019325200000000153, 0.1969510000000021, 0.09373589999999865, 0.7447933999999918, 0.8692357000000044, 0.7197749000000044, 0.7948807999999872, 2.4181901999999695, 1.7210011000000804, 1.9349771000000828]
# y_answers_sog = [0.12130760000013652, 0.4248233999999229, 0.433659999999918, 0.5670482000000447, 0.5378825000000234, 2.7613800999999967, 1.2566928000001099, 0.5118390999996336, 53.67777100000012, 62.46001100000012]
# y_answers_pg = [0.16346999999996115, 0.013109399999848392, 0.8231983000000582, 0.13343639999993684, 0.8788864999996804, 0.7249760999998216, 0.5151095000001078, 4.3485610999996425, 1.0440162999993845, 0.34165609999945445]
# y_answers_mg = [None, 0.31367119999999993, 0.037512400000011326, 0.6444377999999915, 0.0975945000000138, 1.055790600000023, 1.367515400000002, 4.005718499999944, 34.89313510000011, 0.843095500000345]

# gc.Graph_Creator().create_answers_graph(x_index, y_answers_ssg, y_answers_sog, y_answers_pg, y_answers_mg)


