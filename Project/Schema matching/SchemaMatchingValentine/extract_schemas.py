import os
import json


def extract(name, file_path, dict_synonyms_path, threshold):
    print("Cluster:", name)

    file = open(file_path)
    dictionary_score = json.load(file)
    file.close()

    synonyms = set()
    for main_token, tokens_score in dictionary_score.items():
        tokens = [k for k, v in tokens_score.items() if v > threshold]
        tmp = set()
        tmp.add(main_token)
        tmp.update(tokens)
        synonyms.add(frozenset(tmp))

    i = 0
    dict_synonyms = {}
    for tokens in synonyms:
        tokens = list(tokens)
        tmp = tokens[0].split("-")[2]
        if tmp not in dict_synonyms.keys():
            dict_synonyms[tmp] = tokens
        else:
            dict_synonyms[tmp + "-" + str(i)] = tokens
            i += 1

    json_obj = json.dumps(dict_synonyms, indent=4)
    f = open(dict_synonyms_path + name + ".txt", "w")
    f.write(json_obj)
    f.close()


def extract_schema_clusters(dictionary_path, dict_synonyms_path, threshold=0.0):
    for filename in os.listdir(dictionary_path):
        file_path = os.path.join(dictionary_path, filename)
        cluster = os.path.splitext(filename)[0]
        extract(cluster, file_path, dict_synonyms_path, threshold)


def extract_schema_clusters_for_final_schema(dictionary_path, dict_synonyms_path, threshold=0.0):
    extract("final_schema", dictionary_path, dict_synonyms_path, threshold)
