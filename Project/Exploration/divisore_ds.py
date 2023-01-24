#suddivisione dei dataset per nome.
#raggruppiamo i dataset della stessa sorgente
import pandas as pd
import json
import os


def create_cluster(json):
    cluster_dataset_by_name=dict()
    for i in range (0,44):
        source_name=json_object[i]['dataset_name']
        team_name=json_object[i]['group_name']
        df = pd.read_json(json_object[i]["dataset"], encoding="utf-8").T
        tupla=(team_name,df)

        if source_name in cluster_dataset_by_name:
            cluster_dataset_by_name[source_name].append(tupla)

        else:
            cluster_dataset_by_name[source_name]=[tupla]

    return cluster_dataset_by_name



with open("Project\\Dataset\\Original\\datasets.json", 'r', encoding='utf-8') as f:
    json_object = json.loads(f.read())
    f.close()

#ma


cluster_dataset_by_name=create_cluster(json_object)

base_path='Project\\Dataset\\Clusters'

for k,v in cluster_dataset_by_name.items():
    name_ds=k
    elements=cluster_dataset_by_name[k]
    os.mkdir(base_path+'\\'+name_ds)
    for e in elements:
        team_name=e[0]
        ds=e[1]
        
        tgt_path=base_path+'\\'+name_ds+'\\'+team_name
        print(tgt_path)
        ds.to_csv(tgt_path)


print(cluster_dataset_by_name['companiesmarketcap'][0][1])
print(cluster_dataset_by_name['companiesmarketcap'][0][0])

