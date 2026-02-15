import os
import sys
import dill
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        trained_models = {}

        for model_name, model in models.items():

            param_grid = params.get(model_name, {})

            if len(param_grid) == 0:
                model.fit(X_train, y_train)
                best_model = model
            else:
                gs = GridSearchCV(
                    model,
                    param_grid,
                    cv=3,
                    scoring='accuracy',
                    n_jobs=-1
                )
                gs.fit(X_train, y_train)
                best_model = gs.best_estimator_

            y_test_pred = best_model.predict(X_test)
            test_score = accuracy_score(y_test, y_test_pred)

            report[model_name] = test_score
            trained_models[model_name] = best_model

            print(f"{model_name}: Test Acc={test_score:.4f}")

        return report, trained_models

    except Exception as e:
        raise CustomException(e, sys)
