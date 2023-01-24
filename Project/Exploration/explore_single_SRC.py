
import pandas as pd
import os
import numpy as np
from parser_custom import Parser_custom
from Levenshtein import distance
class Explorer:
    def __init__(self):
        pass




    def write_infos_on_file(self,file,basePath,string):
        fileTGT=os.path.join(basePath,file)
        with open(fileTGT, 'w') as f:
    
            f.write(string)
#crea un dizionario composto da:
#1. nome team
#2. path del csv
    def get_files_name(self,base_path):
        file_names=dict()                  
        for f in os.listdir(base_path):
            file=os.path.join(base_path,f)
            if os.path.isfile(file):
                if '.' not in file:
                    file_names[f]=file

        return file_names

    def get_col_4_files(self,files):

        col_4_team=dict()
        for team, path in files.items():

            team_name=team
            path_ds=files[team]
            print(path_ds)
            data=pd.read_csv(path_ds)

            parser=Parser_custom(path_ds)
            columns=data.columns
        
            columns=parser.parse(columns)    #eliminaimo gli unamed columns

            col_4_team[team_name]=columns


        return col_4_team

    def create_inverted_index(self,cols4file):
        inverted_index=dict()
        for k in cols4file.keys():
            elements=cols4file[k]
            for e in elements:
                if e in inverted_index:
                    inverted_index[e].append(k)
                else:
                    inverted_index[e]=[k]
        
        return inverted_index

    def correlation_metrix_Levi(self,inverted_index):
        list_of_tokens=sorted(inverted_index.keys())
        

        List1 = list_of_tokens
        List2 = list_of_tokens

        #Matrix = np.zeros((len(List1),len(List2)),dtype=np.int_)
        correlazione=dict()

        for i in range(0,len(List1)):
            correlazione[List1[i]]=[]
            for j in range(0,len(List2)):
                compute_dist=distance(List1[i],List2[j])
                print('eval',List1[i],List2[j],'->',compute_dist)
                
                correlazione[List1[i]].append(distance(List1[i],List2[j]))

        
        matrice_correlazione=pd.DataFrame(data=correlazione,columns=list_of_tokens,index=list_of_tokens)


        return matrice_correlazione
    
    import ngram
    
    def compute_sim_ngrams(inverted_index):
        N=3
        list_of_tokens=sorted(inverted_index.keys())
    

        List1 = list_of_tokens
        List2 = list_of_tokens

        #Matrix = np.zeros((len(List1),len(List2)),dtype=np.int_)
        correlazione=dict()

        for i in range(0,len(List1)):
            correlazione[List1[i]]=[]
            for j in range(0,len(List2)):
                element1=List1[i]
                element2=List2[j]
            
                
                compute_dist=ngram.NGram.compare(element1,element2)
                print('eval',List1[i],List2[j],'->',compute_dist)
            
                correlazione[List1[i]].append(compute_dist)

    
        matrice_correlazione=pd.DataFrame(data=correlazione,columns=list_of_tokens,index=list_of_tokens)

        return matrice_correlazione


    def explore_single_data(self, base_path, src):

        base_path=base_path

        file_all_columns4ds='colonnePerdataset.txt'

        file_inverted_index='indice_invertito.txt'

        file_matrice_correlazione='matrice_correlazioneLevinstein.txt'

        

        files_name=self.get_files_name(base_path)
        print(files_name)

        #compute columns: per ogni file definiamo le colonne
        col4file=self.get_col_4_files(files_name)
        string=''
        #preparazioen stringa da scrivere
        for k in col4file.keys():
            string=string+'TEAM:'+k+'-> COLS: '+ str(col4file[k])+'\n'

        self.write_infos_on_file(file_all_columns4ds,base_path,string)

        #creazione di un indice invertito dove andiamo ad inserire nome_colonna->doc
        print('inverted index')
        inverted_index=self.create_inverted_index(col4file)

        #crittura su file
        string=''
        for k in sorted(inverted_index):
            string=string+ k+'->'+str(inverted_index[k])+'\n'
        
        self.write_infos_on_file(file_inverted_index,base_path,string)

        correlation_matrix_levi=self.correlation_metrix_Levi(inverted_index)

        correlation_matrix_levi.to_csv(os.path.join(base_path,file_matrice_correlazione))




        
            
            
