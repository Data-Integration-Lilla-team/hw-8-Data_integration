
import pandas as pd
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
            elementi=self.dizionarioSinonimi[k]
            print('ELEMENTI',elementi)
            #per ogni colonna accedo all'indice invertito
            teams=[]
            for e in elementi:
                print('Elemento',e)
                teams=inverted_index[e]
                for t in teams:
                    print('team',t)
                    data_series=team2ds[t][e]   #series
                    column_team=[t]*len(data_series)
                    
                    frame={e:data_series,'team':column_team}
                    data=pd.DataFrame(frame)
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

            

                

            






