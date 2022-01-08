# from generators.star_subject_generator import *
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg
from helpers.data_handler import DataHandler
import helpers.timetaker as tt 
import helpers.graph_creator as gg

# x = gg.Graph_Creator(1.23, ["Name", "2", "Test"], 2.32, ["Name", "2", "Test"], 1.22, ["Name", "2", "Test"])


queries4 = mg.generate_query(1, 4, 0.5, 0)
for elem in queries4['queries']:
    print(elem + '\n')
print("Execution time mixed: ", str(queries4['exectime']))

queries = sog.generate_query(1, 4, 0.5, 0)
for elem in queries['queries']:
    print(elem + "\n")
print("Execution time object: ", str(queries['exectime']))


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
