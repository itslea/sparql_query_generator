from matplotlib import colors
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker
from numpy import array

#Init params like double, arr, double, arr, double, arr

class Graph_Creator:
    """Creates the graphs for the evaluation metrics"""

    def create_generation_graph(self, x_ssg, y_ssg, x_sog, y_sog, x_pg, y_pg, x_mg, y_mg):
        plt.plot(x_ssg, y_ssg, label = "Star-Subject Generator", color = 'purple', marker = 'o', markersize = 8)
        plt.plot([3, 0], [0, 4], label = "Star-Object Generator", color = 'orange', marker = 'o', markersize = 6)
        plt.plot([0, 1], [1, 0], label = "Path Generator", color = 'green', marker = 'o', markersize = 6)
        plt.plot([1, 0], [2, 0], label = "Mixed Generator", color = 'blue', marker = 'o', markersize = 6)

        # plt.plot(x_sog, y_sog, label = "Star-Object Generator", color = 'orange', marker = 'o', markersize = 6)
        # plt.plot(x_pg, y_pg, label = "Path Generator", color = 'green', marker = 'o', markersize = 6)
        # plt.plot(x_mg, y_mg, label = "Mixed Generator", color = 'blue', marker = 'o', markersize = 6)

        plt.xlabel('triples per query')
        plt.ylabel('generation time (sec)')
        plt.title('Generation time of queries')
        plt.legend()
        plt.savefig('gen_time.png')

    def create_evaluation_graph(self, x_ssg, y_ssg, x_sog, y_sog, x_pg, y_pg, x_mg, y_mg):
        plt.plot(x_ssg, y_ssg, label = "Star-Subject Generator", color = 'purple', marker = 'o', markersize = 6)
        plt.plot([3, 0], [0, 4], label = "Star-Object Generator", color = 'orange', marker = 'o', markersize = 6)
        plt.plot([0, 1], [1, 0], label = "Path Generator", color = 'green', marker = 'o', markersize = 6)
        plt.plot([1, 0], [2, 0], label = "Mixed Generator", color = 'blue', marker = 'o', markersize = 6)

        # plt.plot(x_sog, y_sog, label = "Star-Object Generator", color = 'orange', marker = 'o', markersize = 6)
        # plt.plot(x_pg, y_pg, label = "Path Generator", color = 'green', marker = 'o', markersize = 6)
        # plt.plot(x_mg, y_mg, label = "Mixed Generator", color = 'blue', marker = 'o', markersize = 6)

        plt.xlabel('triples per query')
        plt.ylabel('request time (sec)')
        plt.title('Request time of generated queries')
        plt.legend()
        plt.savefig('ev_time.png')

    def create_answers_graph(self, x_ssg, y_ssg, x_sog, y_sog, x_pg, y_pg, x_mg, y_mg):
        df = pd.DataFrame({'Star-Subject Generator':y_ssg, 'Star_Object Generator': y_sog, 'Path Generator': y_pg, 'Mixed Generator': y_mg})
        df.index = x_ssg
        df.plot(kind = 'bar')

        plt.ylabel('answers produced')
        plt.gca().yaxis.set_major_formatter(ticker.Formatter('$%.2f'))
        plt.gca().xaxis.set_tick_params(rotation = 0)

        plt.title('Answers produced by generated queries')
        plt.legend()
        plt.savefig('answer_number.png')

