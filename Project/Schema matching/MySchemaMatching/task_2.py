import os
from itertools import combinations
import pandas as pd
import json
from multiprocessing import Pool

def jaccard(set1, set2):
    if len(set1) > 0 or len(set2) > 0:
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)
    return 0


def calculate_jaccard(columns):
    c1, c2, data, threshold = columns
    s = jaccard(set(data[c1]), set(data[c2]))
    if s > threshold:
        return (c1, c2)
    return None


def extract_schema_paolo(directory, name, final_schema_directory, threshold, format, head):

    result_jaccard = {}

    for filename in os.listdir(directory):
        print(filename)
        file = os.path.join(directory, filename)
        df = pd.read_csv(file, encoding="utf-8")
        df = df.sample(frac=head)

        combs = list(combinations(df.columns, 2))
        print("Numbero di confronti: ", len(combs))

        # Calcolare le colonne che soddisfano la soglia in parallelo
        with Pool() as p:
            results = p.map(calculate_jaccard, [(c1, c2, df, threshold) for c1, c2 in combs])

        # Aggiungere le colonne che soddisfano la soglia ai risultati finali
        for r in results:
            if r is not None:
                c1, c2 = r
                if c1 not in result_jaccard:
                    result_jaccard[c1] = set()
                if c2 not in result_jaccard:
                    result_jaccard[c2] = set()

                result_jaccard[c1].add(c2)
                result_jaccard[c2].add(c1)

    s = set()
    for main_token, tokens in result_jaccard.items():
        tmp = set()
        tmp.add(main_token)
        tmp.update(tokens)
        s.add(frozenset(tmp))

    i = 0
    dict_synonyms = {}
    for tokens in s:
        tokens = list(tokens)
        tmp = tokens[0].split("-")[1]
        if tmp not in dict_synonyms.keys():
            dict_synonyms[tmp] = tokens
        else:
            dict_synonyms[tmp + "-" + str(i)] = tokens
            i += 1

    json_obj = json.dumps(dict_synonyms, indent=4)
    f = open(final_schema_directory + name + format, "w")
    f.write(json_obj)
    f.close()

    print("\n\n")


def schema_cluster(directory, final_schema_directory, threshold, format, head):
    for dirname in os.listdir(directory):
        print(dirname)
        cluster = os.path.join(directory, dirname)
        extract_schema_paolo(cluster, dirname, final_schema_directory, threshold, format, head)



def schema_final(directory, final_schema_directory, threshold, format, head):
    extract_schema_paolo(directory, "finalschema", final_schema_directory, threshold, format, head)
