'''
Classe specializzata nella valutazione dei dizionari dei sinonimi mediante Jaccard

'''
class Eval:

    def __init__(self):
        pass

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
            evaluation_dic[k].append(self.compute_jaccard(com_elements,tgt_elements))
            

        return evaluation_dic
        
            

