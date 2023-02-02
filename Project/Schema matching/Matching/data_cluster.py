'''
classe specializzata nella clusterizzazione delle colonne di un sorgente
Ogni colonna dei diversi ds di un sorgente vengono codificati in un vettore di features.
Il vettore di features è il seguente:
#nome campo
    #1. tipo di dato: string 0, int 1, data (?)
    #2. (string)type of str->perc_:1, b or t or doll_: 2, rank_=3, other=4
    #3. (string)avg_lenght of fiald (if string)
    #4. (string)variance of lenght
    #5. (string) std deviation of lenght
    #6. (string)ratio of whitespace fields
    #7. (string)ratio of numeric values
    #8. (int)min val
    #9. (int)max val
    #10. (int)avg
    #11 (int)variance
    #12 (int) std deviation

Si clasterizzano le colonne utilizzando l'algoritmo k_means

'''
import pandas as pd
from feature_engineering_columns import FeatureExtraction
from clusterModel import ClusterModel
class ClusterData:
    def __init__(self,clusterName):
    #base path
        self.cluster=clusterName
        self.path_destinazione='Project\\Schema matching\\DatasetSchemaMatch\\'+clusterName

        #dataset
        self.dataset='ds_features.csv'
        self.path_dataset=self.path_destinazione+'\\'+self.dataset

        #dataset_normalizzato
        self.dataset_norm='ds_features_norm.csv'
        self.path_dataset_norm=self.path_destinazione+'\\'+self.dataset_norm



    #crea il dataset per il cluster

    def create_dataset(self,files):
        
        team2feature=dict()
        print('Creating dataset of features')
        for k in files.keys():
            feature_extractor=FeatureExtraction()
            path=files[k]
            data=pd.read_csv(path)
            team=k.replace('.csv','')
            print(team)
            
            team2feature[team]=feature_extractor.extract_feature(data,team)

        dataset=feature_extractor.create_pandas_dataframe(team2feature)

        dataset=dataset.fillna(0)
        dataset.to_csv(self.path_dataset)

        
        dataset_norm=feature_extractor.get_scaled_dataframe(dataset).fillna(0)

        dataset
        return dataset_norm

      #eliminazione delle conolle Unnamed
    def drop_not_needed_cols(self,data):
        print('Name columns bf:',data.columns)
        data.columns.str.startswith('Unnamed')
        
        data=data.loc[:,~data.columns.str.startswith('Unnamed')]
        print('Name columns af:',data.columns)
        return data   
            
            



    #per ogni file presente nel cluster,
    #1 estraiamo le features
    #2 inseriamo in un dataframe pandas
    #3 clusterizziamo
    def clusterData(self, files,max_clusters,validation_set):
        dataset=self.create_dataset(files)          #creazione del dataset di features

        dataset.to_csv(self.path_dataset_norm)
        dataset=self.drop_not_needed_cols(dataset)
        clusterModel=ClusterModel(self.cluster)
        columns=list(dataset.columns)
        columns.pop(0)
        print(columns)
        dataClustered=clusterModel.clustered_data_explor(dataset,columns,validation_set,max_clusters=max_clusters)

        if 'symbol' in dataClustered:
            print(dataClustered['symbol'])

        return dataClustered



        
        
            
            

        
