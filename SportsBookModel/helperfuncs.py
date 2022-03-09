"""
Helper functions for model creation
"""
from typing import Callable
import pandas as pd
import numpy as np
from typing import dict, list

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


def feature_list(df: pd.DataFrame) -> list:
    """[summary]

    Args:
        df (pd.DataFrame): [description]

    Returns:
        [type]: [description]
    """

    if df.empty == False:
        return list(df.columns[1:])
    return ["Empty DataFrame"]


def summarise_classification(y_test: pd.Series, y_pred: pd.Series) -> dict[str, object]:

    acc = accuracy_score(
        y_test, y_pred, normalize=True
    )  # Accuracy as a fraction  when True
    num_acc = accuracy_score(
        y_test, y_pred, normalize=False
    )  # Accuracy based on number of predicted labels  when False
    prec = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    return {
        "accuracy": acc,
        "precision": prec,
        "recall": recall,
        "accuracy_count": num_acc,
    }


def build_model(
    classifier_fn: Callable,
    name_of_y_cols: object,
    names_of_X_cols: list,
    dataset: pd.DataFrame,
    test_frac=0.2,
) -> dict:

    X = dataset[names_of_X_cols]
    y = dataset[name_of_y_cols]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_frac)

    model = classifier_fn(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    train_summary = summarise_classification(y_train, y_pred_train)
    test_summary = summarise_classification(y_test, y_pred)

    pred_results = pd.DataFrame({"y_test": y_test, "y_pred": y_pred})

    model_crosstab = pd.crosstab(pred_results.y_pred, pred_results.y_test)

    return {
        "training": train_summary,
        "test": test_summary,
        "confusion_matrix": model_crosstab,
    }


def compare_results(results_dict: dict) -> None:
    for key in results_dict:
        print("Classification: ", key)
        print()
        print("Training Data")
        for score in results_dict[key]["training"]:
            print(score, results_dict[key]["training"][score])
        print()
        for score in results_dict[key]["test"]:
            print(score, results_dict[key]["test"][score])
        print()


if __name__ == "__main__":
    print()
