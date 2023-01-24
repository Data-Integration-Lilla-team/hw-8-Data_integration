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
            print('USING PARSER FOR',self.path_dataset)
            return self.parserMarketCap(columns)
        
        else:
            return self.default_parser(columns)
