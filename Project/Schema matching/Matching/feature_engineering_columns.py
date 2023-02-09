import re
from string import punctuation
from collections import Counter
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
class FeatureExtraction:
    def __init__(self):
        self.features=['column_name',
        'type_of_data',
        'type_of_string',
        'avg_length_of_field',
        'var_length',
        'std_dev_length',
        'ratio_white_space_length',
        'ratio_num_val',
        'is_country',
        'min_val(int)',
        'max_val(int)',
        'avg(int)',
        'variance',
        'std_dev',
        'incremetal_int']
    

        # da adornare con data
    def compute_features(self, col):

        integer=1
        string_t=0
        data_t=2
        months=['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december',
          'January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
        numbers={'0','1','2','3','4','5','6','7','8','9'}
        conta_string=0
        conta_int=0
        regex_date="^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"
        regex_date2='\d{2}.\d{2}.\d{2}'
        import string
        s = set(string.ascii_lowercase)
        
        for i in col.head(30):
            
            
            string_version=str(i).lower()
            set_chars=set(string_version)
            inter=s.intersection(set_chars)
            if 'https' in string_version or 'http' in string_version:
                print('URL')
                return string_t
            if '(' in string_version or ')' in string_version:
                conta_string+=1
            
            if 'doll' in string_version or 'rank' in string_version or 'perc' in string_version or 'b' in string_version or 't' in string_version or 'm' in string_version or ' ' in string_version:
                print('stringa')
                return string_t
            if len(inter)>=0.6*len(set_chars):
                print('stringa')
                return string_t
            elif len(inter)<0.6*len(set_chars):
                
                data=str(string_version).split(' ')
                if len(data)>1:
                    if data[1] in set(months):
                        print('data')
                        return data_t
                elif re.match(regex_date,string_version) or re.match(regex_date2,string_version):
                        print('data')
                        return data_t
                
            else:
                    print('è un intero')
                    float_set_chars={str(float(x)) for x in set_chars}
                    print(float_set_chars)
                    float_int_chars={str(float(x)) for x in numbers}
                    int=float_set_chars.intersection(float_int_chars)
                    if len(int)==len(float_set_chars) and 'doll' not in string_version and '0' not in string_version:
                        print('intero')
                        conta_int+=1
                    else:
                        conta_string+=1

        print('conta stringa', conta_string)
        print('conta interi',conta_int)
        if conta_string>conta_int:
            return string_t
        else:
            return integer
        
    
    def compute_incremental(self,col):
        print('incremental')
        somma=0
        min=0
        max=40
        opp=-1
        while (min<max/2):
            a=col.iloc[min]
            b=col.iloc[max]
            d=a+b
            somma=somma+(opp)*d
            min+=1
            max-=1
            opp=opp*-1
        if somma==0:
            return 1
        else:
            return 2

    def parse_data(self,col):
        elements=[]
        numbers={'0','1','2','3','4','5','6','7','8','9'}
        
        import string
        float_int_chars={str(float(x)) for x in numbers}
        s = set(string.ascii_lowercase)
        
        for i in col:
            string_val=str(i).lower()
            value=string_val.replace(',','').replace('.','')
            set_chars=set(value)
            inter=s.intersection(set_chars)
            
            if len(inter)>0:
                
                elements.append(0)
            else:   
                elements.append(value)
        out=pd.Series(data=elements)
        
        return out
    def compute_features_for_int(self, col):
            integer_features=[]
            print(type(col))
            print(col.head(10))
            
            col = col.apply(pd.to_numeric, errors='coerce')
            col = col.fillna(0)
            col=col.astype(float)
            
            integer_features.append(col.min(skipna=True))
            integer_features.append(col.max(skipna=True))
            integer_features.append(col.mean(skipna=True))
            integer_features.append(col.var())
            integer_features.append(col.std())
            integer_features.append(self.compute_incremental(col))
            return integer_features
        
    def compute_type(self, val):
        numero_perc=0
        numero_rank=0
        numero_doll_normal=0
        numero_doll=0
        numero_resto=0
        for i in val:
            if '_perc' in val:
                numero_perc+=1
            
            if 'rank_' in val:
                numero_rank+=1

            if 'doll_' in val:
                if 'm' in val or 't' in val or 'b' in val:
                    numero_doll_normal+=1
                else:
                    numero_doll+=1
            
            else:
                numero_resto+=1
        
        if numero_doll>=3:
            return 3
        elif numero_perc>=5:
            return 1
        elif numero_rank>=5:
            return 2
        elif numero_doll_normal:
            return 4
        else:
            return 5


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


    
        
    def is_country(self,col):
        countries = {'china','usa', 'india', 'united states', 'indonesia', 'pakistan', 'brazil', 'nigeria', 'bangladesh', 'russia', 'mexico','honk-kong','italy','united kingdom','united-kingdom','uk'}
        tot=20
        somma=0
        data=col.head(41)
        for c in data:
            if c in countries:
                somma+=1
        if somma>=0.4*tot:
            print('country')
            return 1
        else:
            return 0                
           

    def compute_features_for_string(self, col):
        feature_vector=[]

        #type of string
        feature_vector.append(self.compute_type(col.head(30)))

        #avg len of strings
        feature_vector.append(col.str.len().mean())

        #var len of strings
        feature_vector.append(col.str.len().var())

        #std deviation of strings lenght
        feature_vector.append(col.str.len().std())

        #ratio of whitespaces
        feature_vector.append(self.compute_ratio_of_whitespace(col))

        #ratio of numeric values
        result=self.compute_ratio_of_numeric_values(col)

        feature_vector.append(self.is_country(col))

        
        feature_vector.append(result)
        

        return feature_vector

    

    
   







         
        




    #features-> 
    #nome campo
    #1. tipo di dato: string 0, int 1, data 3
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


    #creazione del dataset
    def create_pandas_dataframe(self,data):
        list_of_data=[]
        
        for k in data.keys():
            for e in data[k]:
                list_of_data.append(e)
        

        dataset=pd.DataFrame(data=list_of_data,columns=self.features)
        return dataset

    #estrattore di features
    def extract_feature(self,ds,k):
        ds=ds.fillna(0)
        ds_features=[]                  
        list_of_names_columns=ds.columns.values.tolist()
        i=0
        for col in ds.columns:
            if i>0:
                name_column=k+'-'+list_of_names_columns[i]
                print('colonna:',name_column)
                vector_features=[name_column]
                
                
                type_of_col=self.compute_features(ds[col])
                print(type_of_col)
                vector_features.append(type_of_col)
                if type_of_col==0:  #calcola le feature per la stringa, i valori numerici verranno settati a 0
                    
                    vector_features=vector_features+self.compute_features_for_string(ds[col])
                    vector_features=vector_features+[0,0,0,0,0,0]
                elif type_of_col==1:
                    
                    
                    vector_features=vector_features+[0,0,0,0,0,0]
                    vector_features=vector_features+self.compute_features_for_int(ds[col])
                
                else:
                    vector_features=vector_features+[0,0,0,0,0,0,0,0,0,0,0,0,0]
                
                
                ds_features.append(vector_features)
                i=i+1
            else:
                i+=1

        return ds_features

