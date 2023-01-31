'''
Momentanea
classe responsabile per il parsing dei dati

metodo principale->parse_source

riorganizzazione nomi delle colonne
riorganizzazinoe valori delle colonne
'''
import os
import pandas as pd

class Parser_data:


    def __init__(self):
        pass



    #metodo generico di trasformazione del nome delle colonne.
    # incaso di parser specifici, si invoca questo metodo che a sua volta, in base al nome del cluster passato, invoca un metodo specifico   
    def compute_new_column_name(self,columns):

        oldName2NewName=dict()
        cols=list(columns)
       
        to_filter_col='Unnamed:'
        for c in cols:
            if to_filter_col not in c:
                c_new=c.lower()             #tutto in lower case
                c_new=c_new.replace('(','_')
                c_new=c_new.replace(')','')
                c_new=c_new.replace(' ','_')
                c_new=c_new.replace('-','_')
            
                oldName2NewName[c]=c_new
           
        return oldName2NewName


    #eliminazione delle conolle Unnamed
    def drop_not_needed_cols(self,data):
        print('Name columns bf:',data.columns)
        data.columns.str.startswith('Unnamed')
        
        data=data.loc[:,~data.columns.str.startswith('Unnamed')]
        print('Name columns af:',data.columns)
        return data


    #specializzato nel parsing dei nomi delle colonne
    def parse_column_name(self, data, path_tgt):
        
        data_cols=data.columns
        oldCols2newCols=self.compute_new_column_name(data_cols)
        data.rename(columns=oldCols2newCols,inplace=True)

        data=self.drop_not_needed_cols(data)
        data.to_csv(path_tgt)

    
    #specializzato nel parsing e cleaning dei valori del ds
    def parse_values(self,data,path_tgt):
        
        dic_to_replace=dict()
        dic_to_replace={'%':'_perc',
                        '#':'rank_',
                        '\$': 'doll_',
                        '\r\n': ' '
        }
        columns=data.columns
        cols_to_lower_case=[]
        import re

       
        #ds=ds.fillna(0)
        for c in columns:
            
            data[c]=data[c].replace(dic_to_replace,regex=True)
            if isinstance(data[c].head(1)[0], str):
                data[c]=data[c].str.lower()


        data=self.drop_not_needed_cols(data)
        data.to_csv(path_tgt)

    #riceve in input il path src del dataset da parsare
    #parsa il dataset e lo memorizza nel path path_tgt
    def parse_data(self,path_src, path_tgt):
        data=pd.read_csv(path_src)

        self.parse_column_name(data,path_tgt)
        data=pd.read_csv(path_tgt)
        self.parse_values(data,path_tgt)
        #nuovo dataset con colonne nuove
        
        
        
        


    #parsing delle colonne ed eliminazione di quelle inutili

    
 


        

        
            


    
    
    def parse_data_values(self,ds):
        dic_to_replace=dict()
        dic_to_replace={'%':'_perc',
                        
                        
                        '#':'rank_',
                        '\$': 'doll_'
        }
        columns=ds.columns
        cols_to_lower_case=[]
        import re

       
        #ds=ds.fillna(0)
        for c in columns:
            
            ds[c]=ds[c].replace(dic_to_replace,regex=True)
            if isinstance(ds[c].head(1)[0], str):
                ds[c]=ds[c].str.lower()


        return ds
            
