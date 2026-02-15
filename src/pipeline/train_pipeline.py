from src.components.model_trainer import ModelTrainer

if __name__ == "__main__":
    # This script triggers the training process
    print("Starting the training pipeline...")
    trainer = ModelTrainer()
    trainer.initiate_model_trainer()
    print("Training completed successfully!")
