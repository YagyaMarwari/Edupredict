"""
Student Performance Predictor - Master Execution Script
Demonstrating Module I & Module II of Statistical Machine Learning (SML)
"""

import os
import sys
import pandas as pd

# Add src to system path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.data_understanding import (
    print_learning_paradigms,
    classify_features,
    compute_statistical_theory
)
from src.eda import perform_eda
from src.preprocessing import run_preprocessing_pipeline
from src.models import (
    train_simple_linear_regression,
    train_multilinear_regression,
    train_polynomial_regression
)
from src.evaluate import (
    compute_metrics,
    compare_models,
    plot_model_evaluations
)


def main():
    print("=" * 75)
    print("      STUDENT PERFORMANCE PREDICTOR: STATISTICAL MACHINE LEARNING      ")
    print("               Implementation of Module I & Module II                  ")
    print("=" * 75)

    data_path = os.path.join(BASE_DIR, "data", "student_data.csv")
    output_dir = os.path.join(BASE_DIR, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------
    # STAGE 1: MODULE I - DATA UNDERSTANDING & STATISTICAL THEORY
    # -------------------------------------------------------------
    print_learning_paradigms()
    
    raw_df = pd.read_csv(data_path)
    classify_features(raw_df)
    compute_statistical_theory(raw_df)

    # -------------------------------------------------------------
    # STAGE 2: MODULE I - EXPLORATORY DATA ANALYSIS (EDA)
    # -------------------------------------------------------------
    perform_eda(raw_df, output_dir)

    # -------------------------------------------------------------
    # STAGE 3: MODULE II - DATA PRE-PROCESSING PIPELINE
    # -------------------------------------------------------------
    prep_data = run_preprocessing_pipeline(data_path, output_dir)

    X_train = prep_data["X_train"]
    X_test = prep_data["X_test"]
    X_train_scaled = prep_data["X_train_scaled"]
    X_test_scaled = prep_data["X_test_scaled"]
    y_train = prep_data["y_train"]
    y_test = prep_data["y_test"]
    feature_names = prep_data["feature_names"]

    # -------------------------------------------------------------
    # STAGE 4: MODULE II - REGRESSION MODELING
    # -------------------------------------------------------------
    # 1. Simple Linear Regression (using previous period grade G2)
    m1 = train_simple_linear_regression(X_train, X_test, y_train, y_test, feature_name='G2')
    m1_train_metrics = compute_metrics(y_train, m1["y_train_pred"])
    m1_test_metrics = compute_metrics(y_test, m1["y_test_pred"])

    # 2. Multilinear Regression (using all engineered predictors)
    m2 = train_multilinear_regression(X_train_scaled, X_test_scaled, y_train, y_test, feature_names)
    m2_train_metrics = compute_metrics(y_train, m2["y_train_pred"])
    m2_test_metrics = compute_metrics(y_test, m2["y_test_pred"])

    # 3. Polynomial Regression (Degree 2)
    m3 = train_polynomial_regression(X_train_scaled, X_test_scaled, y_train, y_test, degree=2)
    m3_train_metrics = compute_metrics(y_train, m3["y_train_pred"])
    m3_test_metrics = compute_metrics(y_test, m3["y_test_pred"])

    # -------------------------------------------------------------
    # STAGE 5: MODULE II - EVALUATION METRICS & COMPARISON
    # -------------------------------------------------------------
    results = {
        "Simple Linear (G2)": {
            "train_metrics": m1_train_metrics,
            "test_metrics": m1_test_metrics,
            "test_pred": m1["y_test_pred"]
        },
        "Multilinear Regression": {
            "train_metrics": m2_train_metrics,
            "test_metrics": m2_test_metrics,
            "test_pred": m2["y_test_pred"]
        },
        "Polynomial Reg (Deg 2)": {
            "train_metrics": m3_train_metrics,
            "test_metrics": m3_test_metrics,
            "test_pred": m3["y_test_pred"]
        }
    }

    # Print comparative matrix
    summary_df = compare_models(results)

    # Plot actual vs predicted & residual analysis
    plot_model_evaluations(results, y_test, output_dir)

    print("\n" + "=" * 75)
    print("Project run completed successfully!")
    print(f"Generated visualization artifacts saved in: {output_dir}")
    print("=" * 75)


if __name__ == "__main__":
    main()
