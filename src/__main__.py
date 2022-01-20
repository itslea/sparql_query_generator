import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg


endpoint_url = 'http://localhost:8890/sparql?'

# queries will also be saved to a file -> see folder 'queries'

queries_ssg = ssg.StarSubjectGenerator(endpoint_url).generate_query(1, 4, 0.5, 0.5)
for query in queries_ssg:
    print(query)

queries_sog = sog.StarObjectGenerator(endpoint_url).generate_query(1, 4, 0.5, 0.5)
for query in queries_sog:
    print(query)

queries_pg = pg.PathGenerator(endpoint_url).generate_query(1, 4, 0.5, 0.5)
for query in queries_pg:
    print(query)

queries_mg = mg.MixedGenerator(endpoint_url).generate_query(1, 4, 0.5, 0.5)
for query in queries_mg:
    print(query)
