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
        self.threshold_tokens=0.25
        self.threshold=0.4
        self.threshold_levi=0.6
        self.max=0.6
        self.step=0.1
        self.dim_n_grams=4

        #base path
        self.cluster=clusterName
        self.path_destinazione='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari'

        #team2cols
        self.name_file_cols4team='colonne_per_team.txt'
        self.path_name_file_cols4team=self.path_destinazione+'\\'+self.name_file_cols4team

        
        self.path_name_file_inverted_index='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\inverted_index.txt'

        
        




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


       

    #eliminazione delle conolle Unnamed
    def drop_not_needed_cols(self,data):
        
        
        
        data=data.loc[:,~data.columns.str.startswith('Unnamed')]
        
        return data

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
    def create_inverted_index(self):
        with open(self.path_name_file_inverted_index, 'r') as file:
            data=file.read()
        inverted_index=json.loads(data)
        return inverted_index
        
    #crea un dizionario key, val
    #key->nome del team
    #val->lista di colonne
    def get_col_4_files(self,files):

        col_4_team=dict()
        for team in files.keys():

            cluster_name=team
            path_ds=files[team]
            
            data=pd.read_csv(path_ds)
            print('#=========================')
            print('Cluster:',cluster_name)
            
            data=self.drop_not_needed_cols(data)   
            

            
            columns=data.columns
            colonne_parsed=[]
            for c in columns:
                colonne_parsed.append(c)
            
            print(colonne_parsed)
            
        
            
            col_4_team[cluster_name]=colonne_parsed

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
    
    def save_infos_ngrams(self,stringa,corr_matrix):
        corr_matrix.to_csv(self.path_name_file_correlazioni_ngrams)
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
        print('Lista1',sorted(List1))
        print('Lista2',sorted(List2))

        #Matrix = np.zeros((len(List1),len(List2)),dtype=np.int_)
        correlazione=dict()

        for i in range(0,len(List1)):
            correlazione[List1[i]]=[]
            if List1[i] not in sim4column:
                sim4column[List1[i]]=[]
            for j in range(0,len(List2)):
                element1=List1[i]
                element2=List2[j]
                                
                words_in_element1=set(element1.split('_'))
                words_in_element2=set(element2.split('_'))
                inters=words_in_element1.intersection(words_in_element2)
                insert=0
                if len(words_in_element1)==1 and  len(inters)==1:
                       
                        insert=1
                       
                else:
                    if len(inters)>=0.8*len(words_in_element1):
                        
                        insert=1
                
                compute_dist=distance(List1[i],List2[j])
                if compute_dist!=0:
                    compute_dist=1/compute_dist
                if compute_dist>=self.threshold_levi or compute_dist==0 or insert==1:
                    tupla=(List2[j],compute_dist)
                    
                    sim4column[List1[i]].append(tupla)
                correlazione[List1[i]].append(compute_dist)
            print(List1[i],sim4column[List1[i]])

        

        matrice_correlazione=pd.DataFrame(data=correlazione,columns=list_of_tokens,index=list_of_tokens)

        return [matrice_correlazione,sim4column]


    #metodo per la creazione della matrice di similarità mediante LEVINSTEIN
    #si impongono più threshold
    def compute_LEVI_sim(self, inverted_index, test):
        i=self.threshold
        stringa=''
        jaccard_dist_eval=dict()
        eval=Eval()
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
            
            
        
     
       

        self.save_infos_levi(stringa,matrice_correlazioneLevi)
        return sim4column_no_score

#=======================================================================
#====================NGRAMS=============================================
#=====================================================================
    def save_infos_ngrams(self, string, matrice):
        matrice.to_csv(self.path_name_file_matrice_correlazione_Ngrams)
        with open(self.path_name_file_correlazioni_ngrams, 'w') as f:
    
            f.write(string)


    #calcolo della matrice di correlazione e della lista di correlazioni in modalità threshold   
    def compute_sim_ngrams(self,inverted_index,thresh=0.0):
        
        
        list_of_tokens=sorted(inverted_index.keys())
        jaccard_dist_eval=dict()
        eval=Eval()
        sim4column=dict()
        List1 = list_of_tokens
        List2 = list_of_tokens
        print(List1.index('revenue_2020_eu'),'\n',List2.index('revenue_2020_eu'))

        #Matrix = np.zeros((len(List1),len(List2)),dtype=np.int_)
        correlazione=dict()

        for i in range(0,len(List1)):
            correlazione[List1[i]]=[]
            if List1[i] not in sim4column:
                sim4column[List1[i]]=[]
            for j in range(0,len(List2)):
                element1=List1[i]
                element2=List2[j]
                
                words_in_element1=set(element1.split('_'))
                words_in_element2=set(element2.split('_'))
                inters=words_in_element1.intersection(words_in_element2)
                insert=0
                if len(words_in_element1)==1:
                    if len(inters)==1:
                        insert=1
                       
                else:
                    if len(inters)>=0.8*len(words_in_element1):
                        insert=1

            
                compute_dist=ngram.NGram.compare(element1,element2,N=self.dim_n_grams)
                
                
                
                correlazione[List1[i]].append(compute_dist)
                if compute_dist>=thresh or insert==1:
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
            
            
       


        self.save_infos_ngrams(stringa,matrice_correlazioneNgrams)
        return sim4column_no_score
        
    #files->dizionario k: nome file, value, path   
    def computeCorr(self, files, validation_set):

        #calcolo delle colonne per dataset
        col4file=self.get_col_4_files(files)               #lista di colonne per ogni dataset in un sorgente
       
        inverted_index=self.create_inverted_index()
        print('Indice invertito keys',inverted_index.keys())
        
        resultLevi=self.compute_LEVI_sim(inverted_index,validation_set)
        
        resultNgrams=self.compute_Ngrams_sim(inverted_index,validation_set)

        resultLevi.update(resultNgrams)

        valutation=Eval()
        print('Score mod 1')
        results=valutation.compute_dis_f1(resultLevi,validation_set)
        for i in results:
            print(i)

        

        
        return resultLevi
    
    def computeCorrTokens(self, tokens, validation_set):

        
        diz_sinonimi_final=dict()
        i=0
        #crea i potenziali nuovi sinonimi
        for i in range(len(tokens)):
            current_element=tokens[i]
            j=0
            for j in range (len(tokens)):
                if j!=i:
                    to_confront=tokens[j]
                    
                    score=current_element.confront_columns(to_confront)
                    if score>=self.threshold_tokens:
                        
                        
                        current_element.update_sin_attuali(to_confront.name)
        #crea i sinonimi
        for t in tokens:
            true_name=t.name
            if true_name in validation_set:
                if true_name not in diz_sinonimi_final:
                    diz_sinonimi_final[true_name]=t.sin_attuali
                if true_name in diz_sinonimi_final:
                    diz_sinonimi_final[true_name].update(t.sin_attuali)
        

        
        return diz_sinonimi_final
        
        

        


        


        
       
        
        
        
