import os
import pandas as pd
import json


def get_path_group_name(cluster_path):
    path_group_name = {}
    for filename in os.listdir(cluster_path):
        dataset_path = os.path.join(cluster_path, filename)
        path_group_name[os.path.splitext(filename)[0]] = dataset_path
    return path_group_name


def get_inverted_index_column_name_file(path_folder):
    inverted_index = {}
    for filename in os.listdir(path_folder):
        file_path = os.path.join(path_folder, filename)
        df = pd.read_csv(file_path)
        group_name = os.path.splitext(filename)[0]
        for column in list(df.columns):
            if column not in inverted_index.keys():
                inverted_index[column] = []
            inverted_index[column].append(group_name)
    return inverted_index


def save_cluster_columns(js_synonym, js_inverted_index, dict_filename_paths, path_to_save_csv):
    list_of_columns = []
    for main_token, tokens in js_synonym.items():

        if tuple(tokens) not in list_of_columns:

            list_of_columns.append(tuple(tokens))

            data_column_cluster = {}

            for token in tokens:

                filename_with_token = js_inverted_index[token]
                for filename in filename_with_token:
                    df_tmp = pd.read_csv(dict_filename_paths[filename])
                    column = df_tmp[token]
                    data_column_cluster[filename + "-" + token] = column

            df = pd.DataFrame(data_column_cluster)
            df.to_csv(path_to_save_csv + main_token + ".csv", index=False)


def make_cluster_columns_cluster(datasets_base_path, info_path, filename_synonym, csv_columns_path):
    for cluster_folder_name in os.listdir(datasets_base_path):

        print("Cluster:", cluster_folder_name)

        tmp = os.path.join(info_path, cluster_folder_name)

        synonym_path = os.path.join(tmp, filename_synonym)
        with open(synonym_path) as f:
            data = f.read()
        js_synonym = json.loads(data)

        cluster_path = os.path.join(datasets_base_path, cluster_folder_name)
        paths = get_path_group_name(cluster_path)
        
        js_inverted_index = get_inverted_index_column_name_file(cluster_path)

        cluster_path = csv_columns_path + cluster_folder_name + "\\"
        os.mkdir(cluster_path)
        save_cluster_columns(js_synonym, js_inverted_index, paths, cluster_path)


def make_cluster_columns_final(datasets_base_path, info_path, filename_synonym, csv_columns_path):

    js_inverted_index = get_inverted_index_column_name_file(datasets_base_path)

    synonym_path = os.path.join(info_path, filename_synonym)
    with open(synonym_path) as f:
        data = f.read()
    js_synonym = json.loads(data)

    dict_filename_paths = {}
    for filename in os.listdir(datasets_base_path):
        dict_filename_paths[os.path.splitext(filename)[0]] = os.path.join(datasets_base_path, filename)

    save_cluster_columns(js_synonym, js_inverted_index, dict_filename_paths, csv_columns_path)
