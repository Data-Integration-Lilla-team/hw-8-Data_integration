import json
import os
     
def create_computato(computato):
    final_dic_sin=dict()
    for k in computato.keys():
        if '-' in k:
            name=k.split('-')[0]
        else:
            name=k
        if name not in final_dic_sin:
            final_dic_sin[k]=set()
        
        elements=computato[k]
        for e in elements:
            values=e.split('-')
            value=values[len(values)-1]
            final_dic_sin[name].add(value)
   
    return final_dic_sin
def create_token_list(dizionario_sinonimi_pregressi):
    from token_obj import Token_obj
    list_of_tokens=[]
    for k in dizionario_sinonimi_pregressi.keys():
        full_name=k
        
        sinonimi_pregressi=set(dizionario_sinonimi_pregressi[k])
        token=Token_obj(full_name,sinonimi_pregressi=sinonimi_pregressi)
        
        list_of_tokens.append(token) 
    return list_of_tokens
if __name__=='__main__':
        computato=r'Project\Schema matching\MySchemaMatching\final_schema\dictionary\finalschema.txt'
        dest_dizionario_sinonimi_pregressi=r'Project\Schema matching\MySchemaMatching\files_matching\files_vari\dizionario_sinonimi_pregressi.txt'
        validatio_set=r'Project\Schema matching\MySchemaMatching\files_matching\validation_set\column_sinonimi.txt'


        

        with open(dest_dizionario_sinonimi_pregressi,'r') as f:
            data=f.read()
        
        prgressi=json.loads(data)
        print('pregressi')
        print(prgressi)

        with open(validatio_set,'r') as f:
            data=f.read()
        
        validatio_set=json.loads(data)
        print(validatio_set)

        with open(computato,'r') as f:
            data=f.read()
        
        computato=json.loads(data)
        print('computato',computato)
        new_comp=create_computato(computato)
        print('new comp',new_comp)
        tokens=create_token_list(computato)
        diz_sinonimi_final=dict()
        i=0
        #crea i potenziali nuovi sinonimi
        for i in range(len(tokens)):
            current_element=tokens[i]
            j=0
            for j in range (len(tokens)):
                if j!=i:
                    to_confront=tokens[j]
                    
                    score=current_element.confront_columns(to_confront)
                    
                    
                    if score>=0.2 and current_element.name!=to_confront.name:
                        print(current_element.name,to_confront.name)
                        
                        print(score)
                        current_element.update_sin_attuali(to_confront.name)
                        
        #crea i sinonimi
        seen=set()
        for t in tokens:
            true_name=t.name
            if true_name not in seen:
                seen.add(true_name)
                if true_name in validatio_set:
                    if true_name not in diz_sinonimi_final:
                        diz_sinonimi_final[true_name]=t.sin_attuali
                    if true_name in diz_sinonimi_final:
                        diz_sinonimi_final[true_name].update(t.sin_attuali)
                    print(true_name)
                    print('computato',diz_sinonimi_final[true_name])
                    print('vero',validatio_set[true_name])
                    print('intersezione:',diz_sinonimi_final[true_name].intersection(set(validatio_set[true_name])))
                    
                    print('extra:',diz_sinonimi_final[true_name].difference(set(validatio_set[true_name])))
                    
                    print('mancanti:',set(validatio_set[true_name]).difference(set(diz_sinonimi_final[true_name])))

        final_SMM=r'Project\Testing\Matching\performace\diz_fin.txt'
        diz_f=dict()
        for k in diz_sinonimi_final.keys():
            diz_f[k]=list(diz_sinonimi_final[k])
        with open(final_SMM,'w') as f:
            f.write(json.dumps(diz_f,indent=4))




