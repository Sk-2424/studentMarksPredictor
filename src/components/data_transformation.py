import os
import sys
from xml.etree.ElementTree import PI

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass


@dataclass
class DataTransformationConfig:
    preprocessor_pkl_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:

    def __init__(self):
        self.preprocessor_pkl_path = DataTransformationConfig()


    def get_transformer_object(self):

        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            num_col_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            cat_col_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoding', OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            preprocessor_obj = ColumnTransformer(
                [
                    ('num_pipeline',num_col_pipeline,numerical_columns),
                    ('categorical_pipeline',cat_col_pipeline,categorical_columns)
                ]
            )

            logging.info('Numerical col  & Categorical col pipeline is created')

            return preprocessor_obj
        except Exception as e:
            logging.info(CustomException(e,sys))
            raise CustomException(e,sys)
        

    def transform_object(self,train_path,test_path):
        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            logging.info('Read the Train and test data')
        except Exception as e:
            logging.info(CustomException(e,sys))
            raise CustomException(e,sys)
        
        target_col = 'math_score'
        try:
            input_feature_train_df = train_data.drop(columns=target_col, axis=1)
            train_df_target_feature = train_data[target_col]
            logging.info('Train data splitted in to Dependent & Independent features')

            input_feature_test_df  = test_data.drop(columns=target_col,axis=1)
            test_df_target_feature = test_data[target_col]
            logging.info('Test data splitted in independent and dependent features')

            preprocessor_obj = self.get_transformer_object()
            logging.info('Preprocessor object is created')

            train_data_processed = preprocessor_obj.fit_transform(input_feature_train_df)
            test_data_processed = preprocessor_obj.transform(input_feature_test_df)
            logging.info('processed both train and test data independent features')

            train_arr = np.c_[
                train_data_processed, np.array(train_df_target_feature)
            ]
            test_arr = np.c_[test_data_processed, np.array(test_df_target_feature)]

            logging.info('Merged Processed Independent col and targets col for both train & test data ')

            save_object(preprocessor_obj,self.preprocessor_pkl_path.preprocessor_pkl_path)

            logging.info('Preprocessor Pickel file is saved in artifact folder')

            return (train_arr,test_arr)
        except Exception as e:
            logging.info(CustomException(e,sys))
            raise CustomException(e,sys)


# if __name__ == '__main__':
#     dt = DataTransformation()
#     print(dt.preprocessor_pkl_path.preprocessor_pkl_path)
#     dt1 = DataTransformationConfig()
#     print(dt1.preprocessor_pkl_path)


        




