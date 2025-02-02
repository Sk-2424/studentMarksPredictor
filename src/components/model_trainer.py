import os
import sys

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,open_json_file,train_and_evaluate_model

from dataclasses import dataclass

# from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
# from xgboost import XGBRegressor

@dataclass
class ModelConfig:
    model_config_Path: str = os.path.join('artifacts','model.pkl')

class ModelTrainer:

    def __init__(self):
        self.model_config = ModelConfig()
        # print(self.model_config.model_config_Path)
    
    def model_training(self,train_data,test_data):
        # print(self.model_config.model_config_Path)
        X_train = train_data[:,:-1]
        Y_train = train_data[:,-1]
        X_test = test_data[:,:-1]
        Y_test = test_data[:,-1]

        logging.info('Train & test data splitted into independent and dependent features')

        models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                # "XGBRegressor": XGBRegressor(),
                # "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
        
        params = open_json_file('params\hyperparameter.json')

        model_report = train_and_evaluate_model(X_train,Y_train,X_test,Y_test,models,params)

        best_model_score = max(sorted(model_report.values()))
        
        best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
        best_model = models[best_model_name]

        logging.info('Best model is selected on the basis of R2 Score')

        if best_model_score<0.6:
                raise CustomException("No best model found")
        logging.info(f"Best found model on both training and testing dataset")
        # print(self.model_config.model_config_path)
        save_object(best_model,
                self.model_config.model_config_Path)

        print(best_model)

        predicted=best_model.predict(X_test)

        r2_square = r2_score(Y_test, predicted)
        return r2_square




