import os
from name_correlation import NameCorr
from data_cluster import ClusterData
import pandas as pd

'''
Modulo responsabile della creazione dei dizionari di sinonimi.
Per lo scopo, implementa la seguente pipeline:
1. creazione di un dizionario preliminare di sinonimi mediante analisi della correlazione tra i nomi delle colonne DIZ 1
2. creazione di un dizionario preliminare di sinonimi mediante clusterizzazione delle colonne in base a feature predefinite DIZ 2
3. Unione dei dizionari DIZ 1, DIZ 2
4. Creazione del Dizionario dei sinonimi mediante utilizzo di Valentine
'''

class MatchingModule:

    def __init__(self,k):
        self.base_path=''

        self.file_all_columns4ds='colonnePerdataset.txt'

        self.file_inverted_index='indice_invertito.txt'

        self.path_destinazione='Project\\Schema matching\\DatasetSchemaMatch\\'+k         #dove andranno tutte le elaborazioni

#per ogni dataset del sorgente, genera il suo path
#esempio:
#sorgente: disfold
#k 00-avengers.csv v Project\Dataset\Clusters_CSV\original\disfold\00-avengers.csv
#k 02-GioPonSpiz.csv v Project\Dataset\Clusters_CSV\original\disfold\02-GioPonSpiz.csv
#k 03-gren.csv v Project\Dataset\Clusters_CSV\original\disfold\03-gren.csv
#k 04-iGMM.csv v Project\Dataset\Clusters_CSV\original\disfold\04-iGMM.csv
    def get_files_name(self,base_path):
        file_names=dict()                  
        for f in os.listdir(base_path):
            file=os.path.join(base_path,f)
            if os.path.isfile(file):
                
                    file_names[f]=file
        return file_names


    def compute_max_clusters(self, file_names):
        attributes=set()
        for k in file_names.keys():
            path=file_names[k]
            df=pd.read_csv(path)
            cols=set(df.columns.values)
            attributes.update(cols)
        
        print(attributes)
        print(len(attributes))
        return len(attributes)





    #riceve in input:
    #Nome sorgente
    #lista di tuple (nome team, path dataset)
    #restituisce il dizionario calcolato dei sinonimi
    def create_dic_sin(self,path_cluster, clusterName):
        
        file_names=self.get_files_name(path_cluster)
        #computazione della name correlation
        nameCorr=NameCorr(clusterName)
        #nameCorr.computeCorr(file_names)

        #calcola il numero di attributi da imporre come massimo per cluster
        #max cluster=max columns distinte
        max_clusters=self.compute_max_clusters(file_names)-1

        #computazione clustering data
        dataClustering=ClusterData(clusterName)
        print(clusterName)
        dataClustering.clusterData(file_names,max_clusters)





        

        
        

        
        
           

            
