'''
Classe specializzata nel calcolo della similarità tra nomi delle colonne
Utilizza n-grams dist per computare la similitudine

'''
import pandas as pd
from Levenshtein import distance
import ngram
import os
from evaluator import Eval
import numpy as np
import json
class NameCorr:

    def __init__(self,clusterName) -> None:

        #thresholds
        self.threshold=0.6
        self.max=0.6
        self.step=0.1

        #base path
        self.cluster=clusterName
        self.path_destinazione='Project\\Schema matching\\DatasetSchemaMatch\\'+clusterName

        #team2cols
        self.name_file_cols4team='colonne_per_team.txt'
        self.path_name_file_cols4team=self.path_destinazione+'\\'+self.name_file_cols4team

        #invertedIndex
        self.name_file_inverted_index='inverted_index_col_names.txt'
        self.path_name_file_inverted_index=self.path_destinazione+'\\'+self.name_file_inverted_index

        #invertedIndex_dic
        self.name_file_inverted_index_dic='inverted_index_col_names_dic.txt'
        self.path_name_file_inverted_index_dic=self.path_destinazione+'\\'+self.name_file_inverted_index_dic

        




        #matriceCorrelazione: NGRAMS
        self.name_file_matrice_correlazione_Ngrams='matrice_ngrams.csv'
        self.path_name_file_matrice_correlazione_Ngrams=self.path_destinazione+'\\'+self.name_file_matrice_correlazione_Ngrams

        
        #matriceCorrelazione: LEVI
        self.name_file_matrice_correlazione_levi='matrice_levi.csv'
        self.path_name_file_matrice_correlazione_levi=self.path_destinazione+'\\'+self.name_file_matrice_correlazione_levi

        #correlazioni: Levi
        self.name_file_correlazione_levi='correlazioni_levi.txt'
        self.path_name_file_correlazioni_levi=self.path_destinazione+'\\'+self.name_file_correlazione_levi

         #correlazioni: Ngrams
        self.name_file_correlazione_ngrams='correlazioni_ngrams.txt'
        self.path_name_file_correlazioni_ngrams=self.path_destinazione+'\\'+self.name_file_correlazione_ngrams


       


    #stampa su un file di un dizionario
    def print_on_txt_file(self, col4file):
        stringa=''
        for k in col4file.keys():
            stringa=stringa+"'"+k+"':"+ str(col4file[k])+'\n'
        
        
        with open(self.path_name_file_cols4team, 'w') as f:
    
            f.write(stringa)


    def print_on_file_inverted_index(self,inverted_index):
        stringa=''
        for k in sorted(inverted_index.keys()):
            stringa=stringa+"'"+k+"':"+ str(inverted_index[k])+'\n'
        
        
        with open(self.path_name_file_inverted_index, 'w') as f:
    
            f.write(stringa)
        
        with open(self.path_name_file_inverted_index_dic, 'w') as f:
            f.write(json.dumps(inverted_index))
        
        



    #creazione dell'indice invertito
    # input-> diz team:[cols]
    # output->diz col:[teams]  
    def create_inverted_index(self,cols4file):
        inverted_index=dict()
        for k in cols4file.keys():
            elements=cols4file[k]
            for e in elements:
                if e in inverted_index:
                    inverted_index[e].append(k)
                else:
                    inverted_index[e]=[k]
        
        self.print_on_file_inverted_index(inverted_index)
        return inverted_index
    #crea un dizionario key, val
    #key->nome del team
    #val->lista di colonne
    def get_col_4_files(self,files):

        col_4_team=dict()
        for team, path in files.items():

            team_name=team
            path_ds=files[team]
            
            data=pd.read_csv(path_ds)

            
            columns=data.columns
            filtered_columns=[]
            for c in columns:
                if 'Unnamed' not in c:
                    filtered_columns.append(c)
        
            
            col_4_team[team_name]=filtered_columns

        self.print_on_txt_file(col_4_team)
        return col_4_team


#PLOT DELLE MATRICI DI CORRELAZIONE
    def plot_correlation(self,df,name,threshold=0): # Define cmap for heatmap
        import seaborn as sns
        import matplotlib.colors
        import matplotlib.pyplot as plt
        mask1 = np.triu(np.ones_like(df, dtype=bool))# Generate mask under threshold
        if threshold > 0:
            mask2 = df < threshold
        else:
            mask2 = df < 0 # Plot heatmap and save fig
        fig, ax = plt.subplots(figsize=(20, 20))
        title = "Titolo heatmap"
        file_name = self.path_destinazione + "\\" + "".join(title.lower()).replace(" ", "_")
        ax.set_title(title)
        # ax.set_xlabel("Token")
        # ax.set_ylabel("Token")
        heatmap = sns.heatmap(df, ax=ax, mask=(mask1), fmt=".0f",linewidths=2, cmap="Purples", square=True, )
        
        fig.savefig(os.path.join(self.path_destinazione,name), bbox_inches='tight', transparent=True)

    #computa un dizionario nome_colonna->lista sinonimi senza il punteggio di similitudine
    def compute_sim4column_no_score(self, sim4col):
        out=dict()
        for k in sim4col.keys():
            lista=[]
            for i in sim4col [k]:
                lista.append(i[0])
            
            out[k]=lista
        return out
    
    def evalBestThreshold(self, scores):
        best=0
        thresh=0
        for k in scores.keys():
            score=scores[k]
            if score>best:
                best=score
                thresh=k
            
        return (best,thresh)

        

#=======================================================================
#====================LEVI=============================================
#=====================================================================
    #salvataggio info distanza di levi
    def save_infos_levi(self,stringa,corr_matrix):
        corr_matrix.to_csv(self.path_name_file_matrice_correlazione_levi)
        with open(self.path_name_file_correlazioni_levi, 'w') as f:
    
            f.write(stringa)

    #Calcolo della similarità Levi tra colonne
    #input: indice invertito, threshold
    #output: matrice di correlazione, dizionario in cui sono indicati le somiglanze tra colonne
    def compute_similarityLEVI(self,inverted_index,thersh):

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


    #metodo per la creazione della matrice di similarità mediante LEVINSTEIN
    #si impongono più threshold
    def compute_LEVI_sim(self, inverted_index, test):
        i=self.threshold
        stringa=''
        jaccard_dist_eval=dict()
        eval=Eval()
        while(i<=self.threshold):
            
            stringa=stringa+'threshold:'+str(i)+'\n'
            
            res=self.compute_similarityLEVI(inverted_index,i)
            matrice_correlazioneLevi=res[0]
            sim4column=res[1]
            sim4column_no_score=self.compute_sim4column_no_score(sim4column)
            score=eval.evaluate(sim4column_no_score,test)
            jaccard_dist_eval[i]=score
            stringa=stringa+' avg jaccard:'+str(score)+'\n'
            
            

            for k in sim4column.keys():
                stringa=stringa+k+'->'
                for e in sim4column[k]:
                    stringa=stringa+str(e)
                
                stringa=stringa+'\n'
            stringa=stringa+'\n'
            i+=self.step
        best_thershold=self.evalBestThreshold(jaccard_dist_eval)
        
     
        best_result_all=self.compute_sim_ngrams(inverted_index,best_thershold[1])
        matrice_correlazioneLevi=best_result_all[0]
        best_result=best_result_all[1]
        out=self.compute_sim4column_no_score(best_result)

        self.save_infos_levi(stringa,matrice_correlazioneLevi)
        return out

#=======================================================================
#====================NGRAMS=============================================
#=====================================================================
    def save_infos_ngrams(self, string, matrice):
        matrice.to_csv(self.path_name_file_matrice_correlazione_Ngrams)
        with open(self.path_name_file_correlazioni_ngrams, 'w') as f:
    
            f.write(string)


    #calcolo della matrice di correlazione e della lista di correlazioni in modalità threshold   
    def compute_sim_ngrams(self,inverted_index,thresh=0.0):
        
        N=3
        list_of_tokens=sorted(inverted_index.keys())
        jaccard_dist_eval=dict()
        eval=Eval()
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

    #correlazione via Ngrams
    def compute_Ngrams_sim(self, inverted_index,test):
        stringa=''
        eval=Eval()
        jaccard_dist_eval=dict()
        i=self.threshold
        while(i<=self.threshold):
            stringa=stringa+'threshold:'+str(i)
            
            res=self.compute_sim_ngrams(inverted_index,i)
            matrice_correlazioneNgrams=res[0]
            sim4column=res[1]
            sim4column_no_score=self.compute_sim4column_no_score(sim4column)
            score=eval.evaluate(sim4column_no_score,test)
            jaccard_dist_eval[i]=score
            stringa=stringa+' avg jaccard:'+str(score)+'\n'
            for k in sim4column.keys():
                stringa=stringa+k+'->'
                for e in sim4column[k]:
                    stringa=stringa+str(e)
                
                stringa=stringa+'\n'
            stringa=stringa+'\n'
            i+=self.step
        best_thershold=self.evalBestThreshold(jaccard_dist_eval)
        best_result_all=self.compute_sim_ngrams(inverted_index,best_thershold[1])
        matrice_correlazioneNgrams=best_result_all[0]
        best_result=best_result_all[1]
        out=self.compute_sim4column_no_score(best_result)


        self.save_infos_levi(stringa,matrice_correlazioneNgrams)
        return out
        
        
    def computeCorr(self, files, validation_set):
        #calcolo delle colonne per dataset
        col4file=self.get_col_4_files(files)               #lista di colonne per ogni dataset in un sorgente
       
        inverted_index=self.create_inverted_index(col4file)
        
        resultLevi=self.compute_LEVI_sim(inverted_index,validation_set)

        resultNgrams=self.compute_Ngrams_sim(inverted_index,validation_set)

        resultLevi.update(resultNgrams)

        

        
        return resultLevi
        
       
        
        
        
