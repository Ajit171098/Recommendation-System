from Recommendation_System_Books.components.stage_00_data_ingestion import DataIngestion
from Recommendation_System_Books.components.stage_01_data_validation import DataValidation
from Recommendation_System_Books.components.stage_02_data_transformation import DataTransformation
from Recommendation_System_Books.components.stage_03_model_trainer import ModelTrainer

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()

    def start_data_ingestion(self):
        self.data_ingestion.initiate_data_ingestion()

    def start_data_validation(self):
        self.data_validation.initiate_data_validation()

    def start_training_pipeline(self):
        self.data_transformation.initiate_data_transformation()

    def start_model_trainer(self):
        self.model_trainer.initiate_model_trainer()