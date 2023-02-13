import pandas as pd
if __name__=='__main__':
    path='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\dati_monetari\\valuetoday.csv'
    data=pd.read_csv(path)
    colonne=data.columns.values
    print(colonne)
    #analizza colonne
    for c in colonne:
        if 'Unn'  not in c:
            values=data[c]
            
            print(c)
            totali=len(values)
            validi=values.count()
            nan=totali-validi
            #t
            count_t=(values.str.contains(' t')).sum()
            
            
            
            count_m=(values.str.contains(' m')).sum()
            count_b=(values.str.contains(' b')).sum()
            count_non_e=(values.str.contains('non e')).sum()
            count_zeros=(values.str.contains('0')).sum()
         

            print('Numero valori:',len(values))
            print('valori validi',values.count())
            print('nan:',nan)
            print('trillion',count_t)
            print('brillion',count_b)
            print('mrillion',count_m)
            print('non e',count_non_e)
            