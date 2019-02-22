from __init__ import *
import json
from pprint import pprint
class DatasetManager():
    def __init__(self, **kwargs):
        self.tablename = kwargs["table"]
        data = []
        with open(self.tablename+'.json') as data_file:    
            data = json.load(data_file)



               
               
        print(json.dumps(data, indent=4))
               
        self.data = data
    def get_data(self): return self.data
    def Archivar(self):
        with open(self.tablename+".json", "w") as outfile:
            x = 0
            for i in self.data:
                x += 1
                if x == 1:
                    outfile.write("[\n")
                else:
                    outfile.write("\n,\n")
                json.dump(i, outfile, indent=4)
                
            outfile.write("]")
            
    def Insertar(self,**kwargs):
        self.data.append(kwargs["jdata"])

            
 
 
# Dataset = DatasetManager()
# Dataset.Insertar(jdata = {"Nombre":"Armando", "Apellido":"Joder"})
# Dataset.Insertar(jdata = {"Nombre":"Armando", "Apellido":"Joder"})
# Dataset.Insertar(jdata = {"Nombre":"Armando", "Apellido":"Joder"})
# Dataset.Archivar()
 