# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 11:02:35 2022

@author: dboateng
"""

# importing models
import sys
from sklearn.ensemble import StackingRegressor, VotingRegressor
from sklearn.model_selection import cross_val_score, cross_validate, cross_val_predict

sys.path.append("C:/Users/dboateng/Desktop/Python_scripts/ESD_Package")
from Package.models import Regressors

class EnsembleRegressor():
    
    def __init__(self, estimators, final_estimator=None, cv=10, n_jobs=-1, passthrough=False, method="Stacking"):
        self.estimators = estimators 
        self.final_estimator = final_estimator 
        self.cv = cv
        self.n_jobs = n_jobs
        self.passthrough = passthrough
        self.method = method
        
        if self.final_estimator == None:
            regressor = Regressors(method="RandomForest", cv=10)
            regressor.set_model()
            print("....using random forest as final estimator......")
            self.final_estimator = regressor.estimator 
        if self.method == "Stacking":   
            self.ensemble = StackingRegressor(estimators=self.estimators, final_estimator=self.final_estimator, cv=self.cv, 
                                             passthrough=self.passthrough, n_jobs=self.n_jobs)
        elif self.method == "Voting":
            self.ensemble = VotingRegressor(estimators=self.estimators, n_jobs=self.n_jobs)
            
        else:
            raise ValueError("The ensembles are Stacking Generalization or Voting, check the name of the method")
        
    def fit(self, X,y):
        return self.ensemble.fit(X,y)
    
    
    def predict(self, X):
        yhat = self.ensemble.predict(X)
        return yhat
    
    def score(self, X,y):
        return self.ensemble.score(X,y)
    
    def get_params(self, deep=True):
        params = self.ensemble.get_params(deep)
        return params
    
    def transform(self, X):
        y_preds = self.ensemble.transform(X)
        return y_preds
    
    def cross_val_score(self, X, y):
        return cross_val_score(self.ensemble, X, y, cv=self.cv)
    
    def cross_validate(self, X, y):
        return cross_validate(self.ensemble, X, y, scoring=["r2", "neg_root_mean_squared_error"],
                                n_jobs=2, verbose=0, cv=self.cv)
    
    def cross_val_predict(self, X, y):
        return cross_val_predict(self.ensemble, X, y, n_jobs=2, verbose=0)


