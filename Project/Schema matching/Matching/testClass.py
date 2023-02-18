
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MultiLabelBinarizer

from sklearn.ensemble import RandomForestClassifier
from skmultilearn.problem_transform import BinaryRelevance
from skmultilearn.problem_transform import ClassifierChain
from skmultilearn.problem_transform import LabelPowerset
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.metrics import accuracy_score,hamming_loss
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import pandas as pd
import json

def fun(value):
    x=str(value)
    y=x.split('-')[1]
    return y

def trans(value):
    return str(value) 

def create_data(y):
        set_vals=set()
        for y in Y.values:
            y=set(y)
            set_vals.update(y)
        

        set_vals_dic=dict()
        conta=0
        for i in set_vals:
            set_vals_dic[i]=conta
            conta+=1
        
        
        

        


        #print(set_vals)
        #colonne
        classes=list()
        for y in Y.values:
            vals=list(y)
            vector=[0]*len(set_vals)
            for i in vals:
                pos=set_vals_dic[i]
                vector[pos]=1
            classes.append(vector)
        
        data=pd.DataFrame(data=classes,columns=set_vals_dic.keys())
        data['Y']=Y.apply(trans)
        order=['Y']+(list(set_vals_dic.keys()))
        print(order)
        data=data[order]
        data.to_csv('Project\\Schema matching\\Matching\\test.csv') 
        return list(set_vals_dic.keys() )

def build_model(model,mlb_estimator,xtrain,ytrain,xtest,ytest):
    clf = mlb_estimator(model)
    clf.fit(xtrain,ytrain)
    clf_predictions = clf.predict(xtest)
    acc = accuracy_score(ytest,clf_predictions)
    ham = hamming_loss(ytest,clf_predictions)
    result = {"accuracy:":acc,"hamming_score":ham}
    return result

def generate_syntetic_data(data):
    from sdv.tabular import GaussianCopula
    data=data.astype(str)
    model = GaussianCopula(list(data.columns.values))
    model.fit(data)
    synthetic_data = model.sample(num_rows=data.shape[0]*10)
    
    return synthetic_data


#DECISIONTREE
def train_using_gini(X_train, X_test, y_train):
  
    # Creating the classifier object
    clf_gini = DecisionTreeClassifier(criterion = "gini",
            random_state = 100,max_depth=3, min_samples_leaf=5)
  
    # Performing training
    clf_gini.fit(X_train, y_train)
    return clf_gini 
# Function to perform training with entropy.
def tarin_using_entropy(X_train, X_test, y_train):
  
    # Decision tree with entropy
    clf_entropy = DecisionTreeClassifier(
            criterion = "entropy", random_state = 100,
            max_depth = 3, min_samples_leaf = 5)
  
    # Performing training
    clf_entropy.fit(X_train, y_train)
    return clf_entropy    
# Function to make predictions
def prediction(X_test, clf_object):
  
    # Predicton on test with giniIndex
    y_pred = clf_object.predict(X_test)
    print("Predicted values:")
    print(y_pred)
    return y_pred
      
# Function to calculate accuracy
def cal_accuracy(y_test, y_pred):
      
    print("Confusion Matrix: ",
        confusion_matrix(y_test, y_pred))
      
    print ("Accuracy : ",
    accuracy_score(y_test,y_pred)*100)
      
    print("Report : ",
    classification_report(y_test, y_pred))



def randomForest(data):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split


        

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

        # Create a random forest classifier with 100 trees
        rf = RandomForestClassifier(n_estimators=100)

        # Fit the random forest model to the training data
        rf.fit(X_train, y_train)
        y_pred=rf.predict(X_test)
        print(X_train.head(1))
        print(y_pred[0])

        # Evaluate the model on the testing data
        score = rf.score(X_test, y_test)

        print(f"Accuracy: {score:.2f}")

def decision_tree(X,Y):
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    clf_gini = train_using_gini(X_train, X_test, y_train)
    clf_entropy = tarin_using_entropy(X_train, X_test, y_train)
      
    # Operational Phase
    print("Results Using Gini Index:")
      
    # Prediction using gini
    y_pred_gini = prediction(X_test, clf_gini)
    cal_accuracy(y_test, y_pred_gini)
      
    print("Results Using Entropy:")
    # Prediction using entropy
    y_pred_entropy = prediction(X_test, clf_entropy)
    cal_accuracy(y_test, y_pred_entropy)
      

if __name__=='__main__':

    X=pd.read_csv('Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\files_vari\\ds_features_norm.csv')
    Y='Project\\Schema matching\\SchemaMatchingValentine\\files_matching\\validation_set\\column_sinonimi.txt'
    
    with open(Y,'r') as f:
        data=f.read()
        y_dir=json.loads(data)
        Y=pd.DataFrame(list(y_dir.items()), columns=['column_name', 'Y'])

    

        print(X['column_name'])

        X['column_name']=X['column_name'].apply(fun)
        print(X['column_name'])

        # Merge the dataframes
        data = pd.merge(X, Y, on='column_name')

        data=data.drop(["Unnamed: 0", "column_name"],axis=1)
        cols=data.columns.to_list()
        cols = cols[-1:] + cols[:-1]
        data=data[cols]

        print('prima',len(data))


        #genero dati sintetici
        #data_sy=generate_syntetic_data(data)
        #cols=data_sy.columns.to_list()
        #cols = cols[-1:] + cols[:-1]
        #data_sy=data_sy[cols]

        #data_sy.to_csv('Project\\Schema matching\\Matching\\syn_data.csv')

        syntetic_data=pd.read_csv('Project\\Schema matching\\Matching\\syn_data.csv')
        syntetic_data=syntetic_data.fillna(0)

        data=pd.concat([data, syntetic_data], ignore_index=True, axis=0)
        data=data.fillna(0)
        data=data.drop(["Unnamed: 0"],axis=1)

        print('dopo',len(data))


    


        
        
        Y=data['Y'].apply(trans)
        X=data.drop(['Y'],axis=1)
        print(len(Y))
        print(len(data))
    
        #RandomForest()
        #randomForest()

        decision_tree(X,Y)
        

        '''
    
        data=data.drop(["Unnamed: 0", "column_name"],axis=1)
        


        
        X=data.drop(['Y'],axis=1)
        Y=data['Y']
        #create_data(Y)

        Y=pd.read_csv('Project\\Schema matching\\Matching\\test.csv')

        
       
        #cols=list(Y.columns.values)
        
        #cols=cols[2:]
        #print(cols)

        #X[cols]=Y[cols]
        #X.to_csv('Project\\Schema matching\\Matching\\test_full.csv')
        # using Label Powerset
        
        
        cols=list(Y.columns.values)[2:]
        Y=Y[cols]
        
    
     
        X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=0.3,random_state=42)

        binary_rel_clf = BinaryRelevance(MultinomialNB())
        clf_chain_model = build_model(MultinomialNB(),ClassifierChain,X_train,y_train,X_test,y_test)
        print(clf_chain_model)
        




        
        
        
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Choose a machine learning algorithm
        #dtc=DecisionTreeClassifier(max_depth=5, min_samples_leaf=2)
        clf = MultinomialNB()

        # Create an instance of the MultiOutputClassifier
        multi_clf = MultiOutputClassifier(clf)

        # Train the classifier on the data
        multi_clf.fit(X_train, y_train)

        # Predict the labels for new data
        y_pred = multi_clf.predict(X_test)
        
        score = multi_clf.score(X_test, y_test)
        print(score)
        print(classification_report(y_test, y_pred))
        #print(confusion_matrix(y_test, y_pred))
    '''

        