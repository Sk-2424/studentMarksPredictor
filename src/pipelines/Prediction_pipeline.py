import os
import sys
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object

from src.components import data_ingestion
from src.components import data_transformation
from src.components import model_trainer

class Prediction_Pipeline:
    def __init__(self):
        pass

    def prediction(self,features):
            try:
                model_path=os.path.join("artifacts","model.pkl")
                preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
                model=load_object(file_path=model_path)
                preprocessor=load_object(file_path=preprocessor_path)
                logging.info('Both Preprocessor and model pickel file loaded successfully')
                data_scaled=preprocessor.transform(features)
                preds=model.predict(data_scaled)
                logging.info(f'Model has predicted the score i.e {preds[0]}')
                return preds
            except Exception as e:
                logging.info(CustomException(e,sys))
                raise CustomException(e,sys)
            

class CustomData:
    def __init__(  self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender

        self.race_ethnicity = race_ethnicity

        self.parental_level_of_education = parental_level_of_education

        self.lunch = lunch

        self.test_preparation_course = test_preparation_course

        self.reading_score = reading_score

        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)