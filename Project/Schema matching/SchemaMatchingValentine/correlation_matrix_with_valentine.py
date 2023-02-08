import os
import shutil
import pandas as pd
from valentine import valentine_match
from valentine.algorithms import JaccardLevenMatcher
import random
import seaborn as sns
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np

import json
import re


def get_path_group_name(cluster_path):
    path_group_name = {}
    for filename in os.listdir(cluster_path):
        dataset_path = os.path.join(cluster_path, filename)
        path_group_name[os.path.splitext(filename)[0]] = dataset_path
    return path_group_name


def get_inverted_index_column_name_file(cluster_path):
    inverted_index = {}
    for filename in os.listdir(cluster_path):
        file_path = os.path.join(cluster_path, filename)
        df = pd.read_csv(file_path)
        group_name = os.path.splitext(filename)[0]
        for column in list(df.columns):
            if column not in inverted_index.keys():
                inverted_index[column] = []
            inverted_index[column].append(group_name)
    return inverted_index



