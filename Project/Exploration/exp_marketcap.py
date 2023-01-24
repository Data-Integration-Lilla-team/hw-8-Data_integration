import pandas as pd
import os
import numpy as np
from parser_custom import Parser_custom
from Levenshtein import distance


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

def write_infos_on_file(file,basePath,string):
    fileTGT=os.path.join(basePath,file)
    with open(fileTGT, 'w') as f:
    
            f.write(string)

        

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


#codice base

import seaborn as sns
import matplotlib.pyplot as plt

import spacy


def create_matrix_spacy(inverted_index):
    list_of_tokens=sorted(inverted_index.keys())
    

    List1 = list_of_tokens
    List2 = list_of_tokens

    nlp=spacy.load("en_core_web_sm")
    
    #Matrix = np.zeros((len(List1),len(List2)),dtype=np.int_)
    correlazione=dict()

    for i in range(0,len(List1)):
        correlazione[List1[i]]=[]
        for j in range(0,len(List2)):
            compute_dist=distance(List1[i],List2[j])
            print('eval',List1[i],List2[j],'->',compute_dist)
            word1=nlp(List1[i])
            word2=nlp(List2[j])
            
            correlazione[List1[i]].append(word1.similarity(word2))

    
    matrice_correlazione=pd.DataFrame(data=correlazione,columns=list_of_tokens,index=list_of_tokens)

    return matrice_correlazione

def create_inverted_index_on_similarity(inverted_index):
    list_of_tokens=sorted(inverted_index.keys())
    

    List1 = list_of_tokens
    List2 = list_of_tokens

    #Matrix = np.zeros((len(List1),len(List2)),dtype=np.int_)
    correlazione=dict()

    for i in range(0,len(List1)):
        correlazione[List1[i]]=[]
        for j in range(0,len(List2)):
            compute_dist=distance(List1[i],List2[j])
            print('eval',List1[i],List2[j],'->',compute_dist)
            
            correlazione[List1[i]].append(distance(List1[i],List2[j]))

    
    matrice_correlazione=pd.DataFrame(data=correlazione,columns=list_of_tokens,index=list_of_tokens)

    return matrice_correlazione

import matplotlib.pyplot as plt
def plot_correlation(matrix, base_path):
    sns.set_theme(style="white")

    

    

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(matrix, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    plot=sns.heatmap(matrix, mask=mask, cmap=cmap, vmax=20, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    plt.show()
    path=base_path+'\\Correlazione.png'
    #plt.savefig(path)



if __name__=='__main__':  
    #andiamo ad effettuare della anlisi relative a campi in overlap
    base_path='Project\\Dataset\\Clusters\\companiesmarketcap'

    file_all_columns4ds='colonnePerdataset.txt'

    file_inverted_index='indice_invertito.txt'

    file_names=get_file_names(base_path)
    #compute columns: per ogni file definiamo le colonne
    col4file=get_col_4_files(file_names)
    string=''
    #preparazioen stringa da scrivere
    for k in col4file.keys():
            string=string+'TEAM:'+k+'-> COLS: '+ str(col4file[k])+'\n'

    write_infos_on_file(file_all_columns4ds,base_path,string)
    

    #creazione di un indice invertito dove andiamo ad inserire nome_colonna->doc
    print('inverted index')
    inverted_index=create_inverted_index(col4file)

    #crittura su file
    string=''
    for k in sorted(inverted_index):
            string=string+ k+'->'+str(inverted_index[k])+'\n'
    
    write_infos_on_file(file_inverted_index,base_path,string)


    #creazione di un indice invertito basato sulla similarità di chiavi

    threshold=0.9   #valore minimo per definire due di chiavi uguali

    matrice_correlazione=create_inverted_index_on_similarity(inverted_index)
    

    plot_correlation(matrice_correlazione,base_path)

    matrice_correlazione_scpy=create_matrix_spacy(inverted_index)

    plot_correlation(matrice_correlazione,base_path)
    #inverted_index_based_on_sim=create_inverted_index_on_similarity(inverted_index)

    

    




    