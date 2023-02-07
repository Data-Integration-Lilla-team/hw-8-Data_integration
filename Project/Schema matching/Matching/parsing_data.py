'''
Momentanea
classe responsabile per il parsing dei dati

metodo principale->parse_source

riorganizzazione nomi delle colonne
riorganizzazinoe valori delle colonne
'''
import os
import pandas as pd
def format_amount_emp(element):
    divisore=1000
    format_int=int(element)/divisore
    return format_int
#formattazione amount dollari
def fomrat_amount(element):
            prefix_03_gram='doll_'
            trillion='t'
            billion='b'
            million='m'
            trillino_limit=10**12
            billio_limit=10**9
            million_limit=10**6
            int_elem=int(element)
            #check trillion
            if int_elem>=trillino_limit:
                
                int_elem=int_elem/trillino_limit
                string_elem=prefix_03_gram+str(int_elem)+' '+trillion
                
            elif int_elem<trillino_limit and int_elem>=billio_limit:
                int_elem=int_elem/billio_limit
                string_elem=prefix_03_gram+str(int_elem)+' '+billion
                
            
            else:
                int_elem=int_elem/million_limit
                string_elem=prefix_03_gram+str(int_elem)+' '+million
                
            return string_elem
class Parser_data:


    def __init__(self):
        pass

    
    

    def parse_market_cap_USD_03_gram(self):
        market_cap_03_gram='Project\\Dataset\\ClusterParsed\\disfold\\03-gren.csv'
        column_name_03_gram='market_capitalization_usd'
        
        
        ds=pd.read_csv(market_cap_03_gram)
        #ds[column_name_03_gram]=ds[column_name_03_gram].apply(fomrat_amount)
        ds=self.drop_not_needed_cols(ds)
        ds.to_csv(market_cap_03_gram)

    #standardizzaizione del campo employees
    def parse_employees_number_03_gram(self):
        to_parse='Project\\Dataset\\ClusterParsed\\valuetoday\\03-gren.csv'
        col_employees='employees_number'
        col_market_cap='market_capitalization_2022'
        
        ds=pd.read_csv(to_parse)
        ds=self.drop_not_needed_cols(ds)

        #employees
        ds[col_employees]=ds[col_employees].fillna(0)
        ds[col_employees]=ds[col_employees].apply(format_amount_emp)

        #market cap
        ds[col_market_cap]=ds[col_market_cap].fillna(0)
        ds[col_market_cap]=ds[col_market_cap].apply(fomrat_amount)
        print(ds[col_market_cap].head(10))
        ds.to_csv(to_parse)
        
        
            

    def parse_specific_values(self):
        #self.parse_market_cap_USD_03_gram()
        self.parse_employees_number_03_gram()

       
        

        




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
                        '\r\n': '',
                        'billion':'b',
                        'trillion':'t',
                        'million':'m'
        } 
        columns=data.columns
        cols_to_lower_case=[]
        import re

       
        #ds=ds.fillna(0)
        for c in columns:
            
            data[c]=data[c].replace(dic_to_replace,regex=True)
            #verifico se è una lista
            print(c)
            print(data[c].head(2))
            trovato=''   
            if isinstance(data[c].head(1)[0], str):
                
                if '[' in data[c].head(1)[0]:
                    print(c,'============TROVATO====================')
                    print('before',data[c].head(1)[0])
                    trovato=c
                    data[c]=data[c].str.lower()
                    print(data[c].head(1)[0])
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
            
