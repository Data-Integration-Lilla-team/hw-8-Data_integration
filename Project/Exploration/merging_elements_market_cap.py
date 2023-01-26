
import pandas as pd
import os
from parser_custom import Parser_custom
class Merger:

    def __init__(self):

        self.dizionarioSinonimi=dict()

        self.dizionarioSinonimi={ 
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

        self.team2ds=dict()

    #parsing delle colonne ed eliminazione di quelle inutili
    def get_ds_4_team(self,files):

        col_4_team=dict()
        for team, path in files.items():
            
            print(team)
            team_name=team
            path_ds=files[team]
            
            data=pd.read_csv(path_ds)

            parser=Parser_custom(path_ds)
            columns=data.columns

            print(columns)
            columns=parser.parse_column_for_merge(columns)    #restituisce un dizionario avente vecchio nome colonna e nuovo
            

            data.rename(columns=columns,inplace=True)
            data=data.drop(['Unnamed: 0.1','Unnamed: 0'],axis=1,errors='ignore')
            print(data.columns)
            col_4_team[team_name]=data


        return col_4_team

    def merge_data(self,file_name,inverted_index):

        team2ds=self.get_ds_4_team(file_name)



        #per ogni elemento del dizionario dei sinonimi (i valori nella lista)
        #accedo all'indice invertito e acquisisco il team dove cercare
        #accedo al dizionario dei ds tramite il team
        #prelevo la colonna

        aggregatore_colonne_simili=dict()

        for k in self.dizionarioSinonimi.keys():
            aggregatore_colonne_simili[k]=[]
            elementi=self.dizionarioSinonimi[k]     #lista di valori sinonimi alla key
            print('ELEMENTI',elementi)
            #per ogni colonna accedo all'indice invertito
            teams=[]
            for e in elementi:
                print('Elemento',e)
                teams=inverted_index[e]         #acquisisco il team
                for t in teams:
                    print('team',t)
                    data_series=team2ds[t][e]   #prende la colonna interessata per il dataset creato dal team
                    
                    column_team=[t]*len(data_series)    #crea una colonna con il nome del team

                    frame={k:data_series,'team':column_team}
                    data=pd.DataFrame(frame)
                    print(data)
                    aggregatore_colonne_simili[k].append(data)


        
        
        #union e creazione di un unico dataframe aventi tutti i valori presenti nelle colonne
        schema_mediato=dict()

        for k in aggregatore_colonne_simili.keys(): #nome colonna schema mediato
            elementi=aggregatore_colonne_simili[k]
            
            unione=pd.DataFrame(data=elementi[0],columns=[k,'team'])
            for i in range(1,len(elementi)):
                unione=pd.concat([unione,elementi[i]])
                

            
            schema_mediato[k]=unione

        
        base_path='Project\\Dataset\\Clusters\\companiesmarketcap\\'
        extension='.csv'
        for k in schema_mediato.keys():
            path=base_path+k+extension
            schema_mediato[k].to_csv(path)
    
    def from_ds_to_schema_mediato(path, dizionarioSinonimi):
    
        df_append = pd.DataFrame() #concatenazione di tutti i dataset
        lista_df = []  #lista per concatenare
        
        #scorro tutti i dataset
        for file in os.listdir(path):
            df_temp = pd.read_csv(path + '\\' + file)
            #scorro i termini del dizionario
            for k in dizionarioSinonimi:
                #scorro le colonne del dataset
                for column_headers in list(df_temp.columns):
                    #se il termine è nel dizionario
                    if column_headers in dizionarioSinonimi[k]:
                        #sostituisco il nome con quello desiderato (la chiave)
                        df_temp.rename(columns={column_headers:k}, inplace = True)
            #inserisco il df in una lista
            lista_df.append(df_temp)
        #concateno i dataset
        df_append = pd.concat(lista_df, ignore_index = True)
    
        #elimino le colonne non volute nello schema mediato
        for column in df_append.columns:
            if column not in dizionarioSinonimi.keys():
                df_append = df_append.drop(column, axis = 1)
                
        #salvo il dizionario
        df_append.to_csv(path + '\\schema_mediato.csv' )
            

            

                

            






