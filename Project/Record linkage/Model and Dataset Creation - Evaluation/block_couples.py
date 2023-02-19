import deepmatcher as dm
import py_entitymatching as em
import time

class Blocker:

    def __init__(self):
        self.dict = {}
        #self.path_training = r"C:\hw-8-Data_integration\Project\Record linkage\DATASETS\Training set"
        self.path_predict = r"C:\hw-8-Data_integration\Project\Record linkage\DATASETS\Couples for prediction"
        self.path_original = r"C:\hw-8-Data_integration\Project\Record linkage\DATASETS\Dataset separati per lettera"

    def block_couples(self, filename):
        start = time.time()
        A = em.read_csv_metadata(self.path_original + '\\' + filename, key='id', low_memory = False)
        B = em.read_csv_metadata(self.path_original + '\\' + filename, key='id', low_memory = False)

        A = A.rename(columns={'ceo;': 'ceo'})
        B = B.rename(columns={'ceo;': 'ceo'})

        block_f = em.get_features_for_blocking(A, B, validate_inferred_attr_types=False)

        rb = em.RuleBasedBlocker()
        rb.add_rule(['name_name_lev_sim(ltuple, rtuple) < 0.7'], block_f)

        em.set_key(B, 'id')
        em.set_key(A, 'id')

        ob = em.OverlapBlocker()
        K1 = ob.block_tables(A, B, 'name', 'name', 
        l_output_attrs=['name', 'country', 'address', 'founded', 'employees', 'market_cap', 'revenue', 'profit', 'categories', 'ceo', 'city'],
        r_output_attrs=['name', 'country', 'address', 'founded', 'employees', 'market_cap', 'revenue', 'profit', 'categories', 'ceo', 'city'],
        overlap_size=1)

        K2 = ob.block_candset(K1, 'country', 'country', overlap_size=1, allow_missing = True)

        K3 = rb.block_candset(K2)

        K3.to_csv(self.path_predict + '\\' + filename, index = False)

        end = time.time()
        total = end - start
        
        self.dict[filename] = [total]

        #S = em.sample_table(K3, 50)

        #S.to_csv(self.path_training + '\\' + path)

