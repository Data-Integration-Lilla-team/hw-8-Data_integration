import pandas as pd
import re
def parse_values(value):
    old_val=str(value)
    edit=0
    if old_val!='0' or old_val!='' or old_val!='non e':
        if ',' in old_val:
            old_val=old_val.replace(',','')
        new_val= s=[float(s) for s in re.findall(r'-?\d+\.?\d*',old_val)]
        if len(new_val)>=1:
            new_val=new_val[0]
            if ' t' in value or ' trillion' in value :
                edit=1
                new_val=new_val*1000
            elif ' m' in value or ' million' in value:
                edit=1
                new_val=new_val/1000
            elif ' b' in value or ' billion' in value:
                edit=1
                new_val=new_val/10
            
            if edit==1 and 'https' not in old_val:
            
                new_val='doll_'+str(new_val)+' b'
               
                return new_val
            else:
                return old_val
        else:
            return '0'
    else:
        return old_val

        
def drop_not_needed_cols(data):
        print('Name columns bf:',data.columns)
        data.columns.str.startswith('Unnamed')
        
        data=data.loc[:,~data.columns.str.startswith('Unnamed')]
        print('Name columns af:',data.columns)
        return data
       

if __name__=='__main__':
    path='Project\\Schema matching\\SchemaMatchingValentine\\clusters\\schema\\disfold.csv'
    path_1='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\dati_monetari\\disfold.csv'
    dest='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\dati_monetari\\disfold_parsed.csv'
    dest_='Project\\Schema matching\\SchemaMatchingValentine\\clusters\\schema_parsed\\disfold.csv'
    data=pd.read_csv(path_1)
    colonne=data.columns.values
    print(colonne)
    #analizza colonne
    for c in colonne:
        if 'Unn' not in c:
            values=data[c].fillna('0')
            data[c]=data[c].apply(parse_values)
    data=drop_not_needed_cols(data)
    data.to_csv(dest)
    data_1=pd.read_csv(path)
    data_1=drop_not_needed_cols(data_1)
    data_2_parsed=pd.read_csv(dest)
    data_2_parsed=drop_not_needed_cols(data_2_parsed)
    print(data_1.head(10))
    colonne=data_2_parsed.columns.values
    data_1[colonne]=data_2_parsed[colonne]
    print(data_1.head(10))
    data_1.to_csv(dest_)
    
