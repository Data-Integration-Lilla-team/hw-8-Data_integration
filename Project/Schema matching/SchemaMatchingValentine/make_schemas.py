import os
import pandas as pd
import json

def make2(cluster_path, cluster_folder_name, dict_synonyms_path, schema_path, index):

    print("Cluster:", cluster_folder_name)

    file_synonyms_path = os.path.join(dict_synonyms_path, cluster_folder_name + ".txt")
    file = open(file_synonyms_path)
    dict_synonyms = json.load(file)
    file.close()

    inverted_synonym_index = {}
    for main_token, tokens in dict_synonyms.items():
        for token in tokens:
            inverted_synonym_index[token] = main_token

    base_schema = list(dict_synonyms.keys())
    print(base_schema)

    df = pd.DataFrame(columns=base_schema)
    for filename in os.listdir(cluster_path):

        dataset_path = os.path.join(cluster_path, filename)
        group_name = os.path.splitext(filename)[0]

        column_rename = {}
        tmp = pd.read_csv(dataset_path)
        for column in list(tmp.columns):
            if column in inverted_synonym_index.keys():
                column_rename[column] = inverted_synonym_index[column]

        df_tmp = pd.read_csv(dataset_path)
        df_tmp = df_tmp.rename(columns=column_rename)
        df_tmp = df_tmp[df_tmp.columns.intersection(column_rename.values())]
        print(dataset_path)
        print(column_rename)
        print(list(df_tmp.columns))
        df = pd.concat([df, df_tmp])

    # df = df.reset_index()
    df.to_csv(schema_path + cluster_folder_name + ".csv", index=index)

def make(cluster_path, cluster_folder_name, dict_synonyms_path, schema_path, index):
    if len(os.listdir(cluster_path)) > 1:

        print("Cluster:", cluster_folder_name)

        file_synonyms_path = os.path.join(dict_synonyms_path, cluster_folder_name + ".txt")
        file = open(file_synonyms_path)
        dict_synonyms = json.load(file)
        file.close()

        inverted_synonym_index = {}
        for main_token, tokens in dict_synonyms.items():
            for token in tokens:
                tmp = token.split("-")
                if len(tmp) == 3:
                    inverted_synonym_index[tmp[2]] = main_token
                else:
                    inverted_synonym_index[token] = main_token

        base_schema = list(dict_synonyms.keys())
        print(base_schema)

        df = pd.DataFrame(columns=base_schema)
        for filename in os.listdir(cluster_path):

            dataset_path = os.path.join(cluster_path, filename)
            group_name = os.path.splitext(filename)[0]

            column_rename = {}
            tmp = pd.read_csv(dataset_path)
            for column in list(tmp.columns):
                if column in inverted_synonym_index.keys():
                    column_rename[column] = inverted_synonym_index[column]

            df_tmp = pd.read_csv(dataset_path)
            df_tmp = df_tmp.rename(columns=column_rename)
            df_tmp = df_tmp[df_tmp.columns.intersection(column_rename.values())]
            print(dataset_path)
            print(list(df_tmp.columns))
            df = pd.concat([df, df_tmp])

        #df = df.reset_index()
        df.to_csv(schema_path + cluster_folder_name + ".csv", index=index)


def make_schema_cluster(datasets_base_path, dict_synonyms_path, schema_path):
    for cluster_folder_name in os.listdir(datasets_base_path):
        cluster_path = os.path.join(datasets_base_path, cluster_folder_name)
        make2(cluster_path, cluster_folder_name, dict_synonyms_path, schema_path, False)


def make_schema_cluster_for_final_schema(datasets_base_path, dict_synonyms_path, schema_path):
    make(datasets_base_path, "idea_final_schema", dict_synonyms_path, schema_path, False)
