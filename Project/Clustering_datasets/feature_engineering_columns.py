
class FeatureExtraction:
    def __init__(self):
        pass
    

        # da adornare con data
    def compute_features(self, col):
        integer=1
        string_t=0
        if isinstance(col.head(1)[0], str):
            return string_t
        else:
            return integer

    #features-> 
    #1. tipo di dato: string 0, int 1, data (?)
    #2. (string)type of str->perc_:1, b or t or doll_: 2, rank_=3,  other=4
    #2. (string)avg_lenght of fiald (if string)
    #3. (string)variance of lenght
    #4. (string)ratio of whitespace fields
    #5. (string)ratio of special char
    #6. (string)ratio of numeric values
    #7. (int)min val
    #8. (int)max val
    #9. (int)avg
    #10 (int)variance

    def extract_feature(self,ds):
        ds_features=[]                  #lista di tuple (nome campo, vettore)
        for col in ds.columns:
            vector_features=[]
            type_of_col=self.compute_features(ds[col])
            vector_features.append(type_of_col)
            if type_of_col==0:  #calcola le feature per la stringa, i valori numerici verranno settati a 0
                vector_features.append(self.compute_features_for_string(ds[col]))
            else:
                vector_features.append(self.compute_features_for_string(ds[col]))

