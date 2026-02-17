from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        # 1. Data Ingestion
        ingestion = DataIngestion()
        train_path, test_path = ingestion.initiate_data_ingestion()

        # 2. Data Transformation
        transformation = DataTransformation()
        train_arr, test_arr, _ = transformation.initiate_data_transformation(train_path, test_path)

        # 3. Model Training
        trainer = ModelTrainer()
        accuracy = trainer.initiate_model_trainer(train_arr, test_arr)

        return accuracy


if __name__ == "__main__":
    print("Starting Training Pipeline...\n")

    pipeline = TrainPipeline()   #  OBJECT CREATED HERE
    model_name, acc = pipeline.run_pipeline()

    print("\nTraining completed successfully ")
    print(f"Best Model: {model_name}")
    print(f"Accuracy: {acc:.4f}")
