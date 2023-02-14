
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


def task1(datasets_base_path, info_path, filename_synonym, csv_columns_path):

    print("\nMake cluster columns\n")
    remove_and_make_dir(csv_columns_path)
    make_cluster_columns(datasets_base_path, info_path, filename_synonym, csv_columns_path)


def task2(csv_columns_path, dictionary_path, plot_path, cut_df, threshold):
    print("\nScore Valentine and matrix correlation\n")
    remove_and_make_dir(dictionary_path)
    remove_and_make_dir(plot_path)
    score_valentine_and_matrix_correlation(csv_columns_path, dictionary_path, plot_path, cut_df, threshold)


def task3(dictionary_path, dict_synonyms_path, threshold):
    print("\nExtract schemas\n")
    remove_and_make_dir(dict_synonyms_path)
    extract_schema_clusters(dictionary_path, dict_synonyms_path, threshold)


def task4(datasets_base_path, dict_final_synonyms_path, schema_path):
    print("\nMake schemas\n")
    remove_and_make_dir(schema_path)
    make_schema_cluster(datasets_base_path, dict_final_synonyms_path, schema_path)


if __name__ == '__main__':

    clusters_datasets_base_path = "..\\..\\Dataset\\ClusterParsed\\"
    clusters_info_path = "..\\DatasetSchemaMatch\\"
    clusters_filename_synonym = "dic_pre_val.txt"
    clusters_columns = ".\\clusters\\columns\\"
    clusters_dictionary_score = ".\\clusters\\dictionary_score\\"
    clusters_plot = ".\\clusters\\plot\\"
    clusters_synonyms = ".\\clusters\\synonyms\\"
    clusters_final_synonyms = ".\\clusters\\final_synonyms\\"
    clusters_schema = ".\\clusters\\schema\\"

    #task1(clusters_datasets_base_path, clusters_info_path, clusters_filename_synonym, clusters_columns)
    #task2(clusters_columns, clusters_dictionary_score, clusters_plot, 3000, 8)
    #task3(clusters_dictionary_score, clusters_synonyms, 0.1)
    #task4(clusters_datasets_base_path, clusters_final_synonyms, clusters_schema)
