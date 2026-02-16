import os
import pickle
import sys

from sklearn.neighbors import NearestNeighbors
from Recommendation_System_Books.exception.exception_handler import AppException
from Recommendation_System_Books.config.configuration import AppConfiguration
from Recommendation_System_Books.entity.config_entity import ModelTrainerConfig
from Recommendation_System_Books.logger.log import logging
from scipy.sparse import csr_matrix

class ModelTrainer:
    def __init__(self, app_config = AppConfiguration()):
        try:
            logging.info(f"{'='*20} Get Model Trainer config {'='*20}")
            self.model_trainer_config = app_config.get_model_trainer_config()
        except Exception as e:
            raise AppException(e, sys) from e
        
    def train_model(self):
        try:
            logging.info(f"{'='*20} Starting model training {'='*20}")
            
            # Load the transformed(pivot table) data from the pickle file
            books_pivot = pickle.load(open(self.model_trainer_config.transformed_data_file_path, 'rb'))

            # Convert the pivot table to a sparse matrix
            book_sparse_matrix = csr_matrix(books_pivot)
            
            # Train the Nearest Neighbors model using the sparse matrix
            model = NearestNeighbors(algorithm='brute')
            model.fit(book_sparse_matrix)

            # Save the trained model as a pickle file
            os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
            model_file_path = os.path.join(self.model_trainer_config.trained_model_dir, self.model_trainer_config.model_file_name)
            pickle.dump(model, open(model_file_path, 'wb'))
            logging.info(f"Trained model saved successfully at: {model_file_path}")

            logging.info(f"{'='*20} Model training completed successfully {'='*20}")
        except Exception as e:
            raise AppException(e, sys) from e
        
    def initiate_model_trainer(self):
        try:
            logging.info(f"{'='*20} Initiating model training process {'='*20}")
            self.train_model()
            logging.info(f"{'='*20} Model training process completed successfully {'='*20}")
        except Exception as e:
            raise AppException(e, sys) from e
        