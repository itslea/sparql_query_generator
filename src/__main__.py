import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg
from helpers.data_handler import DataHandler
import helpers.timetaker as tt
import helpers.graph_creator as gg



queries = 10
total_exec = 1
triples_per_query = 5 
triples_per_query_max = 100
timelog = tt.TimeTaker("Mixed Gen")

none_counter = 0


for i in range(total_exec):
   while triples_per_query <= triples_per_query_max:
      timelog.start_timer()
      mg_query = mg.generate_query(queries, triples_per_query, 0.5, 0.5)
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
   print("for ist zu ende")

# ssg_query = ssg.generate_query(queries, triples_per_query, 0.5, 0.5)
# sog_query = sog.generate_query(queries, triples_per_query, 0.5, 0.5)
# pq = pg.generate_query(queries, triples_per_query, 0.5, 0.5)





# queries = 100
# triples_per_query = 10 


# queries4 = mg.generate_query(queries, triples_per_query, 0.5, 0.5)
# for elem in queries4['queries']:
#    print(elem + '\n')
# print("Execution time mixed: ", str(queries4['exectime']))





#graph = gg.Graph_Creator(queries4["exectime"], ["Mixed Gen.", "2"], 2.32, ["Name", "2", "Test"], 1.22, ["Name", "2", "Test"])

# queries = pg.generate_query(1, 6, 0.5, 0.5)
# for elem in queries['queries']:
#    print(elem + '\n')
# print("Execution time path: ", str(queries['exectime']))


# print(ssg.generate_query(1, 4, 0.1, 0.5))
# print(sog.generate_query(1, 4, 0.9, 0.5))

#  x = DataHandler()
#  query = "select distinct ?person where {?person foaf:name ?name .} LIMIT 10000"
#  data = x.fetch_data(query)         #Parameter = query
#  print(data)
#  print("Measured Time: " + x.getTotalTime() + 's')

# x = DataHandler()
# print(x.fetch_data_subject(3))
# print(x.fetch_data_path(3))


