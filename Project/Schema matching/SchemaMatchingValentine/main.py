
from cluster_group_columns import make_cluster_columns, make_cluster_columns_for_final_schema
from excract_score_valentine import score_valentine_and_matrix_correlation, score_valentine_and_matrix_correlation_for_final_schema
from extract_schemas import extract_schema_clusters, extract_schema_clusters_for_final_schema
from make_schemas import make_schema_cluster, make_schema_cluster_for_final_schema
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


def task5(datasets_base_path, info_path, filename_synonym, csv_columns_path):
    print("\nMake cluster columns\n")
    remove_and_make_dir(csv_columns_path)
    make_cluster_columns_for_final_schema(datasets_base_path, info_path, filename_synonym, csv_columns_path)


def task6(csv_columns_path, dictionary_path, plot_path, cut_df, threshold):
    print("\nScore Valentine and matrix correlation\n")
    remove_and_make_dir(dictionary_path)
    remove_and_make_dir(plot_path)
    score_valentine_and_matrix_correlation_for_final_schema(csv_columns_path, dictionary_path, plot_path, cut_df, threshold)


def task7(dictionary_path, dict_synonyms_path, threshold):
    print("\nExtract schemas\n")
    remove_and_make_dir(dict_synonyms_path)
    extract_schema_clusters_for_final_schema(dictionary_path, dict_synonyms_path, threshold)


def task8(datasets_base_path, dict_synonyms_path, schema_path):
    print("\nMake schemas\n")
    remove_and_make_dir(schema_path)
    make_schema_cluster_for_final_schema(datasets_base_path, dict_synonyms_path, schema_path)


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
    task4(clusters_datasets_base_path, clusters_final_synonyms, clusters_schema)

    final_datasets_base_path = ".\\clusters\\schema\\"
    final_info_path = "..\\DatasetSchemaMatch\\"
    final_filename_synonym = "dic_pre_val.txt"
    final_schema_columns = ".\\final_schema\\columns\\"
    final_schema_dictionary_score = ".\\final_schema\\dictionary_score\\"
    final_schema_plot = ".\\final_schema\\plot\\"
    final_schema_synonyms = ".\\final_schema\\synonyms\\"
    final_schema_final_synonyms = ".\\final_schema\\final_synonyms\\"
    final_schema_schema = ".\\final_schema\\schema\\"

    #task5(final_datasets_base_path, final_info_path, final_filename_synonym, final_schema_columns)
    #task6(final_columns, final_dictionary_score, final_plot, 3000, 8)
    #task7(final_dictionary_score, final_synonyms, 0.1)
    #task8(final_datasets_base_path, final_final_synonyms, final_schema)



