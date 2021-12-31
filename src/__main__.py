# from generators.star_subject_generator import *
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
from generators.data_handler import DataHandler

#  result = ssg.generate_query(4, 5, 0.7, 0.5)
#print(ssg.generate_query(1, 4, 0.1, 0.5))
# print(sog.generate_query(1, 4, 0.9, 0.5))

#  x = DataHandler()
#  query = "select distinct ?person where {?person foaf:name ?name .} LIMIT 10000"
#  data = x.fetch_data(query)         #Parameter = query
#  print(data)
#  print("Measured Time: " + x.getTotalTime() + 's')

x = DataHandler()
#print(x.fetch_data_subject(3))
print(x.fetch_data_path(3))