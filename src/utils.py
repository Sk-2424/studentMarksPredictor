import os
import sys 
from src.logger import logging
from src.exception import CustomException

import pickle

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
    

    


            
        


