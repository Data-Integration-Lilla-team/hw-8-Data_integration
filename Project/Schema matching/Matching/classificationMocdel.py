from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

import pandas as pd

class Classificator:

    def __init__(self):
        self.x=None
        self.y=None


    def classify(self, X, Y):
        
        
        # Load your data
        X = ...  # Your feature matrix
        y = ...  # Your target vector

        # Split your data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Choose a machine learning algorithm
        model = LogisticRegression()

        # Train your model
        model.fit(X_train, y_train)

        # Evaluate your model
        y_pred = model.predict(X_test)
        
