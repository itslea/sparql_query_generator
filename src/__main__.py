# from generators.star_subject_generator import *
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
from generators.data_handler import DataHandler
import generators.timetaker as tt 
import generators.graph_creator as gg

x = gg.Graph_Creator(1.23, ["Name", "2", "Test"], 2.32, ["Name", "2", "Test"], 1.22, ["Name", "2", "Test"])

queries = ssg.generate_query(10, 5, 0.5, 0.5)
for elem in queries['queries']:
    print(elem + '\n')
print("Execution time subject: ", str(queries['exectime']))

queries2 = sog.generate_query(10, 5, 0.5, 0.5)
for elem in queries2['queries']:
    print(elem + '\n')
print("Execution time object: ", str(queries2['exectime']))

queries3 = pg.generate_query(10, 5, 0.5, 0.5)
for elem in queries3['queries']:
    print(elem + '\n')
print("Execution time path: ", str(queries3['exectime']))


'''Usecase of Time Taker'''
t = tt.TimeTaker("ssg")
t.stoptimer()


#print(ssg.generate_query(1, 4, 0.1, 0.5))
# print(sog.generate_query(1, 4, 0.9, 0.5))

#  x = DataHandler()
#  query = "select distinct ?person where {?person foaf:name ?name .} LIMIT 10000"
#  data = x.fetch_data(query)         #Parameter = query
#  print(data)
#  print("Measured Time: " + x.getTotalTime() + 's')

# x = DataHandler()
# print(x.fetch_data_subject(3))
# print(x.fetch_data_path(3))
