import requests
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
import generators.mixed_generator as mg
import helpers.timetaker as tt 
from timeit import default_timer as timer


# test_query= "SELECT DISTINCT * FROM <http://dbpedia.org> WHERE { { <http://dbpedia.org/resource/Aisyiyah> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/SocialGroup107950920> . } UNION { <http://dbpedia.org/resource/Aisyiyah> <http://dbpedia.org/ontology/abstract> \"Aisyiyah is an Islamic non-governmental organization in Indonesia dedicated to female empowerment and charitable work. It was formed on 19 May 1917 by Nyai Ahmad Dahlan to facilitate women's access to education, health care and social services. The organization provides micro-loan and small business development support, family planning services, maternal and pediatric care, orphanages, training for female Muslim clerics, and standard preschool through university level education. These social services end at death, whereby the organization provides female morticians so that female bodies do not need to be prepared for burial by men. Aisyiyah manages several hundred healthcare centers in Indonesia as well as three branches in Egypt, Malaysia and the Netherlands. The organization's stated goal is to make Islamic society a reality for women, and it encourages its members to seek further education even if they become \"smarter than their husbands.\" Aisyiyah faces opposition to their work from two sources: traditional Javanese culture with its pre-Islamic practices and the minority of Indonesians who study Islam in the Middle East both display negative attitudes toward women in the public space.\"@en . } OPTIONAL { <http://dbpedia.org/resource/Aisyiyah> ?p1 <http://dbpedia.org/resource/Muhammadiyah> . <http://dbpedia.org/resource/Aisyiyah> <http://dbpedia.org/ontology/wikiPageWikiLink> <http://dbpedia.org/resource/Middle_East> . <http://dbpedia.org/resource/Aisyiyah> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Organization> . } }"
# print("Vorher: " + test_query)
# ev_query = str(tes).encode('utf-8')
# ev_request = requests.get('https://dbpedia.org/sparql', params={'format': 'json', 'query': ev_query})
# print(ev_request)
# ev_result = ev_request.json()
# # print(ev_result)
# ev_answers = len(ev_result['results']['bindings'])  # anzahl der antworten pro query


queries = 10
triples_per_query = 50
triples_per_query_max = 5
timelog = tt.TimeTaker()
none_counter = 0
gen_name = "Star-Subject"

gen_queries = []

# execution time of generation of queries
while triples_per_query >= triples_per_query_max:
    timelog.start_timer()
    ssg_query = ssg.generate_query(queries, triples_per_query, 0.5, 0.5)
    if ssg_query is None:
        none_counter += 1
        if none_counter == 2:
            print("Vorzeitig beendet")
            break
    else:
        exec_time = timelog.stop_timer()
        print(exec_time)
        for query in ssg_query:
            gen_queries.append({"query": query, "triples": triples_per_query, "exectime": str(exec_time)})
        triples_per_query -= 5
    print("ein while durchlauf zu ende")

# print(gen_queries)

# execution time of sending queries back to endpoint + number of answers produced by it
for elem in gen_queries:
    # print("Vorher: " + elem['query'])
    ev_query = str(elem['query']).encode()
    if "^^" in str(elem['query']): # TODO: es fehlen dann aber queries, weil die einfach ausgelassen werden
        print("AUSGELASSEN")
    else:
        timelog.start_timer()
        ev_request = requests.get('https://dbpedia.org/sparql', params={'format': 'json', 'query': ev_query})
        print(ev_request)
        ev_time = timelog.stop_timer()
        ev_result = ev_request.json()
        # print(ev_result)
        ev_answers = len(ev_result['results']['bindings'])  # anzahl der antworten pro query
        timelog.message_log(gen_name, elem['triples'], elem['exectime'], ev_time, ev_answers)
        if ev_answers == 0:
            print(ev_query)
            print(ev_result)
            print(ev_request.content)
            print("\n")
