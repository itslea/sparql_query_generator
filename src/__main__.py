import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg
from helpers.data_handler import DataHandler
import helpers.timetaker as tt 
import helpers.graph_creator as gg

queries = 10
triples_per_query = 5
triples_per_query_max = 100
timelog = tt.TimeTaker("MixedGen")
none_counter = 0

while triples_per_query <= triples_per_query_max:
    timelog.start_timer()
    mg_query = mg.generate_query(queries, triples_per_query, 0.5, 0.5)
    print(mg_query)
    if mg_query is None:
        none_counter += 1
        if none_counter == 2:
            print("Vorzeitig beendet")
            break
    else:
        for elem in mg_query:
            timelog.message_log(str(elem))
            timelog.stop_timer()
            triples_per_query += 5
    print("ein while durchlauf zu ende")

# ssg_query = ssg.generate_query(queries, triples_per_query, 0.5, 0.5)
# sog_query = sog.generate_query(queries, triples_per_query, 0.5, 0.5)
# pq = pg.generate_query(queries, triples_per_query, 0.5, 0.5)
