#performace per singolo cluster
import os
import pandas as pd
import json
def compute_jaccard( A,B):
        intersection=len(list(A.intersection(B)))
        union=(len(list(A))+len(list(B)))-intersection
        return float(intersection)/union

def get_final_score(true,comp):
    with open(comp) as f:
        data=f.read()
    
    computato=json.loads(data)
    with open(true) as f:
        data=f.read()
    target=json.loads(data)

    N=len(target.keys())
    precision=0
    recall=0
    f1=0
    jaccard=0
    numero_confronti_extra=0
    for k in target.keys():
        sing_precision=0
        sing_recall=0
        sing_F1=0
        comp_sin=set(computato[k])
        true_sin=set(target[k])
        
        intersezione=comp_sin.intersection(true_sin)
        false_positive=comp_sin.difference(true_sin)
        false_negative=true_sin.difference(comp_sin)
        jaccard=jaccard+compute_jaccard(comp_sin,true_sin)
        sing_precision=len(intersezione)/(len(comp_sin)+len(false_positive))
        sing_recall=len(intersezione)/(len(intersezione)+len(false_negative))
        sing_F1=(2*sing_precision*sing_recall)/(sing_recall+sing_precision)
        numero_confronti_extra=numero_confronti_extra+len(comp_sin.difference(true_sin))


        precision=precision+sing_precision
        recall=recall+sing_recall
        f1=f1+sing_F1
    
    results=['final',precision/N,recall/N,f1/N,jaccard/N,numero_confronti_extra/N]
    print(results)
    return results

def create_computato(computato):
    final_dic_sin=dict()
    for k in computato.keys():
        elements=computato[k]
        final_dic_sin[k]=set()
        for e in elements:
            values=e.split('-')
            value=values[len(values)-1]
            final_dic_sin[k].add(value)
   
    return final_dic_sin

def get_scores(name,path,val=False):
    computato=path+'\\dic_pre_val.txt'
    target=path+'\\column_sinonimi.txt'
    with open(computato) as f:
        data=f.read()

    
    
    computato=json.loads(data)
    if val==True:
        coumputato=create_computato(computato)
    with open(target) as f:
        data=f.read()
    target=json.loads(data)

    N=len(target.keys())
    precision=0
    recall=0
    f1=0
    jaccard=0
    numero_confronti_extra=0
    for k in target.keys():
        sing_precision=0
        sing_recall=0
        sing_F1=0
        comp_sin=set(computato[k])
        true_sin=set(target[k])
        
        intersezione=comp_sin.intersection(true_sin)
        false_positive=comp_sin.difference(true_sin)
        false_negative=true_sin.difference(comp_sin)
        jaccard=jaccard+compute_jaccard(comp_sin,true_sin)
        sing_precision=len(intersezione)/(len(comp_sin)+len(false_positive))
        sing_recall=len(intersezione)/(len(intersezione)+len(false_negative))
        sing_F1=(2*sing_precision*sing_recall)/(sing_recall+sing_precision)
        numero_confronti_extra=numero_confronti_extra+len(comp_sin.difference(true_sin))


        precision=precision+sing_precision
        recall=recall+sing_recall
        f1=f1+sing_F1
    
    results=[name,precision/N,recall/N,f1/N,jaccard/N,numero_confronti_extra/N]
    return results
def get_scores_VAL(name,path_comp,path_true):
    name=name.replace('.txt','')
    target=path_true+'\\'+name+'\\dizionario.txt'
    
    with open(path_comp) as f:
        data=f.read()

    
    
    computato=json.loads(data)
    computato=create_computato(computato)
    
    with open(target) as f:
        data=f.read()
    target=json.loads(data)
    
   

    
    precision=0
    recall=0
    f1=0
    jaccard=0
    N=0
    
    numero_confronti_extra=0
    for k in computato.keys():
        if k in computato and k in target:
            N+=1
    
        
        sing_precision=0
        sing_recall=0
        sing_F1=0
        if k in target:
            
            
            comp_sin=set(computato[k])
            true_sin=set(target[k])
           
            
            
            intersezione=comp_sin.intersection(true_sin)
            false_positive=comp_sin.difference(true_sin)
            false_negative=true_sin.difference(comp_sin)
            jaccard=jaccard+compute_jaccard(comp_sin,true_sin)
            sing_precision=len(intersezione)/(len(comp_sin)+len(false_positive))
            sing_recall=len(intersezione)/(len(intersezione)+len(false_negative))
            sing_F1=(2*sing_precision*sing_recall)/(sing_recall+sing_precision)
            numero_confronti_extra=numero_confronti_extra+len(comp_sin.difference(true_sin))


            precision=precision+sing_precision
            recall=recall+sing_recall
            f1=f1+sing_F1
        
            
    
    results=[name,precision/N,recall/N,f1/N,jaccard/N,numero_confronti_extra/N]
    print(results)
    return results
    



    
def print_perf_preProcessing_module_4clusters():
    path_Clusters='Project\\Schema matching\\DatasetSchemaMatch'
    clusters=os.listdir(path_Clusters)
    colonne=['name','precision','recall','f1','jaccard','avg comp inutili']
    results=[]
    for f in clusters:
        name_cluster=f
        path=os.path.join(path_Clusters,f)
        results.append(get_scores(name_cluster,path))
    

    results=pd.DataFrame(data=results,columns=colonne)
    tgt_path='Project\\Testing\\Matching\\performace\\perf_per_clusters.csv'
    results.to_csv(tgt_path)
    
def print_perf_preProcessing_module_4schemaMediato():
    colonne=['name','precision','recall','f1','jaccard','avg comp inutili']
    schema_matching_true='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\validation_set\\column_sinonimi.txt'
    computato='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\dic_pre_val.txt'
    scores_final=get_final_score(schema_matching_true,computato)

    scores_final=pd.DataFrame(data=[scores_final],columns=colonne)

    scores_final.to_csv('Project\\Testing\\Matching\\performace\\perf_per_schema_mediato.csv')

def print_perf_Valentine_4clusters():
    path_Clusters_comp='Project\\Schema matching\\SchemaMatchingValentine\\clusters\\final_synonyms'
    path_Clusters_true='Project\\Schema matching\\DatasetSchemaMatch'
    clusters=os.listdir(path_Clusters_comp)
    colonne=['name','precision','recall','f1','jaccard','avg comp inutili']
    results=[]
    for f in clusters:
        name_cluster=f
        path_comp=os.path.join(path_Clusters_comp,f)
        
        print('======CLUSTER=======:',name_cluster)
        results.append(get_scores_VAL(name_cluster,path_comp,path_Clusters_true))
    
    results=pd.DataFrame(data=results,columns=colonne)
    tgt_path='Project\\Testing\\Matching\\performace\\Valentine_per_clusters.csv'
    results.to_csv(tgt_path)
    

if __name__=='__main__':

    #print_perf_preProcessing_module_4clusters()

    #print_perf_preProcessing_module_4schemaMediato()

    print_perf_Valentine_4clusters()
    

    



