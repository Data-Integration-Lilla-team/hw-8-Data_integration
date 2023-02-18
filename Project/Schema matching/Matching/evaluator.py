'''
Classe specializzata nella valutazione dei dizionari dei sinonimi mediante Jaccard

'''
import pandas as pd
class Eval:

    def __init__(self):
        pass
    
    def compute_jaccard( A,B):
        intersection=len(list(A.intersection(B)))
        union=(len(list(A))+len(list(B)))-intersection
        return float(intersection)/union


    def get_tot_col(self, dizionario):
        set_colonne=set()
        for k in dizionario.keys():
            set_colonne.update(set(dizionario[k]))

        return len(set_colonne)
    def compute_dis_f1(self,computato,target, tot_col):
        N=len(target.keys())
        precision=0
        recall=0
        f1=0
        jaccard=0
        results=[]
       
        numero_confronti_extra=0
        totale_colonne=self.get_tot_col(computato)
        for k in target.keys():
            name=k
            sing_precision=0
            sing_recall=0
            sing_F1=0
            comp_sin=set(computato[k])
            true_sin=set(target[k])
            
            intersezione=comp_sin.intersection(true_sin)
            false_positive=comp_sin.difference(true_sin)
            false_negative=true_sin.difference(comp_sin)
            jaccard=self.compute_jaccard(comp_sin,true_sin)
            sing_precision=len(intersezione)/(len(comp_sin)+len(false_positive))
            sing_recall=len(intersezione)/(len(intersezione)+len(false_negative))
            sing_F1=(2*sing_precision*sing_recall)/(sing_recall+sing_precision)
            numero_confronti_extra=len(comp_sin.difference(true_sin))
            numero_confronti_reali=len(true_sin)
            numero_confronti_comp=len(comp_sin)
            



            
        
            results.append([name,sing_precision,sing_recall,sing_F1,jaccard,numero_confronti_extra,numero_confronti_reali,numero_confronti_comp,tot_col])
        
        colonne=['name','precision','recall','f1','jaccard','avg comp inutili','n. confronti reali','n. confronti computati','n. no pp']
        results=pd.DataFrame(data=results,columns=colonne)
        return results

    def compute_jaccard(self, A,B):
        intersection=len(list(A.intersection(B)))
        union=(len(list(A))+len(list(B)))-intersection
        return float(intersection)/union

    def eval_print(self,computed,tgt):
        score=0
        sing_score=0
        N=len(tgt.keys())
        stringa=''
        for k in tgt.keys():
            sin_comp=set(computed[k])
            sin_test=set(tgt[k])
            extra=sin_comp.difference(sin_test)
            mancanti=sin_test.difference(sin_comp)
            comuni=sin_test.intersection(sin_comp)
            stringa=stringa+'Campo: '+ k+'\n'
            stringa=stringa+'Computato: '+ str(sin_comp)+'\n'
            stringa=stringa+'Reale: '+ str(sin_test)+'\n'
            stringa=stringa+'Extra: '+ str(extra)+'\n'
            stringa=stringa+'Mancanti: '+ str(mancanti)+'\n'
            stringa=stringa+'Comuni: '+ str(comuni)+'\n'
            
            
            sing_score=self.compute_jaccard(sin_comp,sin_test)
            score=score+sing_score
            stringa=stringa+'Score: '+ str(sing_score)+'\n'
            stringa=stringa+'==================\n'
        
        score=score/N
        stringa=stringa+'SCORE TOTATE: '+ str(score)+'\n'
        with open('Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\risultati_correlazione.txt','w') as f:
            f.write(stringa)
        
        return score/N

    def evaluate(self,computed,tgt):
        score=0
        N=len(tgt.keys())
        for k in tgt.keys():
            sin_comp=set(computed[k])
            sin_test=set(tgt[k])
            score+=self.compute_jaccard(sin_comp,sin_test)
        
        return score/N

    def eval_cardinality(self, comp,tgt):
        evaluation_dic=dict()
        for k in tgt.keys():
            evaluation_dic[k]=[]
            com_elements=set(comp[k])
            tgt_elements=set(tgt[k])
            intersezione=com_elements.intersection(tgt_elements)
            diff_elements_comp=com_elements.difference(tgt_elements)
            diff_element_tgt=tgt_elements.difference(com_elements)

            evaluation_dic[k].append(intersezione)
            evaluation_dic[k].append(diff_elements_comp)
            evaluation_dic[k].append(diff_element_tgt)
            
            intersezione=com_elements.intersection(tgt_elements)
            false_positive=com_elements.difference(tgt_elements)
            false_negative=tgt_elements.difference(com_elements)
            
            sing_precision=len(intersezione)/(len(com_elements)+len(false_positive))
            sing_recall=len(intersezione)/(len(intersezione)+len(false_negative))
            sing_F1=(2*sing_precision*sing_recall)/(sing_recall+sing_precision)
            
            evaluation_dic[k].append(sing_precision)
            evaluation_dic[k].append(sing_recall)
            evaluation_dic[k].append(sing_F1)
            evaluation_dic[k].append(self.compute_jaccard(com_elements,tgt_elements))
            evaluation_dic[k].append(len(tgt_elements))
            evaluation_dic[k].append(len(com_elements))
            
            

        return evaluation_dic
        
            

