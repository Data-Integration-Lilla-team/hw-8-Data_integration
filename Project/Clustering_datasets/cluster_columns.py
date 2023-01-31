import pandas as pd
import os
from parser_c import Parser_custom
from rename_columns_ds import Rename_columns
from feature_engineering_columns import FeatureExtraction
from clusterModel import ClusterModel


def cluster_columns():
    pass
#crea un dizionario composto da:
#1. nome team
#2. path del csv
def get_file_names(base_path):
    file_names=dict()                  
    for f in os.listdir(base_path):
        file=os.path.join(base_path,f)
        if os.path.isfile(file):
            if '.' not in file:
                file_names[f]=file
    

    return file_names


    

   
def get_col_4_files(files):

    col_4_team=dict()
    for team, path in files.items():

        team_name=team
        path_ds=files[team]
        
        data=pd.read_csv(path_ds)

        parser=Parser_custom(path_ds)
        columns=data.columns
        
        columns=parser.parse(columns)    #eliminaimo gli unamed columns

        col_4_team[team_name]=columns


    return col_4_team

def create_inverted_index(cols4file):
    inverted_index=dict()
    for k in cols4file.keys():
        elements=cols4file[k]
        for e in elements:
            if e in inverted_index:
                inverted_index[e].append(k)
            else:
                inverted_index[e]=[k]
    
    return inverted_index


if __name__=='__main__':

    #1. parsing colonne->unifichiamo il nome delle colonne
    base_path='Project\\Dataset\\Clusters\\companiesmarketcap'
    final_path='Project\\Dataset\\Clusters_CSV\\parsed\\companiesmarketcap\\'
    file_names=get_file_names(base_path)
        #compute columns: per ogni file definiamo le colonne
    col4file=get_col_4_files(file_names)
    string=''
  

     #creazione di un indice invertito dove andiamo ad inserire nome_colonna->doc
    
    inverted_index=create_inverted_index(col4file)


    



    #dizionario dei nomi delle colonne
    dizionarioSinonimi=dict()

    dizionarioSinonimi={ 
            "categories":["categories"],
            "change_1_day":['change1d','change_1_day','change_1day'],
            "change_1_year":['change1y','change_1_year','change_1year'],
            "company_code":['code','codice','company_code','symbol'],
            "country":['country'],
            "earnings":['earnings'],
            "employees":['employees'],
            "market_cap":['market_cap','market_capitalization_usd','marketcap','master_cap','pricecap'],
            "name":['name'],
            'share_price':['price','share_price','shareprice'],
            "rank":['rank'],
            "revenue":['revenue'],
            "shares":['shares'],
            "url":['url']

        }
    rename_cols=Rename_columns()
    team2ds=rename_cols.get_ds_4_team(file_names,final_path)

    for k in team2ds.keys():
        print('dataset:',k,' colonne', team2ds[k].columns)

    pars_values=Parser_custom(None)
    feature_extr=FeatureExtraction()
    team2feature=dict()
    for k in team2ds.keys():

        ds=pars_values.parse_data_values(team2ds[k])              #parsing dei valori
        name_file=k+'_col_val_parsed.csv'
        final_path_file=os.path.join(final_path,name_file)
        print('team:',k ,final_path)
        
        ds.to_csv(final_path_file)
        print(ds.columns.values)
   
        team2feature[k]=feature_extr.extract_feature(ds,k)

    columns=feature_extr.get_features_name()
    print(columns)

    '''print('len cols',len(columns))
    for k in team2feature.keys():
        print('len list of cols',len(team2feature[k]))
        for e in team2feature[k]:
            print('len col:',len(e))'''
    dataset=feature_extr.create_dataset(team2feature,columns)

    print('Not_normalized_data\n',dataset.head(10))

    dataset_norm=feature_extr.get_scaled_dataframe(dataset)

    
    print('Normalized_data\n',dataset_norm.head(10))

    cluster_model=ClusterModel()

    columns_to_use=columns.pop(0)
    
    dataClustered=cluster_model.clustered_data(dataset_norm,columns,len(dizionarioSinonimi.keys()))


    name='clustered_rows.csv'
    file_name=final_path+name

    dataClustered.to_csv(file_name)
    
    clusters=pd.from_csv(file_name)
    


    

    

    
        
    
                
                



    





    
    
