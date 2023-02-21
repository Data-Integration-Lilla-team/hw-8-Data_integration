#performace per singolo cluster
import os
import pandas as pd
import json


def conta_confronti_in_lista(lista_sinonimi_k,indice):
    confronti=0
    
    for sin in lista_sinonimi_k:
        
        print('tokens',sin)
        if len(sin.split('-'))>1:
        
            sin=sin.split('-')[1]
        print('sin:',sin)
        if sin in indice:
            tot=len(indice[sin])
            print('occorrenze',tot)
            confronti+=len(indice[sin])
    
    return confronti


def calc_confronti(sinonimi,indice):
    confronti=0
    
    
    

    for k in sinonimi.keys():
            
                print('ELEMENTO:',k)
                print('------>CONFRONTI ATTUALI',confronti)
                confronti=confronti+conta_confronti_in_lista(set(sinonimi[k]),indice)
    
                print('------>CONFRONTI TOTALI',confronti)    
    return confronti



def conta_valori(true, computed, index):
    #calolca reali
    determinatore=len(computed)
    print('CONFRONTI INUTILI')
    colonne_computate=get_colonne(computed)
    
    colonne_true=get_colonne(true)
    colonne_index=get_colonne(index)

    print('COLONNE COMPUTATE:',colonne_computate)
    
    print('COLONNE TRUE:',colonne_true)
    print('COLONNE INDEX:',colonne_index)
    print('NUMERO DI COLONNE=',determinatore)
    print('---->CALCOLO CONFRONTI VERO')
    confronti_reali=calc_confronti(true,index)
    
    print('->CONFRONTI TRUE:',confronti_reali)
    print('---->CALCOLO CONFRONTI COM')
    confronti_computati=calc_confronti(computed,index)
    print('----->CONFRONTI COMPUTATI:',confronti_computati)
    
    confronti_extra=confronti_computati-confronti_reali
    print('-->CONFRONTI EXTRA:',confronti_extra)
    
    return [confronti_computati,confronti_computati/determinatore,confronti_reali/determinatore,int(confronti_extra)]

def conta_valori_2(true, computed,index):
    determinatore=len(computed)
    
    confronti_reali=calc_confronti(true,index)/determinatore
    for k in computed.keys():
        if k in true:
            confronti_computati=len(computed[k])
    confronti_extra=confronti_computati-confronti_reali
    if(confronti_extra)<=1:
        confronti_extra=1
    print('computati', confronti_computati)
    print('reali',confronti_reali)
    return [confronti_computati,confronti_computati/determinatore,confronti_reali,int(confronti_extra/2)]


    
def compute_jaccard( A,B):
        intersection=len(list(A.intersection(B)))
        union=(len(list(A))+len(list(B)))-intersection
        return float(intersection)/union

def clear_data(true):
    out=set()
    for e in true:
        if '-' in e:
            name=e.split('-')
            name=name[1]
        else:
            name=e
        out.add(name)
    return out

def unify_data(computato):
    out=dict()
    for k in computato.keys():
        if '-' in k:
            name=k.split('-')[0]
        else:
            name=k
        if name not in out:
            out[name]=set()
            out[name].update(computato[k])
        else:
            out[name].update(computato[k])
    return out
def get_colonne(dic):
    return list(dic.keys())      
def get_final_score(true,comp,index):


    #COMPUTATE
    with open(comp) as f:
        data=f.read()
    
    computato=json.loads(data)
    colonne_computate=get_colonne(computato)
    print('Colonne computate (Doppioni): ',colonne_computate)
    print('LUNGHEZZA:',len(colonne_computate))



    computato=unify_data(computato)
    colonne_computate=get_colonne(computato)
    print('Colonne computate (Unificate)',colonne_computate)
    
    print('LUNGHEZZA:',len(colonne_computate))
    #TARGET
    with open(true) as f:
        data=f.read()
    target=json.loads(data)
    colonne_target=get_colonne(target)
    print('Colonne target: ',colonne_target)
    print('LUNGHEZZA TRUE:',len(colonne_target))
    

    #INDEX
    with open(index) as f:
        data=f.read()
    index=json.loads(data)
    colonne_index=get_colonne(index)
    print('COLONNE INDICE:',colonne_index)



    N=len(colonne_computate)    #potrebbero essere minori

    precision=0
    recall=0
    f1=0
    jaccard=0
    
    for k in target.keys():
        print('-->ELEMENTO CORRENTE:',k)
        #da togliere (?)
        if k in computato:
            sing_precision=0
            sing_recall=0
            sing_F1=0
            comp_sin=set(computato[k])  #sinonimi
            print('->SINONINMI COMPUTATI (',k,')->',comp_sin)
            comp_sin=clear_data(comp_sin)
            print('->SINONINMI COMPUTATI (',k,')->',comp_sin)

            #TARGET   
            true_sin=set(target[k])
            
            
            print('->SINONINMI TARGET (',k,')->',comp_sin)
            
            intersezione=comp_sin.intersection(true_sin)

            print('-->INTERSEZIONE:',intersezione)
            false_positive=comp_sin.difference(true_sin)
            print('-->False-pos',false_positive)
            false_negative=true_sin.difference(comp_sin)
            print('-->False-nega',false_negative)
            print('--->Jaccad corrente:',jaccard)
            jaccard=jaccard+compute_jaccard(comp_sin,true_sin)
            
            print('-->Jaccard tot:',jaccard)
            sing_precision=len(intersezione)/(len(comp_sin)+len(false_positive))
            sing_recall=len(intersezione)/(len(intersezione)+len(false_negative))
            sing_F1=(2*sing_precision*sing_recall)/(sing_recall+sing_precision)
            scores=conta_valori(target,computato,index)




            precision=precision+sing_precision
            print('--->Precsion corrente:',sing_precision)
            print('-->Precision totale:',precision)
            recall=recall+sing_recall
            
            print('--->Precsion corrente:',sing_recall)
            print('-->Precision totale:',sing_recall)
            f1=f1+sing_F1
            
            print('--->Precsion corrente:',sing_F1)
            print('-->Precision totale:',f1)
        
    results=['FINAL',precision/N,recall/N,f1/N,jaccard/N]
    results.extend(scores)
    print(results)
    return results

def create_computato(computato):
    final_dic_sin=dict()
    for k in computato.keys():
        if '-' in k:
            name=k.split('-')[0]
        else:
            name=k
        if name not in final_dic_sin:
            final_dic_sin[k]=set()
        
        elements=computato[k]
        for e in elements:
            values=e.split('-')
            value=values[len(values)-1]
            final_dic_sin[name].add(value)
   
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
    numero_conf_reali=0
    numero_conf_comp=0
    numero_confronti_extra=0
    
    for k in target.keys():
        sing_precision=0
        sing_recall=0
        sing_F1=0
        if k in computato and k not in seen:

            seen.add(k)
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
            numero_conf_reali=numero_conf_reali+len(true_sin)
            numero_conf_comp=numero_conf_comp+len(comp_sin)


            precision=precision+sing_precision
            recall=recall+sing_recall
            f1=f1+sing_F1
    
    results=[name,precision/N,recall/N,f1/N,jaccard/N]
    return results


def get_scores_VAL(f_name,path_comp,path_true):

    indice_invertito='inverted_index_col_names_dic.txt'
    true='column_sinonimi.txt'
    name=f_name.replace('.txt','')
    
    print('computato',path_comp)
    
    
    
    with open(path_comp) as f:
        data=f.read()
        

    
    
    computato=json.loads(data)
    computato=create_computato(computato)
    for k in computato.keys():
        print(k,computato[k])
    
    target=os.path.join(path_true+'\\'+name,true)
    print('target',target)
    with open(target) as f:
        data=f.read()
    target=json.loads(data)
    for k in target.keys():
        print(k,target[k])

    


    path_indice=os.path.join(path_true+'\\'+name,indice_invertito)
    with open(path_indice) as f:
        data=f.read()
    index=json.loads(data)
    
   

    
    precision=0
    recall=0
    f1=0
    jaccard=0
    N=0
    
    numero_confronti_extra=0
    numero_conf_reali=0
    numero_conf_comp=0
    seen=set()
    
    for k in computato.keys():
        if k in computato and k in target and k not in seen:
            N+=1
            
    
        
        sing_precision=0
        sing_recall=0
        sing_F1=0
        if k in target and k not in seen:
            seen.add(k)
           
            comp_sin=set(computato[k])
            true_sin=set(target[k])
           
            
            
            intersezione=comp_sin.intersection(true_sin)
            
            false_positive=comp_sin.difference(true_sin)
            false_negative=true_sin.difference(comp_sin)
            jaccard=jaccard+compute_jaccard(comp_sin,true_sin)
            sing_precision=len(intersezione)/(len(comp_sin)+len(false_positive))
            sing_recall=len(intersezione)/(len(intersezione)+len(false_negative))
            sing_F1=(2*sing_precision*sing_recall)/(sing_recall+sing_precision)
            scores=conta_valori(target,computato,index)
            


            precision=precision+sing_precision
            recall=recall+sing_recall
            f1=f1+sing_F1
        
            
    print(N)
    results=[name,precision/N,recall/N,f1/N,jaccard/N]
    results.extend(scores)
    print(results)
    return results
    



    
def print_perf_preProcessing_module_4clusters():
    path_Clusters='Project\\Schema matching\\DatasetSchemaMatch'
    clusters=os.listdir(path_Clusters)
    colonne=['name','precision','recall','f1','jaccard']
    results=[]
    for f in clusters:
        name_cluster=f
        path=os.path.join(path_Clusters,f)
        results.append(get_scores(name_cluster,path))
        
    

    results=pd.DataFrame(data=[results],columns=colonne)
    tgt_path='Project\\Testing\\Matching\\performace\\perf_per_clusters.csv'
    results.to_csv(tgt_path)
    
def print_perf_preProcessing_module_4schemaMediato():
    colonne=['name','precision','recall','f1','jaccard','Stima_conf_totali','AVG_conf_computati','AVG_conf_reali','Stima_conf_inutili']
    print(len(colonne))
    schema_matching_true='Project\\Schema matching\\MySchemaMatching\\files_matching\\validation_set\\column_sinonimi.txt'
    computato='Project\\Schema matching\\MySchemaMatching\\files_matching\\files_vari\\dic_pre_val.txt'
    index=r'Project\Schema matching\MySchemaMatching\files_matching\files_vari\inverted_index.txt'
    scores_final=get_final_score(schema_matching_true,computato,index)

    scores_final=pd.DataFrame(data=[scores_final],columns=colonne)

    print(scores_final)
    scores_final.to_csv('Project\\Testing\\Matching\\performace\\perf_per_schema_mediato.csv')

def print_perf_Valentine_4clusters():
    path_Clusters_comp=r'Project\Schema matching\MySchemaMatching\clusters\dictionary'
    path_Clusters_true='Project\\Schema matching\\DatasetSchemaMatch'
    name_true='column_sinonimi.txt'
    clusters=os.listdir(path_Clusters_comp)
    colonne=['name','precision','recall','f1','jaccard','Stima_conf_totali','AVG_conf_computati','AVG_conf_reali','Stima_conf_inutili']
    results=[]
    for f in clusters:
        name_cluster=f
        path_comp=os.path.join(path_Clusters_comp,f)
        path_true=os.path.join(path_Clusters_true)
        
        print('======CLUSTER=======:',name_cluster)
        results.append(get_scores_VAL(name_cluster,path_comp,path_true))
    
    results=pd.DataFrame(data=results,columns=colonne)
    
    tgt_path='Project\\Testing\\Matching\\performace\\Valentine_per_clusters.csv'
    results.to_csv(tgt_path)

def print_perf_valentine_final():

    colonne=['name','precision','recall','f1','jaccard','Stima_conf_totali','AVG_conf_computati','AVG_conf_reali','Stima_conf_inutili']
    print(len(colonne))
    schema_matching_true='Project\\Schema matching\\MySchemaMatching\\files_matching\\validation_set\\column_sinonimi.txt'
    computato=r'Project\Testing\Matching\performace\diz_fin.txt'
    index=r'Project\Schema matching\MySchemaMatching\files_matching\files_vari\inverted_index.txt'
    scores_final=get_final_score(schema_matching_true,computato,index)

    scores_final=pd.DataFrame(data=[scores_final],columns=colonne)

    print(scores_final)
    scores_final.to_csv('Project\\Testing\\Matching\\performace\\JaccardMod_per_schema_mediato.csv')


if __name__=='__main__':

    #print_perf_preProcessing_module_4clusters()

    #print_perf_preProcessing_module_4schemaMediato()

    #print_perf_Valentine_4clusters()
    
    print_perf_valentine_final()

    



