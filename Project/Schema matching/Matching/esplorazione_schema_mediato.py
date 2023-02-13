import pandas as pd
import os
def get_name_cols_string(file):
    ds=pd.read_csv(file)
    ds=ds[['column_name','type_of_data']]
    ds_to_cols=dict()
    for _,row in ds.iterrows():
        name_att=row['column_name'].split('-')
        
        src=name_att[0]
        print('src:',src)
        campo=name_att[1]
        print(row['type_of_data'])
        if row['type_of_data']==0:
            if src not in ds_to_cols:
                ds_to_cols[src]=[]
            ds_to_cols[src].append(campo)

    return ds_to_cols
def get_monetary_columns(file,list_cols,src):
    data=pd.read_csv(file)
    print(data.columns.values)
    data=data[list_cols]
    
    search_string='doll_'
    
    cols=data.columns[data.apply(lambda x: x.str.contains(search_string).any())]
    data=data[cols]
    path_save='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\dati_monetari\\'+src+'.csv'
    data.to_csv(path_save)
    
    
if __name__=='__main__':
    path_datasets='Project\\Schema matching\\SchemaMatchingValentine\\clusters\\schema'
    ds_features='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\ds_features.csv'
    moneta_symbol='doll_'
    lista_tuple_nomeFile_path={}
    
    string_col_to_ds=get_name_cols_string(ds_features)
    
    to_searc=set(string_col_to_ds.keys())
    print(to_searc)
    for f in os.listdir(path_datasets):
        
            
            file=os.path.join(path_datasets,f)
            name=str(f).replace('.csv','')
            print(file)
            print(name)
            if name in to_searc:
                print('ok')
                print(string_col_to_ds[name])
                lista_tuple_nomeFile_path[f]=get_monetary_columns(file,string_col_to_ds[name],name)
