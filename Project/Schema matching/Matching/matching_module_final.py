import os
from name_correlation_final import NameCorr
from data_cluster_final import ClusterData
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

        self.threshold_max_par=4.5   #massimo numero di cluster
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

        #valutazione
        self.name_file_evaluation_dic_matrix='data_and_name_dic_sin_union.csv'
        self.path_name_file_evaluation_dic_matric=self.path_destinazione+'\\'+self.name_file_evaluation_dic_matrix

        #dic sinonimi name correlation
        self.name_file_dic_sin_name_correlatio='dizionario_sinonimi_name_correlation.txt'
        self.path_dic_sin_name_correlation=self.path_destinazione+'\\'+self.name_file_dic_sin_name_correlatio

        #dic sinonimi data clustering
        self.name_file_dic_sin_data_clustering='dizionario_sinonimi_data_clustering.txt'
        self.path_dic_sin_data_clustering=self.path_destinazione+'\\'+self.name_file_dic_sin_data_clustering

        #valutazione name correlation
        self.name_file_valutazione_name_corr='name_correlation_valutazione.csv'
        self.path_name_file_valutazione_name_corr=self.path_destinazione+'\\'+self.name_file_valutazione_name_corr

        #valutazione data correlation
        self.name_file_valutazione_data_clustering='data_clustering_valutazione.csv'
        self.path_name_file_valutazione_data_clustering=self.path_destinazione+'\\'+self.name_file_valutazione_data_clustering

        


        #tempi
        self.name_file_tempi='tempi.txt'
        self.path_name_file_tempi=self.path_destinazione+'\\'+self.name_file_tempi




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


    def compute_max_clusters(self, validation_set):
        return len(validation_set.keys())
       



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

    def filter_extra_data(self, computed, validation):
        out=dict()
        for k in validation.keys():
            out[k]=list(computed[k])

        return out 

    def compute_dic_name_correlation(self,tokens,validation_set,clusterName):
        nameCorr=NameCorr(clusterName)
        from timeit import default_timer as timer

        
        #versione vecchia (name correlation tradizionale, senza token con memoria)
        #dic_name_correlation=nameCorr.computeCorr(file_names,validation_set)
        
        
        start = timer()
        dic_name_correlation_token=nameCorr.computeCorrTokens(tokens,validation_set)
        end=timer()
        with open(self.path_name_file_tempi,'a') as f:
            stringa='Name correlation: '+str(end-start)+'\n'
            f.write(stringa)

        val=Eval()
        valutazione_name_correlation=val.compute_dis_f1(dic_name_correlation_token,validation_set)
        valutazione_name_correlation.to_csv(self.path_name_file_valutazione_name_corr)
        

        dic_name_correlation_fitered=self.filter_extra_data(dic_name_correlation_token,validation_set)

        
        with open(self.path_dic_sin_name_correlation,'w') as f:
            f.write(json.dumps(dic_name_correlation_fitered))

        return dic_name_correlation_fitered


    def compute_dic_data_clustering(self,file_names,validation_set,clusterName):
        #calcola il numero di attributi da imporre come massimo per cluster
        #max cluster=max columns distinte
        print('DATA CORRELATION')
        from timeit import default_timer as timer
        max_clusters=int(self.compute_max_clusters(validation_set)*self.threshold_max_par)
        print('CLUSTER DA ANALIZZARE:',max_clusters)

        #computazione clustering data
        dataClustering=ClusterData(clusterName)
        print('CLUSTER NAME:',clusterName)
        start=timer()
        dic_data_clustering=dataClustering.clusterData(file_names,max_clusters,validation_set)
        end = timer()
        with open(self.path_name_file_tempi,'a') as f:
            stringa='Data correlation: '+str(end-start)+'\n============\n'
            f.write(stringa)
        
        val=Eval()
        valutazione_name_correlation=val.compute_dis_f1(dic_data_clustering,validation_set)
        valutazione_name_correlation.to_csv(self.path_name_file_valutazione_data_clustering)
        

        dic_data_correlation_fitered=self.filter_extra_data(dic_data_clustering,validation_set)
        print(dic_data_correlation_fitered)

        with open(self.path_dic_sin_data_clustering,'w') as f:
            f.write(json.dumps(dic_data_correlation_fitered,indent=4))


        
        return dic_data_correlation_fitered
       

            
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
        for k in data_c.keys():
            elementi_A=set(data_c[k])
            elementi_B=set(name_corr[k])
            unione=list(elementi_A.union(elementi_B))
            
            output[k]=unione
        
        return output

    def get_tot_colonne(self,file_names):
        totale=0
        for k in file_names.keys():
            path=file_names[k]
            data=pd.read_csv(path)
            colonne=list(data.columns.values)
            totale+=len(colonne)
        return totale

    #riceve in input:
    #Nome sorgente
    #lista di tuple (nome team, path dataset)
    #restituisce il dizionario calcolato dei sinonimi
    def create_dic_sin(self,path_cluster, clusterName,tokens):
        validation_set=self.create_validation_sic_dic()         #acquisizioine del file .txt 'column_sinonimi.txt' e conversione in dizionario

        
        file_names=self.get_files_name(path_cluster)
        
        #info precalolata->178
        #totale_colonne=self.get_tot_colonne(file_names)
        #print(totale_colonne) 178
        
        

        evaluator=Eval()
        #name correlation_with tokens
        #dic_name_correlation_token=self.compute_dic_name_correlation(tokens,validation_set,clusterName)
        with open(self.path_dic_sin_name_correlation,'r') as f:
            data=f.read()

        dic_name_correlation_token=json.loads(data)
        valutazione_name_correlation=evaluator.compute_dis_f1(dic_name_correlation_token,validation_set,178)
        valutazione_name_correlation.to_csv(self.path_name_file_valutazione_name_corr)
        

        #data clustering
        #dic_data_clustering=self.compute_dic_data_clustering(file_names,validation_set,clusterName)

        with open(self.path_dic_sin_data_clustering,'r') as f:
            data=f.read()

        dic_data_clustering=json.loads(data)
        valutazione_name_correlation=evaluator.compute_dis_f1(dic_data_clustering,validation_set,178)
        valutazione_name_correlation.to_csv(self.path_name_file_valutazione_data_clustering)
        
        #UNIONE DEI DIZIONARI COMPUTATI
        full_dic=self.merge_dict(dic_data_clustering,dic_name_correlation_token)
       
        
        final_score=evaluator.compute_dis_f1(full_dic,validation_set,178)
        final_score.to_csv(self.path_name_file_evaluation_dic_matric)

        #STAMPA DEL DIZINARIO FULL
        stringa='\n'
        with open(self.path_file_dic_sin_pre_val, 'w') as f:    
            f.write(json.dumps(full_dic,indent=4))

        
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
                stringa=stringa+'Precision: '+str(evaluation_dic[k][3])+'\n'
                stringa=stringa+'Recall: '+str(evaluation_dic[k][4])+'\n'
                stringa=stringa+'F1:'+str(evaluation_dic[k][5])+'\n'
                stringa=stringa+'Jaccard score:'+str(evaluation_dic[k][6])+'\n'
                stringa=stringa+'Confronti reali'+str(evaluation_dic[k][7])+'\n'
                
                stringa=stringa+'Confronti totali'+str(evaluation_dic[k][8])+'\n'
                inutili=evaluation_dic[k][8]-evaluation_dic[k][7]
                stringa=stringa+'Confronti reali'+str(inutili)+'\n'
                stringa=stringa+'========================\n'
                
            avg_valori_extra=somma/div
            stringa=stringa+'AVG valori extra: ' +str(avg_valori_extra)+'\n'
            f.write(stringa)




                    






        

        
        

        
        
           

            
