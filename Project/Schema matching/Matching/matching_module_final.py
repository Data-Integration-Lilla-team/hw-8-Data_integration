import os
from name_correlation_final import NameCorr
from data_cluster import ClusterData
import pandas as pd
from evaluator import Eval
import json

'''
Modulo responsabile della creazione dei dizionari di sinonimi.
Per lo scopo, implementa la seguente pipeline:
1. creazione di un dizionario preliminare di sinonimi mediante analisi della correlazione tra i nomi delle colonne DIZ 1
2. creazione di un dizionario preliminare di sinonimi mediante clusterizzazione delle colonne in base a feature predefinite DIZ 2
3. Unione dei dizionari DIZ 1, DIZ 2
4. Creazione del Dizionario dei sinonimi mediante utilizzo di Valentine
'''

class MatchingModule_final:

    def __init__(self,k):
        self.base_path=''
        self.path_destinazione='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari'

        self.inverted_index='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\inverted_index.txt'
        
        self.file_all_columns4ds='colonnePerdataset.txt'

        self.test_set='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\validation_set\\column_sinonimi.txt'

        

        #dove andranno tutte le elaborazioni

        self.path_sinonimus_dic=self.path_destinazione+'\\'+'column_sinonimi.txt'

         #prestazioni pre_valentine
        self.name_file_valutazione_pre_val='prestazione_pre_val.txt'
        self.path_file_valutazione_pre_val='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\prestazioni'+'\\'+self.name_file_valutazione_pre_val

        #dic_utlimato
        self.name_file_dic_sin_pre_val='dic_pre_val.txt'
        self.path_file_dic_sin_pre_val=self.path_destinazione+'\\'+self.name_file_dic_sin_pre_val


        #evaluation_dic
        self.name_file_evaluation_dic='confronto_dic_computato_e_target.txt'
        self.path_name_file_evaluation_dic=self.path_destinazione+'\\'+self.name_file_evaluation_dic




#per ogni dataset del sorgente, genera il suo path
#esempio:
#sorgente: disfold
#k 00-avengers.csv v Project\Dataset\Clusters_CSV\original\disfold\00-avengers.csv
#k 02-GioPonSpiz.csv v Project\Dataset\Clusters_CSV\original\disfold\02-GioPonSpiz.csv
#k 03-gren.csv v Project\Dataset\Clusters_CSV\original\disfold\03-gren.csv
#k 04-iGMM.csv v Project\Dataset\Clusters_CSV\original\disfold\04-iGMM.csv
    def get_files_name(self,elements):
        file_names=dict()
        for k in elements:
            name_file=k[0]
            path=k[1]
            file_names[name_file]=path                  
        
        return file_names


    def compute_max_clusters(self, file_names):
        attributes=set()
        for k in file_names.keys():
            path=file_names[k]
            df=pd.read_csv(path)
            cols=set(df.columns.values)
            attributes.update(cols)
        
        
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
        
        with open(self.test_set) as f:
            data=f.read()
            
        inverted_index=json.loads(data)

        return inverted_index
            


                

            
    def limit_names(self,unione,data_c):
        seen=set()
        out=[]
        for i in unione:
            if i not in seen:
                out.append(i)
            elements=data_c[i]
            seen.update(elements)
        return out


    def merge_dict(self, data_c, name_corr):
        output=dict()
        numero_colonne=len(data_c)
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
        eval=Eval()
        score=eval.eval_print(dic_name_correlation,validation_set)
        print('Punteggio jaccard name correlation',score)

        

        #calcola il numero di attributi da imporre come massimo per cluster
        #max cluster=max columns distinte
    ''' 
        max_clusters=self.compute_max_clusters(file_names)-1

        #computazione clustering data
        dataClustering=ClusterData(clusterName)
        print(clusterName)
        dic_data_clustering=dataClustering.clusterData(file_names,max_clusters,validation_set)


        #UNIONE DEI DIZIONARI COMPUTATI
        full_dic=self.merge_dict(dic_data_clustering,dic_name_correlation)
       
        evaluator=Eval()
        score=evaluator.evaluate(full_dic,validation_set)

        #STAMPA DELLE PERFORMANCE
        stringa='\nNUOVO GIRO'
        with open(self.path_file_valutazione_pre_val, 'a') as f:
            stringa=clusterName+' Score: '+str(score)+'\n'
            f.write(stringa)
        
        #STAMPA DEL DIZINARIO FULL
        stringa='\n'
        with open(self.path_file_dic_sin_pre_val, 'w') as f:
            
                
            f.write(json.dumps(full_dic))

        
        #VALUTAZIONE GENERALE
        evaluation_dic=evaluator.eval_cardinality(full_dic,validation_set)
        stringa='\n'
        avg_valori_extra=0
        somma=0
        div=len(evaluation_dic.keys())
        with open(self.path_name_file_evaluation_dic, 'w') as f:
            for k in evaluation_dic.keys():
                stringa=stringa+'Elemento: '+k+'\n'
                stringa=stringa+'Sinonimi computati:'+str(full_dic[k])+'\n'
                stringa=stringa+'Sinonimi reali:'+str(validation_set[k])+'\n'
                stringa=stringa+'Intersezione:'+str(evaluation_dic[k][0])+'\n'
                stringa=stringa+'Computato - TGT:'+str(evaluation_dic[k][1])+'\n'
                somma=somma+len(evaluation_dic[k][1])
                stringa=stringa+'TGT- Computato:'+str(evaluation_dic[k][2])+'\n'
                stringa=stringa+'Jaccard score:'+str(evaluation_dic[k][3])+'\n'
                
            avg_valori_extra=somma/div
            stringa=stringa+'AVG valori extra: ' +str(avg_valori_extra)+'\n'
            f.write(stringa)

    '''      


                    






        

        
        

        
        
           

            
