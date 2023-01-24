import pandas as pd
import os
from parser_custom import Parser_custom


#crea un dizionario composto da:
#1. nome team
#2. path del csv
def get_file_names(base_path):
    file_names=dict()                  
    for f in os.listdir(base_path):
        file=os.path.join(base_path,f)
        if os.path.isfile(file):
            if '.txt' not in file:
                file_names[f]=file

    return file_names

#filtriamo colonne 'Unnamed' ovvero colonne che sono inserite direttamente da Pandas
def format_columns(columns):
    cols=list(columns)
    out=[]
    to_filter_col='Unnamed:'
    for c in cols:
        if to_filter_col not in c:
            c=c.lower()             #tutto in lower case
            c=c.replace('(','_')
            c=c.replace(')','')
            c=c.replace(' ','_')
           
            out.append(c)
    
    return out


def get_col_4_files(files):

    col_4_team=dict()
    for team, path in files.items():

        team_name=team
        path_ds=files[team]
        print(path_ds)
        data=pd.read_csv(path_ds)

        parser=Parser_custom(path_ds)
        columns=data.columns
        
        columns=parser.parse(columns)    #eliminaimo gli unamed columns

        col_4_team[team_name]=columns


    return col_4_team

def write_infos_on_file(file,basePath,col4file):
    fileTGT=os.path.join(base_path,file)
    with open(fileTGT, 'w') as f:
        for k in col4file.keys():
            string='TEAM:'+k+'-> COLS: '+ str(col4file[k])+'\n'
            f.write(string)

        



if __name__=='__main__':  
    #andiamo ad effettuare della anlisi relative a campi in overlap
    base_path='Project\\Dataset\\Clusters\\companiesmarketcap'

    file_all_columns4ds='colonnePerdataset.txt'

    file_names=get_file_names(base_path)

    #compute columns: per ogni file definiamo le colonne
    col4file=get_col_4_files(file_names)

    write_infos_on_file(file_all_columns4ds,base_path,col4file)
    for k in col4file.keys():
        print('TEAM:',k,'-> COLS: ',col4file[k])

    




    