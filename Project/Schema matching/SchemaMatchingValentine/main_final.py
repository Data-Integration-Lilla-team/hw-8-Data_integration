from cluster_group_columns import make_cluster_columns_for_final_schema
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
    make_cluster_columns_for_final_schema(datasets_base_path, info_path, filename_synonym, csv_columns_path)


def task2(csv_columns_path, dictionary_path, plot_path, cut_df, threshold):
    print("\nScore Valentine and matrix correlation\n")
    remove_and_make_dir(dictionary_path)
    remove_and_make_dir(plot_path)
    #score_valentine_and_matrix_correlation_for_final_schema(csv_columns_path, dictionary_path, plot_path, cut_df, threshold)


def task3(dictionary_path, dict_synonyms_path, threshold):
    print("\nExtract schemas\n")
    remove_and_make_dir(dict_synonyms_path)
    #extract_schema_clusters_for_final_schema(dictionary_path, dict_synonyms_path, threshold)


def task4(datasets_base_path, dict_synonyms_path, schema_path):
    print("\nMake schemas\n")
    remove_and_make_dir(schema_path)
    #make_schema_cluster_for_final_schema(datasets_base_path, dict_synonyms_path, schema_path)


if __name__ == '__main__':

    final_datasets_base_path = ".\\clusters\\schema_parsed\\"
    final_info_path = ".\\files_matching\\files_vari"
    final_filename_synonym = "dic_pre_val.txt"
    final_schema_columns = ".\\final_schema\\columns\\"
    final_schema_dictionary_score = ".\\final_schema\\dictionary_score\\"
    final_schema_plot = ".\\final_schema\\plot\\"
    final_schema_synonyms = ".\\final_schema\\synonyms\\"
    final_schema_final_synonyms = ".\\final_schema\\final_dictionary\\"
    final_schema_schema = ".\\final_schema\\schema\\"

    #task1(final_datasets_base_path, final_info_path, final_filename_synonym, final_schema_columns)
    #task2(final_schema_columns, final_schema_dictionary_score, final_schema_plot, 10000, 5)
    #task3(final_schema_dictionary_score, final_schema_synonyms, 0.1)
    #task4(final_datasets_base_path, final_schema_final_synonyms, final_schema_schema)
