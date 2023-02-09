
from cluster_group_columns import make_cluster_columns
from excract_score_valentine import score_valentine_and_matrix_correlation
from extract_schemas import extract_schema_clusters
from make_schemas import make_schema_cluster
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


def task1():

    print("\nMake cluster columns\n")
    remove_and_make_dir(csv_columns_path)
    make_cluster_columns(datasets_base_path, info_path, filename_synonym, csv_columns_path)


def task2():
    print("\nScore Valentine and matrix correlation\n")
    remove_and_make_dir(dictionary_path)
    remove_and_make_dir(plot_path)
    score_valentine_and_matrix_correlation(csv_columns_path, dictionary_path, plot_path, 1000, 8)


def task3():
    print("\nExtract schemas\n")
    remove_and_make_dir(dict_synonyms_path)
    extract_schema_clusters(dictionary_path, dict_synonyms_path, 0.1)


def task4():
    print("\nMake schemas\n")
    remove_and_make_dir(schema_path)
    make_schema_cluster(datasets_base_path, dict_final_synonyms_path, schema_path)


if __name__ == '__main__':

    datasets_base_path = "..\\..\\Dataset\\ClusterParsed\\"
    info_path = "..\\DatasetSchemaMatch\\"
    filename_synonym = "dic_pre_val.txt"
    csv_columns_path = ".\\columns\\"
    dictionary_path = ".\\dictionary_score\\"
    plot_path = ".\\plot\\"
    dict_synonyms_path = ".\\synonyms\\"
    dict_final_synonyms_path = ".\\final_synonyms\\"
    schema_path = ".\\schema\\"

    #task1()
    #task2()
    #task3()
    task4()





