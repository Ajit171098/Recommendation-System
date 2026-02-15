import os
import pickle
import sys
import pandas as pd
from Recommendation_System_Books.exception.exception_handler import AppException
from Recommendation_System_Books.logger.log import logging
from Recommendation_System_Books.config.configuration import AppConfiguration

class DataValidation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            logging.info(f"{'='*20} Starting Data Validation {'='*20}")
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def preprocess_data(self):
        try:
            books = pd.read_csv(self.data_validation_config.books_csv_file, sep=",", on_bad_lines='skip', encoding='latin-1')
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=",", on_bad_lines='skip', encoding='latin-1')

            logging.info(f"Books dataset shape: {books.shape}")
            logging.info(f"Ratings dataset shape: {ratings.shape}")

            books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
            ## Renaming columns for better readability
            books.rename(columns={'Book-Title': 'book_title', 'Book-Author': 'book_author', 'Year-Of-Publication': 'year',
                     'Publisher': 'publisher', 'Image-URL-L': 'image'}, inplace=True)
            ratings.rename(columns={'User-ID': 'user_id', 'Book-Rating': 'rating'}, inplace=True)

            ## Filtering users who have rated more than 200 books
            no_of_books_read_by_userid = ratings['user_id'].value_counts() > 200
            user_id_greater_than_200 = no_of_books_read_by_userid[no_of_books_read_by_userid].index
            users_who_rated_morethan_200times = ratings[ratings['user_id'].isin(user_id_greater_than_200)]

            ## Merging books and ratings datasets to get the number of ratings per book
            ratings_with_books = books.merge(users_who_rated_morethan_200times, on='ISBN')
            number_of_ratings_per_book = ratings_with_books.groupby('book_title')['rating'].count().reset_index()
            number_of_ratings_per_book.rename(columns={'rating': 'number_of_ratings'}, inplace=True)
            final_books = number_of_ratings_per_book.merge(ratings_with_books, on='book_title')

            ## Filtering books that have received at least 50 ratings
            final_books = final_books[final_books['number_of_ratings'] >= 50]

            ## Removing duplicate entries based on user_id and book_title
            final_books.drop_duplicates(subset=['user_id', 'book_title'], inplace=True)
            logging.info(f"Final dataset shape after preprocessing: {final_books.shape}")

            ## Saving the cleaned dataset
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            final_books.to_csv(os.path.join(self.data_validation_config.clean_data_dir, "clean data.csv"), index=False)
            logging.info(f"Cleaned data saved successfully at: {self.data_validation_config.clean_data_dir}")

            os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
            pickle.dump(final_books, open(os.path.join(self.data_validation_config.serialized_object_dir, "final_books.pkl"), 'wb'))
            logging.info(f"Serialized object saved successfully at: {self.data_validation_config.serialized_object_dir}")
            
        except Exception as e:
            raise AppException(e, sys) from e
        
    def initiate_data_validation(self):
        try:
            logging.info(f"{'='*20} Starting Data Preprocessing {'='*20}")
            self.preprocess_data()
            logging.info(f"{'='*20} Data Preprocessing Completed {'='*20}")
        except Exception as e:
            raise AppException(e, sys) from e