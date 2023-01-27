import pandas as pd
import os
import numpy as np
from parser_custom import Parser_custom
from Levenshtein import distance
from merging_elements_market_cap import Merger


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
            
            word1=nlp(List1[i])
            word2=nlp(List2[j])
            
            correlazione[List1[i]].append(word1.similarity(word2))

    
    matrice_correlazione=pd.DataFrame(data=correlazione,columns=list_of_tokens,index=list_of_tokens)

    return matrice_correlazione

def compute_similarityLEVI(inverted_index,thersh):

    sim4column=dict()
    list_of_tokens=sorted(inverted_index.keys())
    

    List1 = list_of_tokens
    List2 = list_of_tokens

    #Matrix = np.zeros((len(List1),len(List2)),dtype=np.int_)
    correlazione=dict()

    for i in range(0,len(List1)):
        correlazione[List1[i]]=[]
        if List1[i] not in sim4column:
            sim4column[List1[i]]=[]
        for j in range(0,len(List2)):

            
            compute_dist=distance(List1[i],List2[j])
            if compute_dist!=0:
                compute_dist=1/compute_dist
            if compute_dist>thersh or compute_dist==0:
                tupla=(List2[j],compute_dist)
                sim4column[List1[i]].append(tupla)
            correlazione[List1[i]].append(compute_dist)

    

    matrice_correlazione=pd.DataFrame(data=correlazione,columns=list_of_tokens,index=list_of_tokens)

    return [matrice_correlazione,sim4column]

import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk



from nltk.corpus import stopwords
def clean_data(text):
 
  text = text.lower()
  text = ' '.join([ele for ele in text.split() if ele not in stopwords])
  return text
def compute_similarityCOS(inverted_index):

    
    
    
    
    list_of_tokens=sorted(inverted_index.keys())
    

    
    
    

    vectorize=CountVectorizer().fit_transform(list_of_tokens)
    
    vectors = vectorize.toarray()
    print(vectors)

    cos_sim = cosine_similarity(vectors)

    print(cos_sim)

    

    #Matrix = np.zeros((len(List1),len(List2)),dtype=np.int_)
    

    
    matrice_correlazione=pd.DataFrame(data=cos_sim,columns=list_of_tokens,index=list_of_tokens)
    

    return matrice_correlazione


import ngram
def compute_sim_ngrams(inverted_index,thresh=0.0):
    N=3
    list_of_tokens=sorted(inverted_index.keys())
    
    sim4column=dict()
    List1 = list_of_tokens
    List2 = list_of_tokens

    #Matrix = np.zeros((len(List1),len(List2)),dtype=np.int_)
    correlazione=dict()

    for i in range(0,len(List1)):
        correlazione[List1[i]]=[]
        if List1[i] not in sim4column:
            sim4column[List1[i]]=[]
        for j in range(0,len(List2)):
            element1=List1[i]
            element2=List2[j]
            
           
            compute_dist=ngram.NGram.compare(element1,element2,N=3)
            
            
            correlazione[List1[i]].append(compute_dist)
            if compute_dist>=thresh:
                tupla=(List2[j],compute_dist)
                sim4column[List1[i]].append(tupla)

    
    matrice_correlazione=pd.DataFrame(data=correlazione,columns=list_of_tokens,index=list_of_tokens)
    
    return [matrice_correlazione,sim4column]


import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
def plot_correlation(df, base_path,name,threshold=0): # Define cmap for heatmap
    
    mask1 = np.triu(np.ones_like(df, dtype=bool))# Generate mask under threshold
    if threshold > 0:
         mask2 = df < threshold
    else:
        mask2 = df < 0 # Plot heatmap and save fig
    fig, ax = plt.subplots(figsize=(20, 20))
    title = "Titolo heatmap"
    file_name = base_path + "\\" + "".join(title.lower()).replace(" ", "_")
    ax.set_title(title)
    # ax.set_xlabel("Token")
    # ax.set_ylabel("Token")
    heatmap = sns.heatmap(df, ax=ax, mask=(mask1), fmt=".0f",linewidths=2, cmap="Purples", square=True, )
    plt.show()
    fig.savefig(os.path.join(base_path,name), bbox_inches='tight', transparent=True)


def compute_sim4column(sim4column):
    for k in sim4column.keys():
        listOf_corr=list(sim4column[k])
        listOf_corr.sort(key=lambda a: a[1])
        print (k)
        for e in listOf_corr:
            print(e)


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
            string=string+"'"+k+"':" + str(col4file[k])+'\n'

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

    merger=Merger()
    merger.merge_data(file_names,inverted_index)
    

    



    '''
    matrice_correlazioneNgrams='matrice_ngrams'
    matrice_levi='matrice_levi'
    threshold=0.9   #valore minimo per definire due di chiavi uguali

    #Levi
    col2sim='similarità_tra_colonne_Levi.txt'
    stringa=''
    min=0.2
    max=0.6
    step=0.1
    i=min
    while(i<=max):
        stringa=stringa+'threshold:'+str(i)+'\n'
        print('threshold=',i)
        res=compute_similarityLEVI(inverted_index,i)
        matrice_correlazione=res[0]
        sim4column=res[1]
        for k in sim4column.keys():
            stringa=stringa+k+'->'
            for e in sim4column[k]:
                stringa=stringa+str(e)
            
            stringa=stringa+'\n'
        stringa=stringa+'\n'
        i+=step
    
    write_infos_on_file(col2sim,base_path,stringa)
    compute_sim4column(sim4column)

    


    
    
    plot_correlation(matrice_correlazione,base_path,matrice_levi,12)


    



    #Ngrams
    col2sim='similarità_tra_colonne_ngrams.txt'
    stringa=''
    min=0.2
    max=0.6
    step=0.1
    i=min
    while(i<=max):
        stringa=stringa+'threshold:'+str(i)+'\n'
        print('threshold=',i)
        res=compute_sim_ngrams(inverted_index,i)
        matrice_correlazione=res[0]
        sim4column=res[1]
        for k in sim4column.keys():
            stringa=stringa+k+'->'
            for e in sim4column[k]:
                stringa=stringa+str(e)
            
            stringa=stringa+'\n'
        stringa=stringa+'\n'
        i+=step
    
    write_infos_on_file(col2sim,base_path,stringa)

    

    
    matrice_correlazione.to_csv(os.path.join(base_path,matrice_correlazioneNgrams))

   
    
    plot_correlation(matrice_correlazione,base_path, matrice_correlazioneNgrams,0.4)

    '''
    
    
    
    

    




    