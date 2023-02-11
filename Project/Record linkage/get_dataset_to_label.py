import deepmatcher as dm
import py_entitymatching as em
import time

class getList:

    def __init__(self):
        self.dict = {}
        self.path_training = r"C:\hw-8-Data_integration\Project\Record linkage\Training set"
        self.path_predict = r"C:\hw-8-Data_integration\Project\Record linkage\Couples for prediction"
        self.path_original = r"C:\hw-8-Data_integration\Project\Record linkage\Dataset separati per lettera"

    def generate_list(self, path):
        start = time.time()
        A = em.read_csv_metadata(self.path_original + '\\' + path, key='ID', low_memory = False)
        B = em.read_csv_metadata(self.path_original + '\\' + path, key='ID', low_memory = False)

        A = A.rename(columns={'ceo;': 'ceo'})
        B = B.rename(columns={'ceo;': 'ceo'})

        block_f = em.get_features_for_blocking(A, B, validate_inferred_attr_types=False)

        rb = em.RuleBasedBlocker()
        rb.add_rule(['name_name_lev_sim(ltuple, rtuple) < 0.3'], block_f)

        em.set_key(B, 'ID')
        em.set_key(A, 'ID')

        ob = em.OverlapBlocker()
        K1 = ob.block_tables(A, B, 'name', 'name', 
        l_output_attrs=['name', 'country', 'headquarters', 'address', 'founded', 'employees', 'market_cap', 'revenue', 'profit', 'industry', 'sector', 'categories', 'ceo'],
        r_output_attrs=['name', 'country', 'headquarters', 'address', 'founded', 'employees', 'market_cap', 'revenue', 'profit', 'industry', 'sector', 'categories', 'ceo'],
        overlap_size=1)

        K2 = ob.block_candset(K1, 'country', 'country', overlap_size=1, allow_missing = True)

        K3 = rb.block_candset(K2)

        K3.to_csv(self.path_predict + '\\' + path)

        end = time.time()
        total = end - start
        
        self.dict[path] = [total]

        S = em.sample_table(K3, 50)

        S.to_csv(self.path_training + '\\' + path)

