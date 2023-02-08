'''
Momentanea
classe responsabile per il parsing dei dati

metodo principale->parse_source

riorganizzazione nomi delle colonne
riorganizzazinoe valori delle colonne
'''
import os
import pandas as pd
import re


def extract_important_part(valore):
    pattern='^[0-9]'
    out=''
    for i in range(0,len(valore)):
        if re.match(pattern,valore[i]):
            out=valore[i:]
            break
    print('interesting',out)        
    return out
            

def fomrat_amount_mix(e):
    valore=e
    if valore!=0:
        string_val=str(valore)
        if ',' in string_val:
            
            string_val=valore.replace(',','')
            full_value=(float(f'{float(string_val)/10**6:.2f}'))
            
        
            string_val='doll_'+str(full_value)+' m'
        else:
            string_val='doll_'+string_val+' m'
        return string_val
    return valore
        

def fomrat_amount_v2(e):
    valore=e
    if valore!=0:
        if valore=='not found':
            return 0
        if valore[0]!='doll_':
            string_val=extract_important_part(valore)
            string_val='doll_'+string_val
            print(string_val)

        if 'billion' in string_val :
                    
                    
                    string_val=string_val.replace('billion',' b')
                    
                    
        if 'trillion' in string_val:
                    print('Before',string_val)
                    string_val=string_val.replace('trillion',' t')
                    print('after:',string_val)
                    
        if 'million' in string_val:
                   
                    string_val=string_val.replace('million',' m')
        
        print('final',string_val)
        return string_val
    return valore
        
def fomrat_amount_v3(e):
    valore=e
    if valore!=0:
        if ',' in valore:
            print('before',valore)
            string_val=valore.replace(',','')
            full_value=(float(f'{int(string_val)/10**6:.2f}'))
            print('after',string_val, 'int', full_value)
            string_val='doll_'+str(full_value)+' m'
            return string_val
        return valore
            

    return valore
def delete_extra_data(e):
    valore=e
    if valore!=0:
        string_val=str(valore)
        if '(' in string_val and ')' in string_val:
            string_val=0
        
        return string_val
    return valore
def fomrat_amount_v4(e):
    valore=e
    if valore!=0:
        if ',' in valore:
            print('before',valore)
            string_val=valore.split(' ')
            
            val=string_val[0].replace(',','.')
            
            val='doll_'+val+' m'
            print('Valore',val)
            return val
        return valore

def fomrat_amount_v6(e):
    valore=str(e)
    if valore!=0:
        print('before',valore)
        if ',' in valore:   #billion
            print('trillion')
            real_val=valore.split(' ')[0]
            real_val=real_val.replace(',','').replace('.','')
            
            print('intero',real_val)
            int_val=int(real_val)/10**6
            real_val='doll_'+str(int_val)+' t'
        elif '.' in valore and ',' not in valore: #billion
            print('billion')
            real_val=valore.split(' ')[0]
            real_val=real_val.replace(',','').replace('.','')
            print('intero',real_val)
            int_val=int(real_val)
            if int_val>=100000:

                int_val=float(f'{float(real_val)/10**5:.2f}')
                real_val='doll_'+str(int_val)+' b'
            else:
                int_val=float(f'{float(real_val)/10**3:.2f}')
                real_val='doll_'+str(int_val)+' m'

        

        else:
            real_val=0
        
        print('after',real_val)
        return real_val
    return valore
            






def convert_unit(e):
    valore=e
    if valore!=0:
        
        string_val=str(valore)
        if 'doll_' not in string_val and string_val !='doll_0':
            string_val='doll_'+string_val
        if string_val=='doll_0':
            string_val='0'

        if 'usdoll_' in string_val :
            string_val=string_val.replace('us','')


        string_val=string_val.lower()
        
        
        if 'billion' in string_val :
                    
                    
                    string_val=string_val.replace('billion',' b')
                    
                    
        if 'trillion' in string_val:
                    print('Before',string_val)
                    string_val=string_val.replace('trillion',' t')
                    print('after:',string_val)
                    
        if 'million' in string_val:
                   
                    string_val=string_val.replace('million',' m')
        
        return string_val
    
        
    return valore


#inserimento del b in fondo al valore passato
#se supera 1000 inserisco trillion
def append_b_to_money_val(e):
    
    valore=e
    if valore!=0:
        valore=str(e)
        real=valore+' b'
        print('before',valore, 'after',real)
        
        return real
    return valore
#inserimento del doll_
def insert_dollar(e):
    valore=e
    if valore!=0:
        valore='doll_'+str(valore)
        return valore
    return valore
        



def format_uni_money_val(e):
    string_val=e
    if e!=0 and ('billion' in str(e) or 'trillion' in str(e) or 'million' in str(e)):
                if 'usdoll_' in str(e):
                    string_val=str(e).replace('usdoll_','')
                    string_val='doll_'+string_val
                elif 'usd' in str(e):
                    string_val=str(e).replace('usd','')
                    string_val='doll_'+string_val


                elif 'doll_' not in str(e):
                        string_val='doll_'+str(e)
                else:
                    string_val=str(e)
                
                if 'billion' in string_val:
                    string_val=string_val.replace('billion','b')
                elif 'trillion' in string_val:
                    string_val=string_val.replace('trillion','t')
                elif 'million' in string_val:
                    string_val=string_val.replace('million','m')

                
                print('before:',e,'after:',string_val)
    return string_val

def format_amount_emp(element):
    divisore=1000
    format_int=int(element)/divisore
    return format_int

def convert_money(element):
    element=str(element)
    if 'kč' in element or  '€' in element or '€' in element or '¥' in element or '£' in element or '฿' in element:
        print('VALUTA STRANIERA') 
        print (element )                      

#parsing di amitobox 06
def parse_data_foundation_year_06 (elemento):
    valore=elemento
    
    if valore!=0:
        valore=str(valore)
        real=valore.split(' ')[0]
        
        pattern='^[0-9]{4}$'

        if not re.match(pattern,real):
            real=0
        
        return real
    return valore
#formattazione amount dollari
def fomrat_amount_error(element):
    valore=element
    if valore!=0:
        string_val=valore[:len(valore)-1]+' '+valore[len(valore)-1]
        return string_val.lower()
    return valore
def fomrat_amount(element):
    valore=element
    if valore!=0:
            prefix_03_gram='doll_'
            trillion='t'
            billion='b'
            million='m'
            trillino_limit=10**12
            billio_limit=10**9
            million_limit=10**6
            if element!=0:
                int_elem=int(element)
                
                #check trillion
                if int_elem>=trillino_limit:
                    
                    int_elem=(float(f'{int_elem/trillino_limit:.2f}'))
                    string_elem=prefix_03_gram+str(int_elem)+' '+trillion
                    
                elif int_elem<trillino_limit and int_elem>=billio_limit:
                    int_elem=(float(f'{int_elem/billio_limit:.2f}'))
                    string_elem=prefix_03_gram+str(int_elem)+' '+billion
                    
                
                else:
                    int_elem=(float(f'{int_elem/million_limit:.2f}'))
                    string_elem=prefix_03_gram+str(int_elem)+' '+million
                    
                return string_elem
            return element
    return valore
class Parser_data:


    def __init__(self):
        pass

    
    

    def parse_market_cap_USD_03_gram(self):
        market_cap_03_gram='Project\\Dataset\\ClusterParsed\\disfold\\03-gren.csv'
        market_cap_03_gram_companies_mk='Project\\Dataset\\ClusterParsed\\companiesmarketcap\\03-gren.csv'
        column_name_03_gram='market_capitalization_usd'
        column_name_03_price='price'
        
        
        '''ds=pd.read_csv(market_cap_03_gram)
        ds[column_name_03_gram]=ds[column_name_03_gram].fillna(0)
        ds[column_name_03_gram]=ds[column_name_03_gram].apply(fomrat_amount)
        ds=self.drop_not_needed_cols(ds)
        ds.to_csv(market_cap_03_gram)'''

        '''ds=pd.read_csv(market_cap_03_gram_companies_mk)
        ds[column_name_03_gram]=ds[column_name_03_gram].fillna(0)
        ds[column_name_03_gram]=ds[column_name_03_gram].apply(fomrat_amount)
        ds=self.drop_not_needed_cols(ds)
        ds.to_csv(market_cap_03_gram_companies_mk)'''

        ds=pd.read_csv(market_cap_03_gram_companies_mk)
        
        ds[column_name_03_price]=ds[column_name_03_price].fillna(0)
        ds[column_name_03_price]=ds[column_name_03_price].apply(insert_dollar)
        ds=self.drop_not_needed_cols(ds)
        ds.to_csv(market_cap_03_gram_companies_mk)


        

    #standardizzaizione del campo employees
    def parse_employees_number_03_gram(self):
        to_parse='Project\\Dataset\\ClusterParsed\\valuetoday\\03-gren.csv'
        col_employees='employees_number'
        col_market_cap='market_capitalization_2022'
        
        ds=pd.read_csv(to_parse)
        ds=self.drop_not_needed_cols(ds)

        #employees
        ds[col_employees]=ds[col_employees].fillna(0)
        ds[col_employees]=ds[col_employees].apply(format_amount_emp)

        #market cap
        ds[col_market_cap]=ds[col_market_cap].fillna(0)
        ds[col_market_cap]=ds[col_market_cap].apply(fomrat_amount)
        print(ds[col_market_cap].head(10))
        ds.to_csv(to_parse)
        
                
    def unify_money_format(self):
        path='Project\\Dataset\\ClusterParsed\\valuetoday\\07-silvestri.csv'
        col='market_value_jan_2020'
        ds=pd.read_csv(path)
        data=data.fillna(0)
        data=data.apply(format_uni_money_val)
       
        
        for e in data:
            if e!=0:
                string_val='doll_'+str(e)
                
                if 'billion' in string_val:
                    string_val=string_val.replace('billion','b')
                elif 'trillion' in string_val:
                    string_val=string_val.replace('trillion','t')
                elif 'million' in string_val:
                    string_val=string_val.replace('million','m')

                string_val=string_val.replace('usd','')
                print('before:',e,'after:',string_val)
        

    
    #estrazione del foundation year
    def parse_amitobox_founded(self):
        path='Project\\Dataset\\ClusterParsed\\ambitiobox\\06-MarScoToc.csv'
        column='foundation_year'
        data=pd.read_csv(path)
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(parse_data_foundation_year_06)
        data=self.drop_not_needed_cols(data)
        data.to_csv(path)


    #parsing dei valori in valutation di 04 cbinsights
    def parse_cbinisghts_04(self):
        path='Project\\Dataset\\ClusterParsed\\cbinsights\\04-iGMM.csv'
        column='valuation'
        data=pd.read_csv(path)
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(append_b_to_money_val)
        data=self.drop_not_needed_cols(data)
        data.to_csv(path)

    def extract_disfold_00(self):
        path='Project\\Dataset\\ClusterParsed\\disfold\\00-avengers.csv'
        column_1='founded'
        column_2='market_cap'
        column_3='gbp'

        data=pd.read_csv(path)
        #data[column_1]=data[column_1].fillna(0)
        #data[column_1]=data[column_1].apply(parse_data_foundation_year_06)
        #print(data[column_1].head(10))

        data[column_2]=data[column_2].fillna(0)
        data[column_2]=data[column_2].apply(convert_unit)
        

        data[column_3]=data[column_3].fillna(0)
        data[column_3]=data[column_3].apply(convert_unit)
       
        data=self.drop_not_needed_cols(data)

        
        
        data.to_csv(path)
    
    def extract_disfold_04(self):
        path='Project\\Dataset\\ClusterParsed\\disfold\\04-iGMM.csv'
        column_1='founded'
        column_2='marketcap'
        column_3='revenue'
        column_4='net_income'

        data=pd.read_csv(path)
        data[column_1]=data[column_1].fillna(0)
        data[column_1]=data[column_1].apply(parse_data_foundation_year_06)
        print(data[column_1].head(10))

        data[column_2]=data[column_2].fillna(0)
        data[column_2]=data[column_2].apply(convert_unit)
        

        data[column_3]=data[column_3].fillna(0)
        data[column_3]=data[column_3].apply(convert_unit)
        data[column_4]=data[column_4].fillna(0)
        data[column_4]=data[column_4].apply(convert_unit)
       
        data=self.drop_not_needed_cols(data)

        
        
        data.to_csv(path)

    def extract_disfold_06(self):
        path='Project\\Dataset\\ClusterParsed\\disfold\\06-MarScoToc.csv'
        column='mastercap'
        data=pd.read_csv(path)
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(delete_extra_data)
        data=self.drop_not_needed_cols(data)
        data.to_csv(path)

    def extract_disfold_08(self):
        path='Project\\Dataset\\ClusterParsed\\disfold\\08-slytherin.csv'
        column='market_cap'
        data=pd.read_csv(path)
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(fomrat_amount_v2)
        data=self.drop_not_needed_cols(data)
        data.to_csv(path)

    def extract_data_ft_01(self):
        path='Project\\Dataset\\ClusterParsed\\ft\\01-DDD.csv'
        column='revenue_2020_euro'
        data=pd.read_csv(path)
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(fomrat_amount_v3)
        data=self.drop_not_needed_cols(data)
        data.to_csv(path)

    def extract_data_ft_03(self):
        path='Project\\Dataset\\ClusterParsed\\ft\\03-gren.csv'
        column='revenue_2020_eu'
        data=pd.read_csv(path)
        print(data[column].head(20))
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(fomrat_amount)
        data=self.drop_not_needed_cols(data)
        print(data[column].head(20))
        data.to_csv(path)

    def extract_data_ft_07(self):
        path='Project\\Dataset\\ClusterParsed\\ft\\07-silvestri.csv'
        column='revenue_2020'
        data=pd.read_csv(path)
        print(data[column].head(20))
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(fomrat_amount_v3)
        data=self.drop_not_needed_cols(data)
        print(data[column].head(20))
        data.to_csv(path)

    def extract_data_ft_08(self):
        path='Project\\Dataset\\ClusterParsed\\ft\\08-slytherin.csv'
        column='revenue'
        data=pd.read_csv(path)
        print(data[column].head(20))
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(fomrat_amount_mix)
        data=self.drop_not_needed_cols(data)
        print(data[column].head(20))
        data.to_csv(path)

    def extract_data_valuetoday_00(self):
        path='Project\\Dataset\\ClusterParsed\\valuetoday\\00-avengers.csv'
        column_1='annual_revenue_in_usd'
        column_2='annual_net_income_in_usd'
        column_3='total_assets_in_usd'
        column_4='total_liabilities_in_usd'
        column_5='total_equity_in_usd'

        data=pd.read_csv(path)
        data[column_1]=data[column_1].fillna(0)
        data[column_1]=data[column_1].apply(fomrat_amount_v4)
        print(data[column_1].head(10))

        data[column_2]=data[column_2].fillna(0)
        data[column_2]=data[column_2].apply(fomrat_amount_v4)
        

        data[column_3]=data[column_3].fillna(0)
        data[column_3]=data[column_3].apply(fomrat_amount_v4)

        data[column_4]=data[column_4].fillna(0)
        data[column_4]=data[column_4].apply(fomrat_amount_v4)

        data[column_5]=data[column_5].fillna(0)
        data[column_5]=data[column_5].apply(fomrat_amount_v4)
        print(data[column_5].head(10))
       
        data=self.drop_not_needed_cols(data)

        
        
        data.to_csv(path)

    def extract_data_valuetoday_02(self):
        path='Project\\Dataset\\ClusterParsed\\valuetoday\\02-GioPonSpiz.csv'
        column='marketvalue'
        column_2='marketcap'
        data=pd.read_csv(path)
        #column
        print(data[column].head(20))
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(fomrat_amount_v6)

        print(data[column_2].head(20))
        data[column_2]=data[column_2].fillna(0)
        data[column_2]=data[column_2].apply(fomrat_amount_v6)


        data=self.drop_not_needed_cols(data)
        print(data[column].head(20))
        data.to_csv(path)

    def extract_data_valuetoday_03(self):
        path='Project\\Dataset\\ClusterParsed\\valuetoday\\03-gren.csv'
        col1='annual_revenue_usd'
        col2='annual_net_income_usd'
        col3='market_capitalization_2022'
        data=pd.read_csv(path)
        print(data[col1].head(20))
        
        data[col1]=data[col1].fillna(0)
        data[col1]=data[col1].apply(fomrat_amount)
        
        print(data[col1].head(20))

        data[col2]=data[col2].fillna(0)
        data[col2]=data[col2].apply(fomrat_amount)
        data=self.drop_not_needed_cols(data)
        print(data[col2].head(20))

        data[col3]=data[col3].fillna(0)
        data[col3]=data[col3].apply(fomrat_amount)
        data=self.drop_not_needed_cols(data)
        print(data[col3].head(20))
        
        data=self.drop_not_needed_cols(data)
        
        data.to_csv(path)
    def extract_data_valuetoday_04(self):
        path='Project\\Dataset\\ClusterParsed\\valuetoday\\04-iGMM.csv'
        column='market_value__jan_07_2022'
        column_2='market_value__jan_1st_2020'
        data=pd.read_csv(path)
        #column
        print(data[column].head(20))
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(fomrat_amount_v6)

        print(data[column_2].head(20))
        data[column_2]=data[column_2].fillna(0)
        data[column_2]=data[column_2].apply(fomrat_amount_v6)


        data=self.drop_not_needed_cols(data)
        print(data[column].head(20))
        data.to_csv(path)




    def extract_data_valuetoday_07(self):
        path='Project\\Dataset\\ClusterParsed\\valuetoday\\07-silvestri.csv'
        column_1='market_value_jan_2020'
        column_2='market_value_jan_2021'
        column_3='market_value_jan_2022'
        column_4='revenue_2022'
        

        data=pd.read_csv(path)
        data[column_1]=data[column_1].fillna(0)
        data[column_1]=data[column_1].apply(fomrat_amount_v6)
        print(data[column_1].head(10))

        data[column_2]=data[column_2].fillna(0)
        data[column_2]=data[column_2].apply(fomrat_amount_v6)
        

        data[column_3]=data[column_3].fillna(0)
        data[column_3]=data[column_3].apply(fomrat_amount_v6)

        

       
       
       
        data=self.drop_not_needed_cols(data)

        
        
        data.to_csv(path)



    def extract_data_valuetoday_08(self):
        path='Project\\Dataset\\ClusterParsed\\valuetoday\\08-slytherin.csv'
        column='revenue'
       
        data=pd.read_csv(path)
        #column
        print(data[column].head(20))
        data[column]=data[column].fillna(0)
        data[column]=data[column].apply(fomrat_amount_v4)

        


        data=self.drop_not_needed_cols(data)
        print(data[column].head(20))
        data.to_csv(path)

    

    def parse_error_data(self):
        mappa_da_fixare={
            'Project\\Dataset\\ClusterParsed\\forbes\\08-slytherin.csv':'revenue',
            
            'Project\\Dataset\\ClusterParsed\\cbinsights\\01-DDD.csv':'totalraised',
            'Project\\Dataset\\ClusterParsed\\ft\\01-DDD.csv':'revenue_2020_euro',
            'Project\\Dataset\\ClusterParsed\\ft\\07-silvestri.csv':'revenue_2020',
            
            'Project\\Dataset\\ClusterParsed\\globaldata\\10-DeBiGa.csv':'market_cap'

        }
        mappa_da_fixare2={
            'Project\\Dataset\\ClusterParsed\\cbinsights\\01-DDD.csv':'valuation',
            'Project\\Dataset\\ClusterParsed\\globaldata\\10-DeBiGa.csv':'revenue'
        }
        
        for k in mappa_da_fixare.keys():
            path=k
            field=mappa_da_fixare[k]
            data=pd.read_csv(path)
            data[field]=data[field].fillna(0)
            data[field]=data[field].apply(fomrat_amount_error)
            data=self.drop_not_needed_cols(data)
            print(k,field)
            print(data[field].head(1))
            data.to_csv(path)
            
        for k in mappa_da_fixare2.keys():
            path=k
            field=mappa_da_fixare2[k]
            data=pd.read_csv(path)
            data[field]=data[field].fillna(0)
            data[field]=data[field].apply(fomrat_amount_error)
            data=self.drop_not_needed_cols(data)
            print(k,field)
            print(data[field].head(1))
            data.to_csv(path)

    def parse_specific_values(self):
        
        #self.parse_employees_number_03_gram()

        #self.unify_money_format()

        #self.parse_amitobox_founded() #0fatto

        #self.parse_cbinisghts_04()     #fatto  

        #self.parse_market_cap_USD_03_gram()  #fatto

        #difold

        #self.extract_disfold_00()
       
        #self.extract_disfold_04()

        #self.extract_disfold_06()

        #self.extract_disfold_08()

        #ft
        #self.extract_data_ft_01()
        #self.extract_data_ft_03()
        #self.extract_data_ft_07()
        #self.extract_data_ft_08()

        #valuetoday
        #self.extract_data_valuetoday_00()
        #self.extract_data_valuetoday_02()
        #self.extract_data_valuetoday_03()
        #self.extract_data_valuetoday_04()
        #self.extract_data_valuetoday_08()
        #self.extract_data_valuetoday_07()

        self.parse_error_data()




        
        

        




    #metodo generico di trasformazione del nome delle colonne.
    # incaso di parser specifici, si invoca questo metodo che a sua volta, in base al nome del cluster passato, invoca un metodo specifico   
    def compute_new_column_name(self,columns):

        oldName2NewName=dict()
        cols=list(columns)
       
        to_filter_col='Unnamed:'
        for c in cols:
            if to_filter_col not in c:
                c_new=c.lower()             #tutto in lower case
                c_new=c_new.replace('(','_')
                c_new=c_new.replace(')','')
                c_new=c_new.replace(' ','_')
                c_new=c_new.replace('-','_')
            
                oldName2NewName[c]=c_new
           
        return oldName2NewName
    
    


    #eliminazione delle conolle Unnamed
    def drop_not_needed_cols(self,data):
        print('Name columns bf:',data.columns)
        data.columns.str.startswith('Unnamed')
        
        data=data.loc[:,~data.columns.str.startswith('Unnamed')]
        print('Name columns af:',data.columns)
        return data


    #specializzato nel parsing dei nomi delle colonne
    def parse_column_name(self, data, path_tgt):
        
        data_cols=data.columns
        oldCols2newCols=self.compute_new_column_name(data_cols)
        data.rename(columns=oldCols2newCols,inplace=True)

        data=self.drop_not_needed_cols(data)

        data.to_csv(path_tgt)

    
    #specializzato nel parsing e cleaning dei valori del ds
    def parse_values(self,data,path_tgt):
        
        dic_to_replace=dict()
        dic_to_replace={'%':'_perc',
                        '#':'rank_',
                        '\$': 'doll_',
                        
                        'usd': '',
                        '\r\n': ''
        } 
        columns=data.columns
        cols_to_lower_case=[]
        import re

       
        #ds=ds.fillna(0)
        for c in columns:
            
            data[c]=data[c].replace(dic_to_replace,regex=True)
            #verifico se è una lista
            print(c)
            print(data[c].head(2))
            trovato=''   
            if isinstance(data[c].head(1)[0], str):
                
                if '[' in data[c].head(1)[0]:
                    print(c,'============TROVATO====================')
                    print('before',data[c].head(1)[0])
                    trovato=c
                    data[c]=data[c].str.lower()
                    print(data[c].head(1)[0])
                data[c]=data[c].str.lower()
                
            sample=data[c].head(1)[0]
            #if 'billion' in str(sample) or 'trillion' in str(sample) or 'million' in str(sample):
                #data[c]=data[c].apply(convert_money)
                #data[c]=data[c].apply(format_uni_money_val)

                


        data=self.drop_not_needed_cols(data)
        data.to_csv(path_tgt)

    #riceve in input il path src del dataset da parsare
    #parsa il dataset e lo memorizza nel path path_tgt
    def parse_data(self,path_src, path_tgt):
        data=pd.read_csv(path_src)

        self.parse_column_name(data,path_tgt)
        data=pd.read_csv(path_tgt)
        self.parse_values(data,path_tgt)
        #nuovo dataset con colonne nuove
        
        
        
        


    #parsing delle colonne ed eliminazione di quelle inutili

    
 


        

        
            


    
    
    def parse_data_values(self,ds):
        dic_to_replace=dict()
        dic_to_replace={'%':'_perc',
                        
                        
                        '#':'rank_',
                        '\$': 'doll_'
        }
        columns=ds.columns
        cols_to_lower_case=[]
        import re

       
        #ds=ds.fillna(0)
        for c in columns:
            
            ds[c]=ds[c].replace(dic_to_replace,regex=True)
            if isinstance(ds[c].head(1)[0], str):
                ds[c]=ds[c].str.lower()


        return ds
            
