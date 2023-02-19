import pandas as pd
import numpy as np

def parseName(value):
    value=str(value)
    data=value.replace('ä','').replace('?','').replace('°','').replace('{n}.','')
    return data

def parseCountry(value):
    value=str(value)
    if value=='nan':
        value=np.NaN
    elif value=='usa' or value=='united states of america':
        value='united states'
    return value


import re
def parseFounded(value):
    
    
    pattern = r"\b\d{4}\b"
    year=0
    if value==np.NaN:
        return value

    if str(value)=='nan' or str(value)=='not found' or str(value)=='0' or str(value)==0 or str(value)=='none' or str(value)=='unknown':
        return np.NaN
    value=str(value)
    
    if  "\\" in value or  any(c.isalpha() for c in value):
        
        match = re.findall(pattern, value)
        
        if len(match)>=1:
            try:
                year = float(match[0])
                
                return year
    
            except ValueError:
                return np.NaN
   
            
        else:
            return np.NaN
    
    else:
        try:
                year = float(value)
                return year
    
        except ValueError:
                return np.NaN
        

def parseEmpl(value):
    if value==np.NaN:
        return np.NaN
    else:
            value=str(value)

            if '.' in value:
                
                count = value.lower().count('.'.lower())
                if count==1:
                    try:
                        number=float(value)*1000
                        return number
                        
                    except ValueError:
                        return value
                else:
                    
                    number=float(value.replace('.',''))
                    return number
            
            if ',' in value:
                
                value=value.replace(',','')
                
                try:
                        number=float(value)
                        return number
                        
                except ValueError:
                        return value

def parse_values(value):
    old_val=str(value)
    edit=0
    if old_val!='0' or old_val!='' or old_val!='non e':
        if ',' in old_val:
            old_val=old_val.replace(',','')
        new_val=[float(s) for s in re.findall(r'-?\d+\.?\d*',old_val)]
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
            return np.NaN
    else:
        return old_val

def parse_cate(value):
    value=str(value)
    if value=='none'or value=='not found' or value=='-' or value=='_' or value=='[]' or value=='nan' or value=='–':
        return np.NaN
    
    if '[' not in value:
        value="['"+value+"']"
        return value
    else:
        return value

def parse_city(value):
    if value=='?' or value=='-':
        return np.NaN
    return value
if __name__=='__main__':

    data=pd.read_csv('Project\\Schema matching\\SchemaMatching\\final_schema\\schema\\idea_final_schema.csv')
    data_final='Project\\Schema matching\\SchemaMatching\\final_schema\\schema\\idea_final_schema_parsed.csv'

    print(data.columns.to_list())

    print('prima del cleaning',len(data))
    # clean data
    data=data.dropna(subset=['name'])

    print('dopo',len(data))



    #parse name
    data['name']=data['name'].apply(parseName)


    #parse country
    data['country']=data['country'].apply(parseCountry)

    #parse founded
    data['founded']=data['founded'].apply(parseFounded)
    

    #parsing employees
    data['employees']=data['employees'].apply(parseEmpl)

    data['market_cap']=data['market_cap'].apply(parse_values)
    data['revenue']=data['revenue'].apply(parse_values)
    data['profit']=data['profit'].apply(parse_values)

    data['city']=data['city'].apply(parse_city)

    data['categories']=data['categories'].apply(parse_cate)
    data.to_csv(data_final)

    
    