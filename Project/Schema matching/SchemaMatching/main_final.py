import json

from cluster_group_columns import make_cluster_columns_for_final_schema
import os
import shutil
import warnings

from extract_schema import schema_final
from make_schema import make_schema_final

warnings.filterwarnings('ignore')


def remove_and_make_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)

def reformat_json(path):
    with open(path, "wr") as f:
        tmp = json.loads(f.read())
        json_obj = json.dumps(tmp, indent=4)
        f.write(json_obj)
        f.close()


def task1(datasets_base_path, info_path, filename_synonym, csv_columns_path):
    print("\nMake cluster columns\n")
    remove_and_make_dir(csv_columns_path)
    make_cluster_columns_for_final_schema(datasets_base_path, info_path, filename_synonym, csv_columns_path)


def task2(csv_columns_path, dictionary_path):
    print("\nExtract schema\n")
    remove_and_make_dir(dictionary_path)
    schema_final(csv_columns_path, dictionary_path)


def task3(datasets_base_path, dict_synonyms_path, schema_path):
    print("\nMake schema\n")
    remove_and_make_dir(schema_path)
    make_schema_final(datasets_base_path, dict_synonyms_path, schema_path)


if __name__ == '__main__':

    final_datasets_base_path = ".\\clusters\\schema\\"
    final_info_path = ".\\files_matching\\files_vari"
    final_filename_synonym = "dic_pre_val.txt"

    final_schema_columns = ".\\final_schema\\columns\\"
    final_schema_dictionary = ".\\final_schema\\dictionary\\"
    final_schema_final_dictionary = ".\\final_schema\\final_dictionary\\"
    final_schema_schema = ".\\final_schema\\schema\\"

    #task1(final_datasets_base_path, final_info_path, final_filename_synonym, final_schema_columns)
    task2(final_schema_columns, final_schema_dictionary)
    #task3(final_datasets_base_path, final_schema_final_dictionary, final_schema_schema)
