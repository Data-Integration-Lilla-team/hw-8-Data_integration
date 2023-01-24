import pandas as pd
import os
import numpy as np
from parser_custom import Parser_custom
from Levenshtein import distance




def get_SRC_to_path(basic_path):
    Sorgenti2path=dict()                  
    for f in os.listdir(base_path):
        file=os.path.join(base_path,f)
        
        
            
        Sorgenti2path[f]=file
    return Sorgenti2path

def write_infos_on_file(file,basePath,string):
    fileTGT=os.path.join(basePath,file)
    with open(fileTGT, 'w') as f:
    
            f.write(string)

def get_SRC_to_datasets(Sorgenti2path):
    Sorgenti2team=dict()
    for k in Sorgenti2path.keys():
        
        folder_name=Sorgenti2path[k]
        list_of_files=[]
        for file in os.listdir(folder_name):
            if '.' not in file:                 #altri file non dataset
                nameTeam=file
                filePath=os.path.join(base_path,file)
                tupla=(nameTeam,filePath)
                list_of_files.append(tupla)
        
        Sorgenti2team[k]=list_of_files
    return Sorgenti2team

if __name__=='__main__':  
    #andiamo ad effettuare della anlisi relative a campi in overlap
    base_path='Project\\Dataset\\Clusters\\'
    
    Sorgenti2path=get_SRC_to_path(base_path)
    print(Sorgenti2path)


    
    Sorgenti2team=get_SRC_to_datasets(Sorgenti2path)

   

    informazioni_per_SRC='Project\\Dataset\\Informazioni'
    file_name='Popolosità_SRC.txt'
    stringa='SORGENTE\t #DATASETS\n'
    for k in Sorgenti2team.keys():
        stringa=stringa+k+'\t'+str(len(Sorgenti2team[k]))+'\n'

    write_infos_on_file(file_name,informazioni_per_SRC,stringa)



    #esplorazione dei dati
    from explore_single_SRC import Explorer
    explorer=Explorer()
    for k in Sorgenti2path.keys():
        explorer.explore_single_data(Sorgenti2path[k],k)
        
