import os
import pickle
import sys
import logging
import pandas as pd
from Recommendation_System_Books.exception.exception_handler import AppException
from Recommendation_System_Books.config.configuration import AppConfiguration


class DataTransformation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            logging.info(f"{'='*20} Starting Data Transformation {'='*20}")
            self.data_transformation_config = app_config.get_data_transformation_config()
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def transform_data(self):
        try:
            clean_data_file_path = self.data_transformation_config.clean_data_file_path
            transformed_data_dir = self.data_transformation_config.transformed_data_dir

            logging.info(f"Reading clean data from: {clean_data_file_path}")
            clean_data = pd.read_csv(clean_data_file_path, sep=",", on_bad_lines='skip', encoding='latin-1')

            ## make pivot table with book_title as index, user_id as columns and rating as values
            book_pivot = clean_data.pivot_table(index='book_title', columns='user_id', values='rating')
            book_pivot.fillna(0, inplace=True)

            ## Get the book names from the pivot table index
            books_names = book_pivot.index

            ## Saving pivot table data
            os.makedirs(transformed_data_dir, exist_ok=True)
            pickle.dump(book_pivot, open(os.path.join(transformed_data_dir, "transformed_data.pkl"), 'wb'))
            logging.info(f"Transformed data saved successfully at: {transformed_data_dir}")

            ## Saving the book names as a serialized object for later use in the web application
            os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
            pickle.dump(books_names, open(os.path.join(self.data_validation_config.serialized_object_dir, "books_names.pkl"), 'wb'))
            logging.info(f"Serialized object for book names saved successfully at: {self.data_validation_config.serialized_object_dir}")

            ## Saving the pivot table data as a serialized object for later use in the web application
            os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
            pickle.dump(book_pivot, open(os.path.join(self.data_validation_config.serialized_object_dir, "book_pivot.pkl"), 'wb'))
            logging.info(f"Transformed data saved successfully at: {self.data_validation_config.serialized_object_dir}")
            
        except Exception as e:
            raise AppException(e, sys) from e
        
    def initiate_data_transformation(self):
        try:
            logging.info(f"{'='*20} Initiating data transformation process {'='*20}")
            self.transform_data()
            logging.info(f"{'='*20} Data transformation process completed successfully {'='*20}")
        except Exception as e:
            raise AppException(e, sys) from e