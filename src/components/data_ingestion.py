import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np


from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components import data_transformation
from src.components import model_trainer

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join('artifacts','train.csv')
    test_data_path = os.path.join('artifacts','test.csv')
    raw_data_path = os.path.join('artifacts','raw_data.csv')


class DataIngestion:

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def ingestion_data(self):
        logging.info('Starting the data ingestion process')
        try:
            data = pd.read_csv(os.path.join(os.getcwd(),'src\\data\\stud.csv'))
            logging.info('Data ingested Successfully')
        except Exception as e:
            logging.info(CustomException(e, sys))
            raise CustomException(e,sys)
        
        logging.info('Started Spliting the main data in train and test data')
        try:
            train_df,test_df=train_test_split(data,test_size=0.2,random_state=34)
            logging.info('Splitted data into train and test data')
        except Exception as e:
            logging.info(CustomException(e, sys))
            raise CustomException(e,sys)
        
        try:
            logging.info('Making artifact directory to save files')
            os.makedirs('artifacts',exist_ok=True)

            logging.info('Started Saving the train, test and raw data in artifact folder')
            # print(self.ingestion_config.train_data_path)
            train_df.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_df.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info('Saved the train, test and raw data Success fully')
        except Exception as e:
            logging.info(CustomException(e, sys))
            raise CustomException(e,sys)
        
        return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)



if __name__ == '__main__':
    obj = DataIngestion()
    train_path,test_path = obj.ingestion_data()
    data_transformation = data_transformation.DataTransformation()
    processed_train_Data,processed_test_data = data_transformation.transform_object(train_path,test_path)
    md = model_trainer.ModelTrainer()
    r2_score=md.model_training(processed_train_Data,processed_test_data)
    print(r2_score)






