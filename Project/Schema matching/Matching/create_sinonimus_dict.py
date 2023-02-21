import pandas as pd
import os
import numpy as np
from matching_module import MatchingModule
from matching_module_final import  MatchingModule_final
from parsing_data import Parser_data
from Levenshtein import distance
import json

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
                            
                nameTeam=file
                filePath=os.path.join(Sorgenti2path[k],file)
                tupla=(nameTeam,filePath)
                list_of_files.append(tupla)
        
        Sorgenti2team[k]=list_of_files
    return Sorgenti2team


#parsing di dataset specidfici
def parse_spcific_data():
    parser=Parser_data()
    parser.parse_specific_values()

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
        
        cluster2newSRCDs[k]=[]
        for filename in os.listdir(sorgenti[k]):
            src=os.path.join(sorgenti[k],filename)
            final_path=os.path.join(tgt_dataset_parsed,k)
            final_path=os.path.join(final_path,filename)                     
            
            
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

#====================================================
#=============FUNZIONI PER LO SCHEMA FINALE==========
#====================================================
#creo una lista contentente di tuple (nome_file, path)
def get_SRC_to_path_final(path):
    final_dic=dict()
    lista_tuple_nomeFile_path=[]
    for f in os.listdir(path):
        file=os.path.join(path,f)
        tupla=(f,file)
        lista_tuple_nomeFile_path.append(tupla)
    final_dic['finale']=lista_tuple_nomeFile_path   
    return final_dic

#creazione del dizionario finale per la creazione dello schema mediato
def create_sin_dic_final(sorgenti2path_par,tokens):
    
    for k in sorgenti2path_par.keys():
        matcher=MatchingModule_final(k)
        print(k)
        print(sorgenti2path_par[k])
        matcher.create_dic_sin(sorgenti2path_par[k],k,tokens)  #la lista di tuple e un nome fake

def extract_cols(elements_path):
    import json
    with open(elements_path) as f:
        data = f.read()
    
    dictionary=json.loads(data)
    columns=dictionary.keys()
    return columns
    
        
def create_inverted_index_final(path):
    cluster_2_columns=dict()
    for f in os.listdir(path):
        cluster=str(f)
        cluster=cluster.replace('.txt','')
        print(cluster)
        path_sinonimi=os.path.join(path,f)
        
           
                
        columns=extract_cols(path_sinonimi)
        cluster_2_columns[cluster]=columns
        
    inverted_index=dict()
    for k in cluster_2_columns.keys():
        elements=cluster_2_columns[k]
        for e in elements:
            if e in inverted_index:
                inverted_index[e].append(k)
            else:
                inverted_index[e]=[]
                inverted_index[e].append(k)
    
    dictionary1 = sorted(inverted_index.items())
    return dict(dictionary1)
        
        
def update_diz(dizionario_gen,dizionario_sinonimi,cluster_name):
    
    for k in dizionario_sinonimi.keys():
        name_cluster=cluster_name+'-'+k
        if k not in dizionario_gen:
            dizionario_gen[k]=set(dizionario_sinonimi[k])
        else:
            print('aggiorno')
            dizionario_gen[k].update(dizionario_sinonimi[k])
            print(k,dizionario_gen[k])
    return dizionario_gen 

def create_dizionario_sinonimi_pregressi(path,dest):

    dizionario_pregressi_attuali=dict()
    clusters=os.listdir(path)
    for cluster in clusters:
        cluster_name=cluster
        print(cluster_name)
        path_sing_cluster=os.path.join(path,cluster_name)
        files=os.listdir(path_sing_cluster)
        for f in files:
            if f=='dizionario.txt':
                print('ok')
                path_diz=os.path.join(path_sing_cluster,f)
                with open(path_diz) as diz:
                    data=diz.read()
        print(data)

        sinonimi_correnti=json.loads(data)
        dizionario_pregressi_attuali=update_diz(dizionario_pregressi_attuali,sinonimi_correnti,cluster_name)  


    return dizionario_pregressi_attuali    
        

def create_token_list(dizionario_sinonimi_pregressi):
    from token_obj import Token_obj
    list_of_tokens=[]
    for k in dizionario_sinonimi_pregressi.keys():
        full_name=k
        sinonimi_pregressi=set(dizionario_sinonimi_pregressi[k])
        token=Token_obj(full_name,sinonimi_pregressi=sinonimi_pregressi)
        
        list_of_tokens.append(token) 
    return list_of_tokens
          
       


if __name__=='__main__':  
    
    #MATCHING MODULE PER CLUSTERS
    '''
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

    
    #parse_spcific_data()

    
    parsed_data_path='Project\\Dataset\\ClusterParsed'


    #MODULE per i cluster
    sorgenti2path_par=get_SRC_to_path(parsed_data_path)
       

    sorgenti2dataPaths_par=get_SRC_to_datasets(sorgenti2path_par)        
    

    #creazione del dizionario dei sinonimi
    #create_sin_dic(sorgenti2path_par)
    '''
    #MODULE finale
    parsed_data_path='Project\\Schema matching\\MySchemaMatching\\clusters\\schema'


    
    

    sorgenti2path_par=get_SRC_to_path_final(parsed_data_path) #per ogni .csv memorizzo (nome file, path)

    for k in sorgenti2path_par.keys():
        print(k,sorgenti2path_par[k])

    path_for_inverted_index='Project\\Schema matching\\MySchemaMatchingValentine\\clusters\\final_synonyms'
    path_for_dizionario_pregressi='Project\\Schema matching\\DatasetSchemaMatch'

    #INVERTED INDEX
    
    inverted_index_path='Project\\Schema matching\\MySchemaMatching\\files_matching\\files_vari\\inverted_index.txt'
    #create_inverted_index=create_inverted_index_final(path_for_inverted_index)
    
    #with open(inverted_index_path, 'w') as file:
    #    file.write(json.dumps(create_inverted_index)) 
    
    
    #



    #nuova features
    dest_dizionario_sinonimi_pregressi='Project\\Schema matching\\MySchemaMatching\\files_matching\\files_vari\\dizionario_sinonimi_pregressi.txt'

    dizionario_sinonimi_pregressi=create_dizionario_sinonimi_pregressi(path_for_dizionario_pregressi,dest_dizionario_sinonimi_pregressi)
    new_diz_preg=dict()
    for k in dizionario_sinonimi_pregressi.keys():
        new_diz_preg[k]=list(dizionario_sinonimi_pregressi[k])

    with open(dest_dizionario_sinonimi_pregressi,'w') as f:
        f.write(json.dumps(new_diz_preg,indent=4))


    tokens=create_token_list(dizionario_sinonimi_pregressi)
    #create_sin_dic_final(sorgenti2path_par,tokens)

    

    
   
     
    

