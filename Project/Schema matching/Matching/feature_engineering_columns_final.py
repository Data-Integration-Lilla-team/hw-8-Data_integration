import re
from string import punctuation
from collections import Counter
import pandas as pd
import numpy as np
import random
import math
from sklearn.preprocessing import MinMaxScaler
class FeatureExtraction:
    def __init__(self):
        self.features=['column_name',
        'type_of_data',

        'type_of_string',
        'avg_mon_values (0 if not monetary)',
        'avg_length_of_field',
        'var_length',
        'std_dev_length',
        'ratio_white_space_length',
        'ratio_num_val',
        'is_country',
        'is_sector',

        'min_val(int)',
        'max_val(int)',
        'avg(int)',
        'variance',
        'std_dev',
        'incremetal_int',
        'is_year']
    
    def create_sample_set(self,col,max):
        conta_valori=0
        max_val=len(col)
        values=[]
        while conta_valori<=max:
            index=random.uniform(0,max_val)
            index=int(index)            
            i=col.loc[index]
            while i==0 or i=='non e' or i=='not found' or i=='none' or i=='0' or i=='':
                index=random.uniform(0,max_val)
                index=int(index)            
                i=col.loc[index]
            values.append(i) 
            conta_valori+=1
            
        return values


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
        print('Dati analizzati')
        values=self.create_sample_set(col,30)
        
       
        
        for i in values:   
            
            string_version=str(i).lower()
            set_chars=set(string_version)
            inter=s.intersection(set_chars)
            if 'https' in string_version or 'http' in string_version:
                print('URL')
                return string_t
            if '(' in string_version or ')' in string_version:
                conta_string+=1
            
            if 'doll' in string_version or 'rank' in string_version or 'perc' in string_version or 'b' in string_version or 't' in string_version or 'm' in string_version or ' ' in string_version:
                print('stringa eeee')
                
                return string_t
            if len(inter)>=0.6*len(set_chars):
                print('stringa')
                return string_t
            elif len(inter)<0.6*len(set_chars):
                
                data=str(string_version).split(' ')
                data2=str(string_version).replace('.','/')
                if len(data)>1:
                    if data[1] in set(months):
                        print('data ci sono i mesi')
                        return data_t
                elif re.match(regex_date,string_version) or re.match(regex_date,data2):
                        print('data')
                        return data_t
                
            else:
                    print('è un intero')
                    float_set_chars={str(float(x)) for x in set_chars}
                    print(float_set_chars)
                    float_int_chars={str(float(x)) for x in numbers}
                    inte=float_set_chars.intersection(float_int_chars)
                    if len(inte)==len(float_set_chars) and 'doll' not in string_version and '0' not in string_version:
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
        
    def is_year(self, col):
        min_range=1850
        max_range=2024
        giusti=0
        for i in col:
            if i>=min_range and i<=max_range:
                giusti+=1
            
        if giusti>=0.9*(len(col)):
            return 1
        else:
            return 0
    def compute_incremental(self,col):
        col=sorted(col)
        print('incremental')
        somma=0
        min=0
        max=40
        opp=-1
        while (min<max/2):
            a=col[min]
            b=col[max]
            d=a+b
            somma=somma+(opp)*d
            min+=1
            max-=1
            opp=opp*-1
        if somma<10:
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

    def get_avg(self,values):
        summ=sum(values)
        length=len(values)
        return summ/length

    def get_var(self,values):
        n = len(values)
        mean = sum(values) / n
        return sum((x - mean) ** 2 for x in values) / n

        
    def create_sample_set_for_int(self,col, max):
        import string
        conta_valori=0
        max_val=len(col)
        values=[]
        s = set(string.ascii_lowercase)
        s.add('[')
        s.add(']')
        s.add('(')
        s.add('?')
        s.add('!')
        s.add('')
        while conta_valori<=max:
            index=random.uniform(0,max_val)
            index=int(index)            
            i=col.loc[index]
            string_version=str(i).lower()
            set_chars=set(string_version)
            inter=s.intersection(set_chars)
           
            while i==0 or i=='non e' or i=='not found' or i=='none' or i=='0' or i=='' or len(inter)>0:
                
                index=random.uniform(0,max_val)
                index=int(index)            
                i=col.loc[index]
                string_version=str(i).lower()
                set_chars=set(string_version)
                inter=s.intersection(set_chars)
            if isinstance(i,str):
                i=i.replace('.','').replace(',','').replace('-','')
                try:
                    i = float(i)
        
                except ValueError:
                    i=0
                
            values.append(i) 
            conta_valori+=1
            
        return values

    def compute_features_for_int(self, col):
            integer_features=[]
            values=self.create_sample_set_for_int(col,300)
            values = list(map(float, values))
            
            
            
            integer_features.append(min(values))
            integer_features.append(max(values))
            integer_features.append(self.get_avg(values))
            integer_features.append(self.get_var(values))
            integer_features.append(math.sqrt(self.get_var(values)))
            integer_features.append(self.compute_incremental(values))
            integer_features.append(self.is_year(values))
            return integer_features


    def compute_out(self, values):
        #se resto è il massimo e tutti 0 allora out è 6
        # se resto è massimo e esiste altro diverso da 0 allora il secondo è out
        # else:
        # key associata al massimo valore
        sorted_d = sorted(values.items(), key=lambda x: x[1],reverse=True)
        massimo_key=sorted_d[0][0]
        valore_max=sorted_d[0][1]
        if massimo_key==6:
            secondo_key=sorted_d[1][0]
            valore_sec=sorted_d[1][1]
            if valore_sec>0:
                return secondo_key
            else:
                return massimo_key
        else:
            return massimo_key
                
                
            
    def compute_type(self, values):
        
        dic_out={1:0,2:0,3:0,4:0,5:0,6:0}
        for val in values:
            val=str(val)
            if '_perc' in val: #1
                
                dic_out[1]+=1
            
            if 'rank_' in val: #2
                
                dic_out[2]+=1
            if 'https' in val or 'http' in val: #3
                dic_out[3]+=1

            if 'doll_' in val:
                if 'm' in val or 't' in val or 'b' in val: #4
                    
                    dic_out[4]+=1
                else:   #5
                    
                    dic_out[5]+=1
            
            else: #6
                dic_out[6]+=1
        out=self.compute_out(dic_out)
        print('tipo:',out)
        return out
       


    def compute_ratio_of_whitespace(self,col):
        mean_ratio=0
        for i in col:
            tot_w_space=i.count(' ')
            s_len=len(i)
            mean_ratio=mean_ratio+(tot_w_space/s_len)

        mean_ratio=mean_ratio/len(col)
        print('Ratio:', mean_ratio)
        return mean_ratio

    def compute_ratio_of_numeric_values(self, col):
        ratio=0
        total=len(col)
        for val in col:
            string_len=len(str(val))
            temp=str(val)
            numeric_val=len(re.sub("[^0-9]", "", temp))
            ratio=ratio+(numeric_val/string_len)
        print('ratio nums:',ratio/total)
        return ratio/total

    def is_sector(self, data):
        business_sectors = {
            "it services & consulting"
    "agriculture",
    "air transportation",
    "alcoholic beverages",
    "apparel",
    "automotive",
    "banking",
    "beauty and personal care",
    "biotechnology",
    "chemicals",
    "communications",
    "construction",
    "consumer goods",
    "consumer services",
    "cosmetics",
    "defense",
    "design and applied arts",
    "education",
    "electronics",
    "oil&gas",
    'technology',
     'internet or mobile app based business',
      'software and it', 
      'software products',
       'cloud services',
        'artificial intelligence',
         'internet of things',
          'gaming',
    "entertainment",
    "cosmetics and beauty",
    "energy",
    "entertainment",
    "fashion",
    "financial services",
    "fine art",
    "food and beverage",
    "government",
    "health care",
    "home furnishings",
    "hospitality",
    "information technology",
    'tech', 'electronics', 'networking hardware', 'dow jones', 'telecommunications equipment', 'tech hardware',
    'consumer defensive', 'fmcg', 'food products', 'beverages', 'dairy products', 'non-alcoholic beverages', 'chocolate & confectionery', 'coffee', 'consumer non durables', 'food and beverage', 'package foods',
    "insurance",
    'alcoholic beverages', 'beverages',
    'stock exchanges', 'financial services', 'dax', 'stock/crypto exchanges',
    "internet",
    "leisure goods",
    "life sciences",
    "media",
    "mining",
    "music",
    "natural resources",
    "pharmaceuticals",
    "professional services",
    "public administration",
    "public utilities",
    "real estate",
    "recreational services",
    "retail",
    "software",
    "sports",
    "technology",
    'automakers', 'manufacturing',
    'stock exchanges', 'financial services', 'stock/crypto exchanges',
    "telecommunications",
    "textiles",
    "tobacco",
    "tourism",
    "transportation",
    "video games",
    "waste management",
    "water utilities",
    "wholesale trade",
    "e-commerce & direct-to-consumer",
    "artificial intelligence",
    "fintech",
    "supply chain, logistics, & delivery",
    "internet software & services"
    }
        matches=0
        for i in data:
            i=i.replace('[','').replace(']','')
            i=i.replace('"','').replace("'","")
            
            if ',' in data:
                values=i.split(',')
                for k in values:
                    if k in business_sectors:
                        
                        matches+=1
                        
            else:
                if i in business_sectors:
                    
                    
                    matches+=1
                   
        if matches>=0.08*len(data):
           
            return 1
        else:
            return 0



    
        
    def is_country(self,data):
        countries = {'china','usa', 'india', 'united states', 'indonesia', 'pakistan', 'brazil', 'nigeria', 'bangladesh', 'russia', 'mexico','honk-kong','italy','united kingdom','united-kingdom','uk'}
        tot=20
        somma=0
        
        for c in data:
            if c in countries:
                somma+=1
        if somma>=0.4*tot:
            print('country')
            return 1
        else:
            return 0                
           
    def compute_len_values(self,values):
        temp = [len(ele) for ele in values]
        res = 0 if len(temp) == 0 else (float(sum(temp)) / len(temp))
        print('AVG len:',res)
        return res

    def compute_variance_mon_values(self,values):
        import re
        somma=0
        n=len(values)
        for v in values:
            s=[float(s) for s in re.findall(r'-?\d+\.?\d*',v)][0]
            print('value_string:',v)
            somma=somma+s
        print('AVG:',somma/n)
        return somma/n
            

    def compute_variance(self,values):
        
        n = len(values)
        lengths = [len(s) for s in values]
        mean = sum(lengths) / n
        variance = sum((x - mean)**2 for x in lengths) / n
        print('var len:',variance)
        return variance


    def compute_features_for_string(self, col):
        feature_vector=[]
        values=self.create_sample_set(col,1000)
        values=list(map(str,values))

        #type of string
        type_string=self.compute_type(values)
        feature_vector.append(type_string)

        if type_string==5 or type_string==4:
            feature_vector.append(self.compute_variance_mon_values(values))
        else:
            feature_vector.append(0)




        #avg len of strings
        feature_vector.append(self.compute_len_values(values))

        #var len of strings
        feature_vector.append(self.compute_variance(values))

        #std deviation of strings lenght
        import math
        feature_vector.append(math.sqrt(self.compute_variance(values)))

        #ratio of whitespaces
        feature_vector.append(self.compute_ratio_of_whitespace(values))
        

        #ratio of numeric values
        feature_vector.append(self.compute_ratio_of_numeric_values(values))


        feature_vector.append(self.is_country(values))

        feature_vector.append(self.is_sector(values))

        
       
        

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
                print('=======NOME COLONNA========',name_column)
                print('colonna:',name_column)
                vector_features=[name_column]
                
                
                type_of_col=self.compute_features(ds[col])
                print('Tipo di colonna',type_of_col)
                
                
                vector_features.append(type_of_col)
                if type_of_col==0:  #calcola le feature per la stringa, i valori numerici verranno settati a 0
                    
                    vector_features=vector_features+self.compute_features_for_string(ds[col])
                    vector_features=vector_features+[0,0,0,0,0,0,0]
                elif type_of_col==1:
                    
                    
                    vector_features=vector_features+[0,0,0,0,0,0,0,0,0]
                    vector_features=vector_features+self.compute_features_for_int(ds[col])
                
                else:
                    vector_features=vector_features+[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                
                
                ds_features.append(vector_features)
                
                i=i+1
            else:
                i+=1

        return ds_features

    

