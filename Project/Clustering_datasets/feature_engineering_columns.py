import re
from string import punctuation
from collections import Counter
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
class FeatureExtraction:
    def __init__(self):
        self.features=['column_name','type_of_data',
        'type_of_string','avg_length_of_field','var_length','std_dev_length','ratio_white_space_length','ratio_num_val',
        'min_val(int)','max_val(int)','avg(int)','variance','std_dev']
    

        # da adornare con data
    def compute_features(self, col):
        integer=1
        string_t=0
        if isinstance(col.head(1)[0], str):
            return string_t
        else:
            return integer

    def compute_features_for_int(self, col):
        integer_features=[]
        integer_features.append(col.min(skipna=True))
        integer_features.append(col.max(skipna=True))
        integer_features.append(col.mean())
        integer_features.append(col.var())
        integer_features.append(col.std())
        return integer_features

    def compute_type(self, val):
        if '_perc' in val:
            return 1
        
        if 'rank_' in val:
            return 2

        if 'doll_' in val:
            return 3
        
        else:
            return 4

    def compute_ratio_of_whitespace(self,col):

        mean_ratio=(col.str.count(' ') / col.str.len()).mean()
        return mean_ratio

    def compute_ratio_of_numeric_values(self, col):
        ratio=0
        total=len(col)
        for val in col:
            string_len=len(str(val))
            temp=str(val)
            numeric_val=len(re.sub("[^0-9]", "", temp))
            ratio=ratio+(numeric_val/string_len)

        return ratio/total


    
        

                
           

    def compute_features_for_string(self, col):
        feature_vector=[]

        #type of string
        feature_vector.append(self.compute_type(col.head(1)[0]))

        #avg len of strings
        feature_vector.append(col.str.len().mean())

        #var len of strings
        feature_vector.append(col.str.len().var())

        #std deviation of strings lenght
        feature_vector.append(col.str.len().std())

        #ratio of whitespaces
        feature_vector.append(self.compute_ratio_of_whitespace(col))

        #ratio of numeric values

        feature_vector.append(self.compute_ratio_of_numeric_values(col))

        return feature_vector

    

    
    def create_dataset(self,data,cols):
        list_of_data=[]
        
        for k in data.keys():
            for e in data[k]:
                list_of_data.append(e)
        

        dataset=pd.DataFrame(data=list_of_data,columns=cols)
        return dataset







         
        




    #features-> 
    #nome campo
    #1. tipo di dato: string 0, int 1, data (?)
    #2. (string)type of str->perc_:1, b or t or doll_: 2, rank_=3, other=4
    #3. (string)avg_lenght of fiald (if string)
    #4. (string)variance of lenght
    #5. (string) std deviation of lenght
    #6. (string)ratio of whitespace fields
    
    #7. (string)ratio of numeric values
    #8. (int)min val
    #9. (int)max val
    #10. (int)avg
    #11 (int)variance
    #12 (int) std deviation
    def get_features_name(self):
        return self.features

    #normalizzazione features
    def get_scaled_dataframe(self,ds):
        scaler=MinMaxScaler()
        x=[]
        for c in self.features:
            if 'column_name' not in c:
                scaler.fit(ds[[c]])
                ds[c]=scaler.transform(ds[[c]])
            
        return ds


    def extract_feature(self,ds,k):
        ds_features=[]                  #lista di tuple (nome campo, vettore)
        list_of_names_columns=ds.columns.values.tolist()
        i=0
        for col in ds.columns:
            
            name_column=k+'_'+list_of_names_columns[i]
            vector_features=[name_column]
            type_of_col=self.compute_features(ds[col])
            vector_features.append(type_of_col)
            if type_of_col==0:  #calcola le feature per la stringa, i valori numerici verranno settati a 0
                
                vector_features=vector_features+self.compute_features_for_string(ds[col])
                vector_features=vector_features+[0,0,0,0,0]
            else:
                
                vector_features=vector_features+[0,0,0,0,0,0]
                vector_features=vector_features+self.compute_features_for_int(ds[col])
            
            
            ds_features.append(vector_features)
            i=i+1

        return ds_features

