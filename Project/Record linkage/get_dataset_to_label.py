import deepmatcher as dm
import py_entitymatching as em

class getList:
    def __init__(self, path):
        self.A = em.read_csv_metadata(path, key='id')
        self.B = em.read_csv_metadata(path, key='id')

    def generate_list(self):
        # Basic information about the tables.
        print('Number of tuples in A: ' + str(len(self.A)))
        print('Number of tuples in B: ' + str(len(self.B)))
        print('Number of tuples in A X B (i.e the cartesian product): ' + str(len(self.A)*len(self.B)))

        #BLOCKING
        ob = em.OverlapBlocker()
        K1 = ob.block_tables(self.A, self.B, 'name', 'name',
                    l_output_attrs=['SCHEMA MEDIATO'], 
                    r_output_attrs=['SCHEMA MEDIATO'],
                    overlap_size=2) #DA SCEGLIERE

        print(f'Number of comparisons after one step of blocking: {len(K1)}')
        value = input('Is this number enough? (Y/N)')

        if(value == 'N' or value == 'n'):
            #CONTIUNA IL BLOCKING
            K1 = ob.block_tables(K1, 'ATTRIBUTO', 'ATTRIBUTO', overlap_size = 1) #DA SCEGLIERE
        
        S = em.sample_table(K1, 100)
        S.to_csv(r'PATH\to_label.csv', index = False)
