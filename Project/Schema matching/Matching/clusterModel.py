'''
modulo per la claterizzazione
'''
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from evaluator import Eval
import pandas as pd


class ClusterModel:
    def __init__(self,cluster_name):
        self.clusterName=cluster_name
        
        self.path_destinazione='Project\\Schema matching\\DatasetSchemaMatch\\'+self.clusterName
        
        #nome ds con cluster
        self.nome_file_ds_cluster='clustered_rows.csv'
        self.path_cluster=self.path_destinazione+'\\'+self.nome_file_ds_cluster

        #nome file diversi dizionari
        self.nome_file_dic_sin='dic_sin_4_cluster.txt'
        self.path_nome_file_dic_sin=self.path_destinazione+'\\'+self.nome_file_dic_sin
        
    #formattazione del nome del campo
    #INPUT->02-GioPonSpiz-name
    #OUTPUT->name
    def format_name_col(self, name):
        
        elements=name.split('-')
        col_name=elements[len(elements)-1]
        
        return col_name

    def evalBestK(self, scores):
        best=0
        thresh=0
        for k in scores.keys():
            score=scores[k]
            if score>best:
                best=score
                thresh=k
            
        return (best,thresh)

    #per ogni record evvettua una aggregazione in base al cluster di appartenenza
    def aggregate_columns_by_clusters(self,data_used):
        cluster_2_columns=dict()
        for e in data_used.iterrows():
            col_name=self.format_name_col(e[1][0])
           
            elem_type=e[1][1]
            
            
            if elem_type not in cluster_2_columns:
                cluster_2_columns[elem_type]=set()
            
            cluster_2_columns[elem_type].add(col_name)
        return cluster_2_columns


    #creazione del dizionario.
    #per ogni entry del dizionario di aggrefazione, creiamo una entry per ogni singolo elemento nella colonna
    #esempio
    #INPUT
    #Cluster->[col1,col2,col3]
    #OUTPUT
    #col1:{col1,col2,col3}
    def compute_dic_sin(self, cluster_2_columns):
        dic_sin=dict()
        for k in cluster_2_columns.keys():
            elements=cluster_2_columns[k]
            for e in elements:  #per ogni nome di colonna
                dic_sin[e]=list(elements)

        
        return dic_sin



    #aggrega le colonne in base ai cluster di appartenenza
    #crea il dizionario dei sinonimi
    def create_sin_dic(self,clusters):
        data_used=clusters[['column_name','cluster']]
        
        cluster_2_columns=self.aggregate_columns_by_clusters(data_used)
        
           
        dic_2_sin=self.compute_dic_sin(cluster_2_columns)
        
        
            
        

        return dic_2_sin
        
        
            
    def save_infos_kmeans(self,stringa,clusters):
        clusters.to_csv(self.path_cluster)
        with open(self.path_nome_file_dic_sin, 'w') as f:
    
            f.write(stringa)

    def clustered_data_explor(self,data,columns,validation,max_clusters=14):
        ss=[]
        jaccard_dist_eval=dict()
        eval=Eval()
        stringa=''
        
        for k in range(2,max_clusters+1):
            stringa=stringa+'N.Clusters'+str(k)
            used_data=pd.DataFrame(data,columns=data.columns)
            print(used_data.columns)
            km=KMeans(init='k-means++',n_clusters=k)
            km.fit(data[columns])
            used_data['cluster']=km.fit_predict(data[columns])
            
            dic_sin=self.create_sin_dic(used_data)

            
            score=eval.evaluate(dic_sin,validation)
            print('cluster k=',k,'score.>',score)
            jaccard_dist_eval[k]=score
            stringa=stringa+'avg jaccard: '+str(score)+'Inertia: '+str(km.inertia_)+'\n'
            for i in dic_sin.keys():
                stringa=stringa+i+'->'
                for e in dic_sin[i]:
                    stringa=stringa+str(e)+', '
                stringa=stringa+'\n'
            stringa=stringa+'\n'

            ss.append(km.inertia_)

        best_K=self.evalBestK(jaccard_dist_eval)[1]
        best_result=self.clustered_data(data,columns,best_K)
        ds_csv=best_result[1]
        dic_sin_best=best_result[0]

        self.save_infos_kmeans(stringa,ds_csv)
        

        #for k in range(2,len(ss)):
            
            #print(k,'->','SSE',ss[k])


        #qui il salvataggio della img su file
        #plt.xlabel('K')
        #plt.ylabel('SSE')
        #plt.plot(ss)
        #plt.show()

        return dic_sin_best


    def clustered_data(self,data,columns,max_clusters=14):
       
            km=KMeans(n_clusters=max_clusters)
            km.fit(data[columns])
            data['cluster']=km.fit_predict(data[columns])
            
            dic_sin=self.create_sin_dic(data)

            return (dic_sin,data)

        
