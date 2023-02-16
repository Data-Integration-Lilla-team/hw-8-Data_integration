from Levenshtein import distance
import ngram
class Token_obj:

    #INPUT
    #Nome della colonna
    #sinonimi pregressi (dizionario fino all'iterazione i)
    #sin_attuali=dizionario dei sinonimi che viene calcolato post valentine

    #utilità
    #Nella name correlation verifichiamo tra due nomi A,B vediamo:
    #1. sin_sim(A,B)>=T1
    #2. A inter B>=T2
    #3. AVG sim (c in A-B and B-A)>=T3
    #4 Score finale =combinazione dei tre input (1,2,3)>=T4
    #Se sono match due
    def __init__(self,name_ture,sinonimi_pregressi):
        self.sin_preg=sinonimi_pregressi
        self.sin_attuali=set()
        self.true_name=name_ture
        self.name=self.true_name.split('-')[1]


        #thresholds
        #aggiornamento immediato
        #se lo score è maggiore di >=0.8
        self.update_imm=0.8
        
        #inserimento nei sinonimi attuali
        self.thresh_sim_sin_attuali=0.25



    
    #SCORE 2
    #inserisci anche il nome di A e B
    def compute_jaccard(self, A,B):
        intersection=len(list(A.intersection(B)))
        union=(len(list(A))+len(list(B)))-intersection
        jaccard=float(intersection)/union
        print('SCORE 2')
        print('Jaccard',jaccard)
        return jaccard

    #SCORE 1
    def compute_dist1(self,A,B):
        Levi=distance(A,B)
        if Levi>0:
            Levi_inv=1/Levi
        else:
            Levi_inv=0
        n_grams=ngram.NGram.compare(A,B,N=3)
        n_grams2=ngram.NGram.compare(A,B,N=4)
        print('SCORE 1')
        print(A,'Levi',B,'=',Levi_inv)
        print(A,'3gram',B,'=',n_grams)
        print(A,'4gram',B,'=',n_grams2)
        

        out=((Levi_inv+n_grams+n_grams2)/3)
        return out
    
    #SCORE 3
    #inserisci anche A e B
    def compute_input_score_3(self,A,nameA,B,nameB):
        A.add(nameA)
        B.add(nameB)

        set_1=A-B
        set_2=B-A
        
        return (set_1,set_2)


    def compute_score3(self, inputA,inputB):
        score=0
        N_a=len(inputA)
        N_b=len(inputB)
        inputA=list(inputA)
        inputB=list(inputB)
        print('SCORE 3')
        for i in range(0,len(inputA)):
            A=inputA[i]
            
            for j in range(0,len(inputB)):
                current_score=self.compute_dist1(inputA[i],inputB[j])
                score+=current_score

        print('Similarity tokens not commom:',score/(N_a+N_b))
        return score/(N_a+N_b)

    def update_sin_attuali(self,B, score):
        if score>=self.update_imm:
            B.sin_preg.add(self.name)
            self.sin_preg.add(B.name)
            self.sin_preg.update(B.sin_preg)
            B.sin_preg.update(A.sin_preg)

        if score>=self.thresh_sim_sin_attuali:
            self.sin_attuali.add(B.name)

    def confront_columns(self, token_B):
        final_score=0




        #1. Score sim(A,B)
        #AVG Levi-1*Ngrams
    
        score_1=self.compute_dist1(self.name,token_B.name)

        #2. Score intersection sinonimi storici A e B
        #Jaccard A e B
        score_2=self.compute_jaccard(self.sin_preg,token_B.sin_preg)

        #3 Score sim(A,B) per ogni A e B in (A.sin_pre - B.sin_pre) union B.sin_pre - A.sin_pre
        input_score3=self.compute_input_score_3(A=self.sin_preg,nameA=self.name,B=token_B.sin_preg,nameB=token_B.name)
        score_3=self.compute_score3(input_score3[0],input_score3[1])

        print('Score 1',score_1)
        
        print('Score 2',score_2)
        print('Score 3',score_3)
        final_score=(score_1+score_2+score_3)/3

        self.update_sin_attuali(token_B,final_score)

        token_B.update_sin_attuali(self,final_score)

        print(final_score)
    

    

if __name__=='__main__':
    A=Token_obj('09.wissel-name',{'name','company','company_name'})
    
    B=Token_obj('10.DEBIGA-name_company',{'name','nome','company_name'})
    print(A.confront_columns(B))
    C=Token_obj('03.gren-market_cap',{'master_cap','marketcap'})
    print(A.confront_columns(C))

    #post 
    print('sin attuali A',A.sin_attuali)
    print('sin_attuali B', B.sin_attuali)
    print('sin_Attuali C', C.sin_attuali)


