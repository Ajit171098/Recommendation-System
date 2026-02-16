import pickle
import streamlit as st
import numpy as np
from Recommendation_System_Books.logger.log import logging  
from Recommendation_System_Books.pipeline.training_pipeline import TrainingPipeline
from Recommendation_System_Books.config.configuration import AppConfiguration
from Recommendation_System_Books.exception.exception_handler import AppException
import sys
import os

class RecommendBooks:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.model_recommendation_config = app_config.get_model_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e
        
    def fetchPoster(self, suggestions):
        try:
            # Load the pivot table and the final books data from the serialized objects
            book_pivot = pickle.load(open(self.model_recommendation_config.book_pivot_serialized_objects, 'rb'))
            final_books = pickle.load(open(self.model_recommendation_config.final_books_serialized_objects, 'rb'))

            ## Get the names of the suggested books based on the indices
            suggested_book_names = []
            for i in suggestions:
                suggested_book_names.append(book_pivot.index[i])

            ## Get the indices of the suggested book names in the final books data
            index_ids = []
            for i in suggested_book_names[0]:
               ids = np.where(final_books['book_title'] == i)[0][0]
               index_ids.append(ids)

            ## Fetch the poster URLs for the suggested books based on the indices
            post_urls = []
            for i in index_ids:
                post_urls.append(final_books.iloc[i]['image'])

            return post_urls

        except Exception as e:
            raise AppException(e, sys) from e
        
    def get_recommendations(self, book_name):
        try:
            ## Load the trained model and the pivot table data from the serialized objects
            model = pickle.load(open(self.model_recommendation_config.trained_model_path, 'rb'))
            book_pivot = pickle.load(open(self.model_recommendation_config.book_pivot_serialized_objects, 'rb'))

            ## Get the index of the input book name in the pivot table
            book_id = np.where(book_pivot.index == book_name)[0][0]

            ## Get the distances and indices of the nearest neighbors for the input book
            distance, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

            ## Fetch the poster URLs for the suggested books
            fetched_poster_urls = self.fetchPoster(suggestions)

            ## Get the names of the suggested books based on the indices
            suggested_book_names = []
            for i in suggestions:
                suggested_book_names.append(book_pivot.index[i])

            return suggested_book_names[0][0:], fetched_poster_urls[0:]
        except Exception as e:
            raise AppException(e, sys) from e
        
    def train_engine(self):
        try:
            training_pipeline = TrainingPipeline()
            training_pipeline.start_training_pipeline()
            st.text("Model training completed successfully!")

        except Exception as e:
            raise AppException(e, sys) from e
        
    def AllRecommendation(self, selected_book):
        try:
            recommended_books, recommended_books_posters = self.get_recommendations(selected_book)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_books[1])
                st.image(recommended_books_posters[1])
            with col2:
                st.text(recommended_books[2])
                st.image(recommended_books_posters[2])
            with col3:
                st.text(recommended_books[3])
                st.image(recommended_books_posters[3])
            with col4:
                st.text(recommended_books[4])
                st.image(recommended_books_posters[4])
            with col5:
                st.text(recommended_books[5])
                st.image(recommended_books_posters[5])
        except Exception as e:
            raise AppException(e, sys) from e
        
if __name__ == "__main__":
    st.title("Book Recommendation System")
    st.text("Select a book from the dropdown to get recommendations")
    try:
        recommend_books = RecommendBooks()

        ## train the model when the "Train Model" button is clicked
        if(st.button("Train Model")):
            recommend_books.train_engine()

        book_names = pickle.load(open(recommend_books.model_recommendation_config.books_names_serialized_objects, 'rb'))
        selected_book = st.selectbox("Select a book", book_names)

        if st.button("Show Recommendation"):
            recommend_books.AllRecommendation(selected_book)
    except Exception as e:
        raise AppException(e, sys) from e