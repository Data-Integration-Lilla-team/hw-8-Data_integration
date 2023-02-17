
from cluster_group_columns import make_cluster_columns
from extract_schema import schema_cluster
from make_schema import make_schema_cluster
import os
import shutil
import warnings
warnings.filterwarnings('ignore')


def remove_and_make_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)


def task1(datasets_base_path, info_path, filename_synonym, csv_columns_path):

    print("\nMake cluster columns\n")
    remove_and_make_dir(csv_columns_path)
    make_cluster_columns(datasets_base_path, info_path, filename_synonym, csv_columns_path)


def task2(csv_columns_path, dictionary_path):
    print("\nExtract schema\n")
    remove_and_make_dir(dictionary_path)
    schema_cluster(csv_columns_path, dictionary_path, 0.2)


def task3(datasets_base_path, dict_final_synonyms_path, schema_path):
    print("\nMake schemas\n")
    remove_and_make_dir(schema_path)
    make_schema_cluster(datasets_base_path, dict_final_synonyms_path, schema_path)


if __name__ == '__main__':

    clusters_datasets_base_path = "..\\..\\Dataset\\ClusterParsed\\"
    clusters_info_path = "..\\DatasetSchemaMatch\\"
    clusters_filename_synonym = "dic_pre_val.txt"

    clusters_columns = ".\\clusters\\columns\\"
    clusters_dictionary = ".\\clusters\\dictionary\\"
    clusters_final_dictionary = ".\\clusters\\final_dictionary\\"
    clusters_schema = ".\\clusters\\schema\\"

    #task1(clusters_datasets_base_path, clusters_info_path, clusters_filename_synonym, clusters_columns)
    #task2(clusters_columns, clusters_dictionary)
    task3(clusters_datasets_base_path, clusters_final_dictionary, clusters_schema)
