'''
modulo per la claterizzazione
'''
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class ClusterModel:
    def __init__(self,cluster_name):
        self.clusterName=cluster_name
        
        self.path_destinazione='Project\\Schema matching\\DatasetSchemaMatch\\'+self.clusterName

   
    def clustered_data_explor(self,data,columns,max_clusters=14):
        ss=[]
        
        for k in range(1,max_clusters+1):
            km=KMeans(init='k-means++',n_clusters=k)
            km.fit(data[columns])
            ss.append(km.inertia_)
            
        

        
        for k in range(1,max_clusters):
            
            print(k,'->','SSE',ss[k])


        plt.xlabel('K')
        plt.ylabel('SSE')
        plt.plot(ss)
        plt.show()


    def clustered_data(self,data,columns,max_clusters=14):
       
            km=KMeans(n_clusters=max_clusters)
            km.fit(data[columns])
            data['cluster']=km.fit_predict(data[columns])

            return data

        
