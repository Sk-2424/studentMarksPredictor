from ast import mod
from inspect import Parameter
import json
import os
import sys 
from src.logger import logging
from src.exception import CustomException

import pickle

from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score

def save_object(obj,file_path):
    logging.info('Saving a pickel file')
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logging.info('Pickel file saved successfully')
    except Exception as e:
        logging.info(CustomException(e,sys))
        raise CustomException(e,sys)
    
def open_json_file(file_path):
    try:
        with open(file_path,'r') as file:
            data = json.load(file)
            logging.info("Loaded the json file Successfully")
        return data
    except Exception as e:
        logging.info(CustomException(e,sys))
        raise CustomException(e,sys)
    

def train_and_evaluate_model(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = RandomizedSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        logging.info('model report is created')

        return report

    except Exception as e:
        logging.info(CustomException(e,sys))
        raise CustomException(e, sys)

    
def load_object(file_path):
    try:
        with open(file_path,'rb') as file :
            data = pickle.load(file)
            logging.info('Pkl file loaded successfully')
            return data
    except Exception as e:
        logging.info(CustomException(e,sys))
        raise CustomException(e,sys)







            
        


