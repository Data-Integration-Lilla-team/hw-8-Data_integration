import os
import pandas as pd
from valentine import valentine_match
from valentine.algorithms import JaccardLevenMatcher
import seaborn as sns
import matplotlib.pyplot as plt
import json


# res = {
#     (table1, column1, table2, column2): score
# }
def schema_matching(df1, df2, matcher, df1_name, df2_name):
    matches = valentine_match(df1, df2, matcher, df1_name, df2_name)
    return {(key[0][0], key[0][1], key[1][0], key[1][1]): matches[key] for key in matches}


# transform dictionary d = {a: 1, b: [1,1], c: 2} in d = {a: [1], b: [1,1], c: [2]}
def transform_dictionary(d):
    for key, value in d.items():
        if type(d[key]) != list:
            d[key] = [value]
    return d


# merge two dictionary d1 = {a: 1, b: [1,1], c: 3, d: 1} and d1 = {a: 2, b: [2,1], c: [2]}
# in d3 = {a: [1,2], b: [1,1,2,1], c: [3,2], d: [1]}
def merge_dictionary(dict_1, dict_2):
    dict_1 = transform_dictionary(dict_1)
    dict_2 = transform_dictionary(dict_2)
    tmp = {**dict_1, **dict_2}
    for key in tmp.keys():
        if key in dict_1 and key in dict_2:
            dict_1[key].extend(dict_2[key])
        elif key in dict_2:
            dict_1[key] = dict_2[key]
    return dict_1


def make_dictionary(inverted_index):
    return set(inverted_index.keys())


def get_value_from_list_of_tuples(l, t):
    for tup in l:
        if tup[0] == t:
            return tup[1]
    return 0


def plot_correlation(df, base_path=".\\", title="Matrice di correlazione"):
    fig, ax = plt.subplots(figsize=(20, 20))
    title = title
    file_name = base_path + "\\" + "".join(title.lower()).replace(" ", "_")
    ax.set_title(title)
    # ax.set_xlabel("Token")
    # ax.set_ylabel("Token")
    heatmap = sns.heatmap(df, ax=ax, fmt=".0f", linewidths=2, cmap="Purples", square=True, cbar_kws={"shrink": .5})

    fig.savefig(file_name, bbox_inches='tight', transparent=True)


def run_valentine(name, cluster_path, dictionary_path, plot_path, matcher, cut_df, threshold):
    score_valentine_pair_of_column = {}
    for filename in os.listdir(cluster_path):
        path = os.path.join(cluster_path, filename)

        df1 = pd.read_csv(path).head(cut_df)
        df2 = pd.read_csv(path).head(cut_df)

        if len(df1.columns) > threshold:
            df1 = df1.head(cut_df)
            df2 = df2.head(cut_df)

        print("Matching cluster" + "(" + name + ")" + "(" + matcher.__class__.__name__ + "): " + path)
        tmp = schema_matching(df1, df2, matcher, "table1", "table2")
        score_valentine_pair_of_column = merge_dictionary(score_valentine_pair_of_column, tmp)

    inverted_index = {}
    for match_tuple, score in score_valentine_pair_of_column.items():

        if match_tuple[1] not in inverted_index.keys():
            inverted_index[match_tuple[1]] = []
        if match_tuple[3] not in inverted_index.keys():
            inverted_index[match_tuple[3]] = []

        inverted_index[match_tuple[1]].append((match_tuple[3], score))
        inverted_index[match_tuple[3]].append((match_tuple[1], score))

    mean_inverted_index = {}
    for token, index in inverted_index.items():
        if token not in mean_inverted_index.keys():
            mean_inverted_index[token] = []
        for e in set([i[0] for i in index]):
            tmp = [k[1][0] for k in index if k[0] == e]
            mean_inverted_index[token].append((e, (sum(tmp) / len(tmp))))

    correlation_matrix = {}
    dictionary = make_dictionary(mean_inverted_index)
    for token, values in mean_inverted_index.items():
        terms_of_token = [e[0] for e in values]
        correlation_matrix[token] = {}
        for term in dictionary:
            if term not in terms_of_token:
                correlation_matrix[token][term] = 0
            else:
                correlation_matrix[token][term] = get_value_from_list_of_tuples(values, term)

    # save correlation_matrix_cluster
    json_obj = json.dumps(correlation_matrix, indent=4)
    f = open(dictionary_path + name + ".txt", "w")
    f.write(json_obj)
    f.close()

    df = pd.DataFrame(correlation_matrix)
    plot_correlation(df, base_path=plot_path, title="Matrice di correlazione-" + name)


def score_valentine_and_matrix_correlation(csv_columns_path, dictionary_path, plot_path, cut_df=-1, threshold=8):
    matcher = JaccardLevenMatcher()
    for cluster_folder_name in os.listdir(csv_columns_path):
        cluster_path = os.path.join(csv_columns_path, cluster_folder_name)
        run_valentine(cluster_folder_name, cluster_path, dictionary_path, plot_path, matcher, cut_df, threshold)


def score_valentine_and_matrix_correlation_for_final_schema(csv_columns_path, dictionary_path, plot_path, cut_df=-1, threshold=8):
    matcher = JaccardLevenMatcher()
    run_valentine("final_schema", csv_columns_path, dictionary_path, plot_path, matcher, cut_df, threshold)
