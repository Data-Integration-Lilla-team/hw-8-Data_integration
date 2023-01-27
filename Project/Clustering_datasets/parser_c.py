#il costruttore riceve in input il path del ds da parsare e invoca il metodo adeguato

class Parser_custom():

    def __init__(self, path_dataset):
        self.path_dataset=path_dataset


# parser cosutm per datasets
    def parserMarketCap(self, columns):
        cols=list(columns)
        out=[]
        to_filter_col='Unnamed:'
        for c in cols:
            if to_filter_col not in c:
                c=c.lower()             #tutto in lower case
                c=c.replace('(','_')
                c=c.replace(')','')
                c=c.replace('-','_')
                c=c.replace(' ','_')
           
                out.append(c)
    
        return sorted(out)
    def default_parser(self,columns):
        cols=list(columns)
        out=[]
        to_filter_col='Unnamed:'
        for c in cols:
            if to_filter_col not in c:
                c=c.lower()             #tutto in lower case
                c=c.replace('(','_')
                c=c.replace(')','')
                c=c.replace(' ','_')
                c=c.replace('-','_')
           
                out.append(c)
    
        return sorted(out)

    def parse(self, columns):
        out=[]
        if 'companiesmarketcap' in self.path_dataset:
            
            return self.parserMarketCap(columns)
        
        else:
            return self.default_parser(columns)

    
    def parse_column_for_merge(self,columns):

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
            
