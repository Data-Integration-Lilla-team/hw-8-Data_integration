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

    def evaluate(self,computed,tgt):
        score=0
        N=len(computed.keys())
        for k in computed.keys():
            sin_comp=set(computed[k])
            sin_test=set(tgt[k])
            score+=self.compute_jaccard(sin_comp,sin_test)
        
        return score/N
            

