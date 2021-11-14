# from generators.star_subject_generator import *
import json
import generators.star_subject_generator as ssg

result = ssg.generate_query(4, 4, 0.7, 0.5)
print(result['results']['bindings'])
