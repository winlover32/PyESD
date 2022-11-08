# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 10:34:20 2022

@author: dboateng
"""

import os 
import sys 
import pandas as pd 
import numpy as np 
from collections import OrderedDict


from pyESD.Weatherstation import read_station_csv
from pyESD.standardizer import MonthlyStandardizer, StandardScaling
from pyESD.ESD_utils import store_pickle, store_csv
from pyESD.splitter import TimeSeriesSplit, MonthlyBooststrapper, KFold, LeaveOneOut

#relative imports 
from read_data import *
from settings import *

# extract full csv results, use climate score also, add ols model, predict_for 2012_to2017, check the explained variance, 
#use stacking but also predict for all and estimate the mean for comparing



def run_experiment2(variable, estimator, cachedir, stationnames, 
                    station_datadir, base_estimators=None, 
                    final_estimator=None, standardizer_method=None):



    #num_of_stations = len(stationnames)
    
    num_of_stations = 10
    
    for i in range(num_of_stations):
        
        stationname = stationnames[i]
        station_dir = os.path.join(station_datadir, stationname + ".csv")
        SO = read_station_csv(filename=station_dir, varname=variable)
        
        
        #setting predictors 
        SO.set_predictors(variable, predictors, predictordir, radius,)
        
        #setting standardardizer
        if standardizer_method is None:
            SO.set_standardizer(variable, standardizer=MonthlyStandardizer(detrending=False,
                                                                            scaling=False))
            
        else: 
            
            SO.set_standardizer(variable, standardizer= standardizer_method)
            
    
        #setting model
        
        #setting model
        scoring = ["neg_root_mean_squared_error",
                   "r2", "neg_mean_absolute_error"]
        
        
        if estimator == "Stacking":
            
            SO.set_model(variable, method=estimator, ensemble_learning=True, 
                     estimators=base_estimators, final_estimator_name=final_estimator, daterange=from1961to2012,
                     predictor_dataset=ERA5Data, cv=TimeSeriesSplit(n_splits=30, test_size=5, gap=12), 
                                   scoring=scoring)
        else:
            
            
            SO.set_model(variable, method=estimator, daterange=from1961to2012, 
                         predictor_dataset=ERA5Data, cv=TimeSeriesSplit(n_splits=30, test_size=5, gap=12), 
                                       scoring=scoring)
        
        #fitting model (with predictor selector optioin)
        
        selector_method = "TreeBased"
        
        SO.fit(variable,  from1961to2012, ERA5Data, fit_predictors=True, predictor_selector=True, 
                selector_method=selector_method , selector_regressor="RandomForest",
                cal_relative_importance=False, impute=False, impute_method="spline", impute_order=5)
        
        
        if estimator == "RandomForest":
            importance = SO.tree_based_feature_permutation_importance(variable, from1961to2012, ERA5Data, fit_predictors=True, 
                                                                      plot=False)
            
        
        score_fit, ypred_fit = SO.cross_validate_and_predict(variable,  from1961to2012, ERA5Data,)
        
        ypred_train = SO.predict(variable, from1961to2012, ERA5Data)
        
        y_obs_train = SO.get_var(variable, from1961to2012, anomalies=True)
        
        
        predictions = pd.DataFrame({
            "obs_train" : y_obs_train,
            "ERA5 1961-2012" : ypred_train})
        
        
        #storing of results
        
        store_pickle(stationname, "validation_score_" + estimator, score_fit, cachedir)
        store_csv(stationname, "validation_predictions_" + estimator, ypred_fit, cachedir)
        store_csv(stationname, "predictions_" + estimator, predictions, cachedir)
        
        if estimator == "RandomForest":
            store_pickle(stationname, "importance_", importance, cachedir)



if __name__ == "__main__":
    
    
    selector_dir = "C:/Users/dboateng/Desktop/Python_scripts/ESD_Package/examples/Ghana/model_selection"
    cachedir = selector_dir
       
    variable = "Precipitation"
       
    stationnames = stationnames_prec
       
    station_datadir = station_prec_datadir
    
    final_estimator = "ExtraTree"
    
    base_estimators = ["LassoLarsCV", "ARD", "MLP", "RandomForest", "XGBoost", "Bagging"]
    

    estimators = ["LassoLarsCV", "ARD", "MLP", "RandomForest", "XGBoost", "Bagging", "Stacking"]
    
    
        
    for estimator in estimators:
        
        print("--------- runing model for:", estimator, "-----------")
    
        run_experiment2(variable, estimator, cachedir, stationnames, station_datadir, 
                        base_estimators, final_estimator)