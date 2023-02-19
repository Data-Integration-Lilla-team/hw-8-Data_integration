import pandas as pd
import textwrap

class Separator:

    #blocks = numero di blocchi in cui dividere il dataset (più o meno --> la divisione è intera)
    def __init__(self):
        self.alfabeto = 'abcdefghijklmnopqrstuvwxyz'
        self.blocchi = textwrap.wrap(self.alfabeto, 1)
    
    #input = dataframe
    #output = csv degli elementi del dataframe separati in base all'iniziale del nome dell'azienda
    def separate(self, df):
        for blocco in self.blocchi:
            df_final = pd.DataFrame
            lista_df = []
            for letter in blocco:
                lista_df.append(df[df['name'].str.startswith(letter, na=False)])
            df_final = pd.concat(lista_df, ignore_index = True)
            df_final.to_csv(r'C:\hw-8-Data_integration\Project\Record linkage\DATASETS\Dataset separati per lettera\\' + blocco + '.csv', index = False)
