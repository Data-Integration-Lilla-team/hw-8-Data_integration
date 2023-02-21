import pandas as pd
import os
def get_info(path):
    df=pd.read_csv(path)
    num_colonne=len(df.columns.to_list())
    numero_righe=len(df)
    return (num_colonne,numero_righe)
if __name__=='__main__':
    path_base='Project\\Dataset\\ClustersCSV'
    #navigo tra i cluster
    dizionario_cluster=dict()
    for files in os.listdir(path_base):
        nome_file=str(files)
        path_cluster=os.path.join(path_base,nome_file)
        dizionario_cluster[nome_file]=[]
        
        for csv in os.listdir(path_cluster):
            #prendo il file
            
            
            path_ds=os.path.join(path_cluster,csv)
            
            info=get_info(path_ds)
            
            informazioni=(csv,info[0],info[1])
            dizionario_cluster[nome_file].append(informazioni)
    
    conta=0
    elemento=[]
    colonne=['cluster','ds', 'numero_colonne', 'numero_righe']
    for k in dizionario_cluster.keys():
        print(dizionario_cluster[k])
        info=[]
        info.append(dizionario_cluster[k][0][0])
        info.append(dizionario_cluster[k][0][1])
        info.append(dizionario_cluster[k][0][2])
        info.insert(0,k)
        elemento.append(info)
    print(elemento)

    data=pd.DataFrame(data=elemento,columns=colonne)

    print(data)
        
            
