import pandas as pd
import os
import numpy as np
from matching_module import MatchingModule
from parsing_data import Parser_data
from Levenshtein import distance

'''
questo modulo è responsabile della gestione della pipeline di creazione dei dizionari dei sinonimi.
Per ogni cluster (sorgente dati uguale [companiesmarket cap, etc...]) effettua le seguenti elaborazioni
1. parsing dei dati (uniformazione e standardidazione dei nomi delle colonne e delle tabelle)
2. cleaning dei dati
3. creazione di un dizionario preliminare di sinonimi mediante analisi della correlazione tra i nomi delle colonne DIZ 1
4. creazione di un dizionario preliminare di sinonimi mediante clusterizzazione delle colonne in base a feature predefinite DIZ 2
5. Unione dei dizionari DIZ 1, DIZ 2
6. Creazione del Dizionario dei sinonimi mediante utilizzo di Valentine
7. Creazione dello schema mediato
'''

#Crea un dizionario key, val dove:
#key-> nome del sorgente (cluster)
#value-> nome del path del sorgente
#NOTA!
#Nel sorgente sono presenti le tabelle (file .csv)
def get_SRC_to_path(basic_path):
    Sorgenti2path=dict()                  
    for f in os.listdir(basic_path):
        file=os.path.join(basic_path,f)
        
        
            
        Sorgenti2path[f]=file
    return Sorgenti2path


#Il metodo crea un dizionario key value dove:
#key->nome del sorgente (cluster)
#value->lista dei (team,path_dataset) presenti in quel sorgente
#ESEMPIO
#companiesmarketcap [('00-avengers.csv', 'Project\\Dataset\\Clusters_CSV\\original\\00-avengers.csv'), ('01-DDD.csv', 'Project\\Dataset\\Clusters_CSV\\original\\01-DDD.csv')
def get_SRC_to_datasets(Sorgenti2path):
    Sorgenti2team=dict()
    for k in Sorgenti2path.keys():
        
        folder_name=Sorgenti2path[k]
        list_of_files=[]
        for file in os.listdir(folder_name):
                            #altri file non dataset
                nameTeam=file
                filePath=os.path.join(Sorgenti2path[k],file)
                tupla=(nameTeam,filePath)
                list_of_files.append(tupla)
        
        Sorgenti2team[k]=list_of_files
    return Sorgenti2team

#itera nel cluster passato ed effettua le operazioni di parsing
#restituisce un dizionario key, val dove
#key->nome sorgente (cluster)
#value->lista di tuple (nome team, path nuovo ds)
def parse_data(sorgenti):
    tgt_dataset_parsed='Project\\Dataset\\ClusterParsed'

    #il parser potrebbe essere istanziato passando il valore (nome del cluster)
    parser=Parser_data()
    cluster2newSRCDs=dict()
    for k in sorgenti.keys():
        print('cluster',k)
        cluster2newSRCDs[k]=[]
        for filename in os.listdir(sorgenti[k]):
            src=os.path.join(sorgenti[k],filename)
            final_path=os.path.join(tgt_dataset_parsed,k)
            final_path=os.path.join(final_path,filename)                     
            print('path ds src:',src)
            print('tgr:',final_path)
            parser.parse_data(src,final_path)
            team_name=filename.replace('.csv','')
            cluster2newSRCDs[k].append((team_name,final_path))
            
            
            
        
        
        
       
        
#metodo generale per la creazione del dizionario dei sinonimi per ogni elemento
# 1. crea il diz 1
# 2. crea il diz 2
# 3. unifica i dizionari
    
def create_sin_dic(sorgente2path):
    dic_for_cluster=dict()
    for k in sorgente2path.keys():
        
        matcher=MatchingModule(k)                                #da definire il nome del cluster dove memorizzare le ingo
        dic_for_cluster[k]=matcher.create_dic_sin(sorgente2path[k],k)

    return dic_for_cluster

        
        


if __name__=='__main__':  
    
    base_path='Project\\Dataset\\ClustersCSV'    #path dei .csv originali

    #per ogni sorgente (cluster name) associamo il path del dir per raggiungere le tabelle contenute in esso 
     #(name_cluster: path_cluster)
    #ESEMPIO:->CLUSTER infoclipper ->PATH: Project\Dataset\Clusters_CSV\original\infoclipper
    sorgenti2path=get_SRC_to_path(base_path)   


    #Il metodo crea un dizionario key value dove:
    #key->nome del sorgente (cluster)
    #value->lista dei (team,path_dataset) presenti in quel sorgente
    #ESEMPIO
    #companiesmarketcap [('00-avengers.csv', 'Project\\Dataset\\Clusters_CSV\\original\\00-avengers.csv'), ('01-DDD.csv', 'Project\\Dataset\\Clusters_CSV\\original\\01-DDD.csv')
    sorgenti2dataPaths=get_SRC_to_datasets(sorgenti2path)    #dizionario in cui, per ogni sorgente (cluster name) associamo una lista di tuple (nome team, path)
    


    
    
    #parsing dei dati
    
    #sorgenti2dataPaths=parse_data(sorgenti2path)

    parsed_data_path='Project\\Dataset\\ClusterParsed'


    #MODULE
    sorgenti2path_par=get_SRC_to_path(parsed_data_path)
       

    sorgenti2dataPaths_par=get_SRC_to_datasets(sorgenti2path_par)        
    

    #creazione del dizionario dei sinonimi
    create_sin_dic(sorgenti2path_par)


    
    


    
    