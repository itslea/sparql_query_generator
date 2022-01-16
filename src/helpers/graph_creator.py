from matplotlib import colors
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker
from numpy import array

#Init params like double, arr, double, arr, double, arr

class Graph_Creator:
    """Creates the graphs for the evaluation metrics"""

    def create_generation_graph(self, x_index, y_ssg, y_sog, y_pg, y_mg):
        plt.clf()
        plt.plot(x_index, y_ssg, label="Star-Subject Generator", color='purple', marker='o', markersize=6)
        plt.plot(x_index, y_sog, label="Star-Object Generator", color='orange', marker='o', markersize=6)
        plt.plot(x_index, y_pg, label="Path Generator", color='green', marker='o', markersize=6)
        plt.plot(x_index, y_mg, label="Mixed Generator", color='blue', marker='o', markersize=6)

        plt.xlabel('triples per query')
        plt.ylabel('generation time (sec)')
        plt.title('Generation time of queries')
        plt.legend()
        plt.savefig('gen_time.png')

    def create_evaluation_graph(self, x_index, y_ssg, y_sog, y_pg, y_mg):
        plt.clf()
        plt.plot(x_index, y_ssg, label="Star-Subject Generator", color='purple', marker='o', markersize=6)
        plt.plot(x_index, y_sog, label="Star-Object Generator", color='orange', marker='o', markersize=6)
        plt.plot(x_index, y_pg, label="Path Generator", color='green', marker='o', markersize=6)
        plt.plot(x_index, y_mg, label="Mixed Generator", color='blue', marker='o', markersize=6)

        plt.xlabel('triples per query')
        plt.ylabel('request time (sec)')
        plt.title('Request time of generated queries')
        plt.legend()
        plt.savefig('ev_time.png')

    def create_answers_graph(self, x_index, y_ssg, y_sog, y_pg, y_mg):
        plt.clf()
        df = pd.DataFrame({'Star-Subject Generator': y_ssg, 'Star_Object Generator': y_sog, 'Path Generator': y_pg, 'Mixed Generator': y_mg})
        df.index = x_index
        df.plot(kind='bar', stacked=True)

        plt.ylabel('answers produced')
        plt.title('Answers produced by generated queries')
        plt.legend()
        plt.savefig('answer_number.png')
