import pandas as pd
from parser_c import Parser_custom
import os
'''
Classe specializzata nel rinominare i nomi delle colonne dei dataset
'''
class Rename_columns:

    def __init__(self):
        self.final_path='Project\\Dataset\\Clusters_CSV\\parsed\\'

    #rename column->per ogni ds di un cluster rinonimiamo i nomi delle colonne in modo tale da avere uno schema univoco.
    #trasformazione->1. row name to parsed name
    #                2. parsed name to unified name

    #prende in input un ds e ed il dizionario dei nomi unificati e rinomina le colonne.

    def rename_ds(self,ds,column_dic,path):
        extension='.csv'
        new_ds=ds.rename(columns={column_dic})
        new_ds.to_csv(path+extension)
        return new_ds

    #parsing delle colonne ed eliminazione di quelle inutili
    def get_ds_4_team(self,files, base_path):

        col_4_team=dict()
        for team, path in files.items():
            
            
            team_name=team
            path_ds=files[team]
            
            data=pd.read_csv(path_ds)

            parser=Parser_custom(path_ds)
            columns=data.columns

            
            columns=parser.parse_column_for_merge(columns)    #restituisce un dizionario avente vecchio nome colonna e nuovo
            

            data.rename(columns=columns,inplace=True)
            data=data.drop(['Unnamed: 0.1','Unnamed: 0'],axis=1,errors='ignore')
           
            col_4_team[team_name]=data
            name_file=team_name+'_col_parsed.csv'
            final_path=os.path.join(base_path,name_file)
            data.to_csv(final_path)


        return col_4_team