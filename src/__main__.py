# from generators.star_subject_generator import *
import generators.star_subject_generator as ssg
#  from generators.data_handler import DataHandler

#  result = ssg.generate_query(4, 5, 0.7, 0.5)
print(ssg.create_operators(4, 0.9))

#  x = DataHandler()
#  query = "select distinct ?person where {?person foaf:name ?name .} LIMIT 10000" 
#  data = x.fetch_data(query)         #Parameter = query
#  print(data)
#  print("Measured Time: " + x.getTotalTime() + 's')
