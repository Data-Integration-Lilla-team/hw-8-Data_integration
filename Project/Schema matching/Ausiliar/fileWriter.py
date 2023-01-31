import os

class FileWriter:

    def __init__(self):
        pass

    def writeFile(self,file_name,basePath,string):
        
        fileTGT=os.path.join(basePath,file_name)
        with open(fileTGT, 'w') as f:
        
                f.write(string)