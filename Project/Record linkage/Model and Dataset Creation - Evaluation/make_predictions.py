import deepmatcher as dm
import time 

class Predictor:

    def __init__(self, model):
        self.dict = {}
        self.model = model
        self.path_predict = r"C:\hw-8-Data_integration\Project\Record linkage\DATASETS\Couples for prediction"
        self.path_save = r"C:\hw-8-Data_integration\Project\Record linkage\DATASETS\Predictions"
    
    def make_prediction(self, filename):
        start = time.time()

        candidate = dm.data.process_unlabeled(
                    path = self.path_predict + '\\' + filename,
                    trained_model = self.model,
                    ignore_columns = ('ltable_ID', 'rtable_ID'))
        
        predictions = self.model.run_prediction(candidate, output_attributes=list(candidate.get_raw_table().columns))

        end = time.time()
        total = end - start
        self.dict[filename] = [total]

        predictions.to_csv(self.path_save + '\\' + filename, index = False)
