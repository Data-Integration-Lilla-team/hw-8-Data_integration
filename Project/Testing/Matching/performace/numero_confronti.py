import json
import os
import pandas as pd
def conta_confronti_in_lista(lista_sinonimi_k,indice):
    confronti=0
    for sin in lista_sinonimi_k:
        if sin in indice:
            confronti+=len(indice[sin])
    return confronti


def calc_confronti(sinonimi,indice):
    confronti=0
    for k in sinonimi.keys():
        confronti=confronti+conta_confronti_in_lista(set(sinonimi[k]),indice)
    return confronti



def conta_valori(true, computed, index):
    #calolca reali
    determinatore=len(true.keys())
    confronti_reali=calc_confronti(true,index)/determinatore
    confronti_computati=calc_confronti(computed,index)
    confronti_extra=confronti_computati-confronti_reali

    return [confronti_computati,confronti_computati/determinatore,confronti_reali,confronti_extra/2]


def extract_data(path):
    with open(path,'r') as f:
                data=f.read()

    return json.loads(data)

if __name__=='__main__':

    dic_pre_val_name='dic_pre_val.txt'

    sinonimi_reali='column_sinonimi.txt'

    indice_invertito='inverted_index_col_names_dic.txt'

    name_cluster=''

    path_base='Project\\Schema matching\\DatasetSchemaMatch'

    ds=[]

    colonne=['name','Stima_Conf_totali','AVG_conf_computati','AVG_conf_reali','AVG_conf_inutili']


    for f in os.listdir(path_base):
        name_cluster=str(f)
        row=[name_cluster]
        path_dic_pre_val_cluster=path_base+'\\'+name_cluster+'\\'+dic_pre_val_name
        path_sinonimi_reali=path_base+'\\'+name_cluster+'\\'+sinonimi_reali
        indice=path_base+'\\'+name_cluster+'\\'+indice_invertito

        comp=extract_data(path_dic_pre_val_cluster)
        true=extract_data(path_sinonimi_reali)
        index=extract_data(indice)

        row.extend(conta_valori(true,comp,index))
    
        ds.append(row)
    

    data=pd.DataFrame(data=ds,columns=colonne)

    print('data',data.columns.to_list())

    data.to_csv(r'Project\Testing\Matching\performace\confronti_pre_precessing_nei_cluster.csv')
    data=data.loc[:,~data.columns.str.contains('name')]

    print('data',data.columns.to_list())

    performance=pd.read_csv(r'Project\Testing\Matching\performace\perf_per_clusters.csv')

    performance=performance.loc[:,~performance.columns.str.contains('Unn')]
    
   

    



    print('1',performance.columns.to_list())

    

    
    
    
    
    per_col=performance.columns.to_list()
    per_col.extend(data.columns.to_list())
    

    print('3.',per_col)

    

   

   
    
    
    
    data=pd.concat([data,performance], axis='columns')
    

   
    

    #data=data.drop(['avg comp inutili','conf reali','conf computati','Unnamed: 0'],axis='columns')

    data=data[per_col]
    data.to_csv(r'Project\Testing\Matching\performace\perf_per_clusters_fin.csv')







        


    
    
            



    

    ris=conta_valori(true,comp,index)
    print(ris[0],'Computati: ',ris[1],'\tVeri: ',ris[2], '\tExtra: ',ris[3])
