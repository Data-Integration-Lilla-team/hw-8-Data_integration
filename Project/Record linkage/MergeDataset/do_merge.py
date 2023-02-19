import pandas as pd
import numpy as np

class Merger:

    def __init__(self, filename):
        self.path_save = r"C:\hw-8-Data_integration\Project\Record linkage\DATASETS\Merged Datasets" + '\\' + filename
        self.prediction = pd.read_csv(r"C:\hw-8-Data_integration\Project\Record linkage\DATASETS\Predictions" + '\\' + filename, low_memory=False)
        self.dataset = pd.read_csv(r"C:\hw-8-Data_integration\Project\Record linkage\DATASETS\Dataset separati per lettera" + '\\' + filename)
        self.threshold = 0.5
        self.dict_match = {}
        self.final_tuple_match = []

    def getListId(self):
        id_match =[]
        flat_list = [item for sublist in self.final_tuple_match for item in sublist]
        for value in flat_list:
            if value not in id_match:
                id_match.append(value)
        return id_match

    def most_frequent(self, l):
        if len(l) > 0:
            return max(set(l), key = l.count)
        return np.nan
    
    def dict_list_to_dict_first_value(d):
        return {k: v[0] for k, v in d.items() if len(v) >= 1}

    def getMatch(self):
        self.prediction = self.prediction.reset_index()
        for index, row in self.prediction.iterrows():
            if row["match_score"] > self.threshold:
                score = row["match_score"]
                l_id = row['ltable_id']
                r_id = row['rtable_id']
                if l_id not in self.dict_match.keys():
                    self.dict_match[l_id] = set()
                self.dict_match[l_id].add(r_id) #((r_id, score))
                if r_id not in self.dict_match.keys():
                    self.dict_match[r_id] = set()
                self.dict_match[r_id].add(l_id) #((l_id, score))

        
        for key, values in self.dict_match.items():
            ok = False
            for sublist in self.final_tuple_match:
                if key in sublist:
                    sublist.update(values)
                    ok = True
            if not ok:
                new_set = set(values)
                self.final_tuple_match.append(new_set)
        

    def merge_list_of_dict(self, values):
        keys = list(self.dataset.columns)
        dict_of_merge = {k: [] for k in keys}
        for value in values:
            tmp = Merger.dict_list_to_dict_first_value(self.dataset.loc[self.dataset['id'] == value].to_dict(orient="list"))
            for k, v in tmp.items():
                if v is not np.nan:
                    dict_of_merge[k].append(v)
        return {k: Merger.most_frequent(self, v) for k, v in dict_of_merge.items()}


    def getFile(self):
        res = []
        for values in self.final_tuple_match:
            res.append(Merger.merge_list_of_dict(self, values = values))
        output1 = pd.DataFrame(res)

        list_id = Merger.getListId(self)
        res2 = []
        for index, row in self.dataset.iterrows():
            if row['id'] not in list_id:
                res2.append(row)
        output2 = pd.DataFrame(res2)
        list_df = [output1, output2]

        output = pd.concat(list_df, ignore_index = True)

        output.to_csv(self.path_save , index = False)