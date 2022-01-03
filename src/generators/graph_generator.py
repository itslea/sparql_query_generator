from matplotlib import colors
import matplotlib.pyplot as plt
from numpy import array



class Graph_Generator:
    def __init__(self, sog_time, sog_info, ssg_time, ssg_info, pg_time, pg_info):
        self.sog_time = sog_time
        self.sog_info = sog_info
        self.ssg_time = ssg_time
        self.ssg_info = ssg_info
        self.pg_time = pg_time
        self.pg_info = pg_info

        self.time_collection = [self.sog_time, self.ssg_time, self.pg_time]
        self.label_collection = []
        self.info = ""
        for info in sog_info:
            self.info = self.info + " " + info
        self.label_collection.append(str(self.info))

        self.info = ""
        for info in ssg_info:
            self.info = self.info + " " + info
        self.label_collection.append(str(self.info))

        self.info = ""
        for info in pg_info:
            self.info = self.info + " " + info
        self.label_collection.append(str(self.info))
        #label_collection kann alle Informationen der Graphen enthalten und halt dementsprechen auch in der Anzeige genutzt werden
        #aktuell noch nicht in gebrauch
        plt.title("Required time of the generators")
        plt.xlabel("Generators")
        plt.ylabel("Time")
        plt.bar(["Star-Subject","Star-Object","Path-Generator"], self.time_collection, color=('red', 'green', 'blue'))
        plt.show()

