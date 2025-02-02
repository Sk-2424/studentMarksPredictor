import os
import sys


from src.exception import CustomException
from src.logger import logging

from src.components import data_ingestion
from src.components import data_transformation
from src.components import model_trainer

try:
    obj = data_ingestion.DataIngestion()
    train_path,test_path = obj.ingestion_data()
    data_transformation = data_transformation.DataTransformation()
    processed_train_Data,processed_test_data = data_transformation.transform_object(train_path,test_path)
    md = model_trainer.ModelTrainer()
    r2_score=md.model_training(processed_train_Data,processed_test_data)
    logging.info(f"R2 Score of Final model {r2_score}")
except Exception as e:
    logging.info(CustomException(e,sys))
    raise CustomException(e,sys)
