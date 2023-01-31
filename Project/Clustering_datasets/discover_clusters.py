import pandas as pd
from pandasql import sqldf


if __name__=='__main__':
    name='clustered_rows.csv'
    final_path='Project\\Dataset\\Clusters_CSV\\parsed\\companiesmarketcap\\'
    file_name=final_path+name

    clusters=pd.read_csv(file_name)
    print(clusters.head(10))
    cluster_labels=set(clusters['cluster'])
    print(cluster_labels)

    pysqldf = lambda q: sqldf(q, globals())

    for i in cluster_labels:
        print(i)
        rslt_df = clusters.loc[clusters['cluster'] == i]
        print(rslt_df)



    
