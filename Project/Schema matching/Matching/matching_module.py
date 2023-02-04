import os
from name_correlation import NameCorr
from data_cluster import ClusterData
import pandas as pd
from evaluator import Eval

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

        self.path_sinonimus_dic=self.path_destinazione+'\\'+'column_sinonimi.txt'

         #prestazioni pre_valentine
        self.name_file_valutazione_pre_val='prestazione_pre_val.txt'
        self.path_file_valutazione_pre_val='Project\\Schema matching\\Matching'+'\\'+self.name_file_valutazione_pre_val

        #dic_utlimato
        self.name_file_dic_sin_pre_val='dic_pre_val.txt'
        self.path_file_dic_sin_pre_val=self.path_destinazione+'\\'+self.name_file_dic_sin_pre_val


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



    def create_list_from_vect(self, values):
        values=values.replace('[','')
        values=values.replace(']','')
        values=values.replace("\n","")
        values=values.replace("'","")
        values=values.replace('"','')
        values=values.replace(" ",'')
        
        

        values=values.split(',')
        values.pop(len(values)-1)
        return values

    def create_validation_sic_dic(self):
        d = {}
        with open(self.path_sinonimus_dic) as f:
            for line in f:
                if '{' not in line and '}' not in line:
                    elementi= line.split(':')
                    key=elementi[0]
                    values=elementi[1]
                    
                    list_val=self.create_list_from_vect(values)
                    d[key]=list_val

            
            for k in d.keys():
                if len(d[k])==0:
                    print('errore')
        
        return d


                

            


    def merge_dict(self, data_c, name_corr):
        output=dict()
        for k in data_c.keys():
            elementi_A=set(data_c[k])
            elementi_B=set(name_corr[k])
            unione=list(elementi_A.union(elementi_B))
            output[k]=unione
        return output
    #riceve in input:
    #Nome sorgente
    #lista di tuple (nome team, path dataset)
    #restituisce il dizionario calcolato dei sinonimi
    def create_dic_sin(self,path_cluster, clusterName):

        validation_set=self.create_validation_sic_dic()         #acquisizioine del file .txt 'column_sinonimi.txt' e conversione in dizionario

        
        file_names=self.get_files_name(path_cluster)
        #computazione della name correlation
        print(clusterName)
        nameCorr=NameCorr(clusterName)
        dic_name_correlation=nameCorr.computeCorr(file_names,validation_set)
        #for k in dic_name_correlation.keys():
        #   print(k,dic_name_correlation[k])

        #calcola il numero di attributi da imporre come massimo per cluster
        #max cluster=max columns distinte
        max_clusters=self.compute_max_clusters(file_names)-1

        #computazione clustering data
        dataClustering=ClusterData(clusterName)
        print(clusterName)
        dic_data_clustering=dataClustering.clusterData(file_names,max_clusters,validation_set)

        full_dic=self.merge_dict(dic_data_clustering,dic_name_correlation)
        print(full_dic)
        evaluator=Eval()
        score=evaluator.evaluate(full_dic,validation_set)

        stringa='\nNUOVO GIRO'
        with open(self.path_file_valutazione_pre_val, 'a') as f:
            stringa=clusterName+' Score: '+str(score)+'\n'
            f.write(stringa)
        
        stringa='\n'
        with open(self.path_file_dic_sin_pre_val, 'w') as f:
            for k in full_dic.keys():
                stringa=stringa+k+'->'+str(full_dic[k])+'\n'
            f.write(stringa)







        

        
        

        
        
           

            
