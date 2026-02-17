import os
import sys
from dataclasses import dataclass
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data.")
            X_train, y_train, X_test, y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {
                "Gradient Boosting": GradientBoostingClassifier(),
                "Adaboost Classifier": AdaBoostClassifier(),
                "K-Neighbors Classifier": KNeighborsClassifier(),
                "Logistic Regression": LogisticRegression(),
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "XGBClassifier": XGBClassifier()
            }

            params = {

                "Gradient Boosting": {
                    'learning_rate': [0.01, 0.1],
                    'n_estimators': [100, 200],
                    'max_depth': [3, 5],
                    'subsample': [0.8, 1.0]
                },

                "Adaboost Classifier": {
                    'learning_rate': [0.01, 0.1, 0.5],
                    'n_estimators': [50, 100, 200]
                },

                "K-Neighbors Classifier": {
                    'n_neighbors': [5, 7, 9, 11],
                    'weights': ['uniform', 'distance']
                },

                "Logistic Regression": {
                    'C': [0.01, 0.1, 1, 10],
                    'penalty': ['l2'],
                    'solver': ['lbfgs']
                },

                "Random Forest": {
                    'n_estimators': [100, 200],
                    'max_depth': [None, 5, 10],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2]
                },

                "Decision Tree": {
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [None, 5, 10],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2]
                },

                "XGBClassifier": {
                    'learning_rate': [0.01, 0.1],
                    'n_estimators': [100, 200],
                    'max_depth': [3, 5, 7],
                    'subsample': [0.8, 1.0]
                }
            }


            model_report, trained_models = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                             models=models, params=params)

            ## To get best model score from dict
            best_model_score = max(model_report.values())

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = trained_models[best_model_name]


            if best_model_score<0.6:
                raise CustomException("No best Model found")

            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            final_accuracy_score = accuracy_score(y_test, predicted)
            return best_model_name, final_accuracy_score

        except Exception as e:
            raise CustomException(e, sys)