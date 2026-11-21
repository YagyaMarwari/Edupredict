"""
Module I: Understanding Data & Statistical Foundations
- Structured vs Unstructured data
- Quantitative vs Qualitative features
- Statistical Theory: Mean, Median, Mode, Standard Deviation, Variance, Range
"""

import pandas as pd
import numpy as np


def print_learning_paradigms():
    print("=" * 70)
    print("MODULE I: STATISTICAL MACHINE LEARNING - LEARNING PARADIGMS")
    print("=" * 70)
    print("1. Supervised Learning:")
    print("   - Learns mapping from inputs X to ground truth target y.")
    print("   - Student Performance Predictor is SUPERVISED REGRESSION:")
    print("     Target: G3 (Final Exam Score, continuous numerical variable).")
    print("2. Unsupervised Learning:")
    print("   - Discovers hidden patterns/clusters without predefined labels (e.g. K-Means).")
    print("3. Reinforcement Learning:")
    print("   - Learns optimal policies via reward/penalty feedback from an environment.")
    print("-" * 70)


def classify_features(df: pd.DataFrame):
    """
    Classifies dataset attributes into Quantitative vs Qualitative
    and Structured Data attributes.
    """
    print("\n" + "=" * 70)
    print("MODULE I: UNDERSTANDING DATA - TAXONOMY & DATA TYPES")
    print("=" * 70)
    print("Data Format: STRUCTURED DATA (Tabular rows & columns, well-defined schema)")
    print("-" * 70)

    # Classification dictionary
    taxonomy = {
        "Target Variable": ["G3 (Final Grade, 0-20 scale)"],
        "Quantitative (Continuous/Discrete)": [
            "age", "studytime", "failures", "absences", "G1 (Period 1 Grade)", "G2 (Period 2 Grade)"
        ],
        "Qualitative (Nominal)": [
            "school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob", 
            "reason", "guardian", "schoolsup", "famsup", "paid", "activities", 
            "nursery", "higher", "internet", "romantic"
        ],
        "Qualitative (Ordinal)": [
            "Medu (Mother education: 0-4)", "Fedu (Father education: 0-4)",
            "traveltime (1-4)", "famrel (1-5)", "freetime (1-5)", 
            "goout (1-5)", "Dalc (1-5)", "Walc (1-5)", "health (1-5)"
        ]
    }

    for category, features in taxonomy.items():
        print(f"[{category}] ({len(features)} variables):")
        print(f"  {', '.join(features)}")
    print("-" * 70)


def compute_statistical_theory(df: pd.DataFrame, numerical_cols=None):
    """
    Calculates fundamental statistical measures:
    - Mean
    - Median
    - Mode
    - Variance
    - Standard Deviation
    - Range (Max - Min)
    """
    if numerical_cols is None:
        numerical_cols = ['age', 'studytime', 'absences', 'G1', 'G2', 'G3']

    print("\n" + "=" * 70)
    print("MODULE I: STATISTICAL THEORY AND DESCRIPTIVE MEASURES")
    print("=" * 70)

    stats_records = []
    for col in numerical_cols:
        series = df[col].dropna()
        mean_val = series.mean()
        median_val = series.median()
        mode_series = series.mode()
        mode_val = mode_series.iloc[0] if not mode_series.empty else np.nan
        var_val = series.var()
        std_val = series.std()
        range_val = series.max() - series.min()
        iqr_val = series.quantile(0.75) - series.quantile(0.25)

        stats_records.append({
            "Feature": col,
            "Mean": round(mean_val, 2),
            "Median": round(median_val, 2),
            "Mode": round(mode_val, 2),
            "Range": round(range_val, 2),
            "Variance": round(var_val, 2),
            "Std Dev": round(std_val, 2),
            "IQR": round(iqr_val, 2)
        })

    stats_df = pd.DataFrame(stats_records)
    print(stats_df.to_string(index=False))
    print("=" * 70)
    return stats_df


if __name__ == "__main__":
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "student_data.csv")
    df = pd.read_csv(data_path)
    print_learning_paradigms()
    classify_features(df)
    compute_statistical_theory(df)
