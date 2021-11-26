from generators.data_handler import DataHandler
class PathGenerator:
    def __init__(self, depth = 100, subject=None, predicate=None, object=None):
        self.depth = depth
        self.subject = subject
        self.predicate = predicate
        self.object = object
        #self.dataset = dataset
        self.depth = self.depth - 1
        print(self.depth) 
        print("S: " + str(self.subject) + " P: " + str(self.predicate) + " O: " + str(self.object))
        if self.depth == 0:
            return

        handler = DataHandler()
        if self.subject != None:            
            p = handler.searchwithsubject(self.subject)        
            PathGenerator(self.depth, predicate=p)
            return
        elif self.predicate != None:
            o = handler.searchwithpredicate(self.predicate)
            PathGenerator(self.depth, object=o)
            return
        elif self.object != None:
            #print(self.object)
            return
        else:
            s = handler.searchrandom()
            PathGenerator(self.depth, subject=s)
            return