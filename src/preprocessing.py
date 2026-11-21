"""
Module II: Data Pre-processing Pipeline
- Need & Phases of Pre-processing
- Handling Duplication of Data
- Handling Missing Values (Imputation)
- Outlier Detection (IQR & Z-Score)
- Handling Categorical Data (Label Encoding & One-Hot Encoding + Dummy Variable Trap)
- Feature Scaling (Standardization vs Normalization)
- Dataset Splitting (Train/Test Split)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder


def print_preprocessing_theory():
    print("\n" + "=" * 70)
    print("MODULE II: DATA PRE-PROCESSING THEORY & PHASES")
    print("=" * 70)
    print("1. Need of Data Pre-processing:")
    print("   - Real-world data is noisy, incomplete, inconsistent, and unscaled.")
    print("   - Raw data leads to poor model convergence, biased coefficients, and high error.")
    print("2. Phases of Data Pre-processing:")
    print("   - Phase 1: Data Cleaning (Duplication removal, Missing value imputation)")
    print("   - Phase 2: Outlier Detection and Treatment")
    print("   - Phase 3: Categorical Encoding (Avoiding dummy variable trap)")
    print("   - Phase 4: Feature Scaling (Standardization & Normalization)")
    print("   - Phase 5: Train/Test Dataset Splitting")
    print("-" * 70)


def handle_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[Phase 1A: Handling Duplication of Data]")
    dup_count = df.duplicated().sum()
    print(f"  Detected duplicate rows: {dup_count}")
    df_cleaned = df.drop_duplicates().copy()
    print(f"  Rows before deduplication: {len(df)} | Rows after deduplication: {len(df_cleaned)}")
    return df_cleaned


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[Phase 1B: Handling Missing Values]")
    null_counts = df.isnull().sum()
    missing_cols = null_counts[null_counts > 0]
    
    if len(missing_cols) == 0:
        print("  No missing values found.")
        return df

    print("  Missing values detected:")
    for col, count in missing_cols.items():
        print(f"    - Column '{col}': {count} missing value(s)")

    df_imputed = df.copy()
    for col in missing_cols.index:
        if pd.api.types.is_numeric_dtype(df_imputed[col]):
            # Impute numerical features using Median (robust against skewness)
            median_val = df_imputed[col].median()
            df_imputed[col] = df_imputed[col].fillna(median_val)
            print(f"    -> Imputed numerical column '{col}' with Median: {median_val}")
        else:
            # Impute categorical features using Mode (most frequent category)
            mode_val = df_imputed[col].mode()[0]
            df_imputed[col] = df_imputed[col].fillna(mode_val)
            print(f"    -> Imputed categorical column '{col}' with Mode: '{mode_val}'")

    print(f"  Total remaining missing values: {df_imputed.isnull().sum().sum()}")
    return df_imputed


def detect_and_handle_outliers(df: pd.DataFrame, output_dir: str, target_col='absences') -> pd.DataFrame:
    print("\n[Phase 2: Outlier Detection Approaches]")
    df_treated = df.copy()
    series = df_treated[target_col]

    # Approach 1: Interquartile Range (IQR) Method
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    iqr_outliers = series[(series < lower_bound) | (series > upper_bound)]
    print(f"  Approach 1 - IQR Method on '{target_col}':")
    print(f"    Q1 = {q1:.1f}, Q3 = {q3:.1f}, IQR = {iqr:.1f}")
    print(f"    Valid Range: [{lower_bound:.1f}, {upper_bound:.1f}]")
    print(f"    Identified {len(iqr_outliers)} outlier(s) using IQR.")

    # Approach 2: Z-Score Method (|z| > 3)
    z_scores = np.abs((series - series.mean()) / series.std())
    z_outliers = series[z_scores > 3]
    print(f"  Approach 2 - Z-Score Method (|z| > 3) on '{target_col}':")
    print(f"    Identified {len(z_outliers)} extreme outlier(s) with |z| > 3.")

    # Visualizing before vs after capping
    os.makedirs(output_dir, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    sns.boxplot(ax=axes[0], y=series, color='#e74c3c')
    axes[0].set_title(f"Before Outlier Capping ({target_col})", fontweight='bold')

    # Outlier treatment: Capping at upper bound (Winsorization)
    df_treated[target_col] = np.clip(df_treated[target_col], lower_bound, upper_bound)

    sns.boxplot(ax=axes[1], y=df_treated[target_col], color='#2ecc71')
    axes[1].set_title(f"After IQR Capping ({target_col})", fontweight='bold')

    outlier_plot_path = os.path.join(output_dir, "outlier_detection_iqr.png")
    plt.tight_layout()
    plt.savefig(outlier_plot_path, dpi=300)
    plt.close()
    print(f"    [Saved] Outlier Comparison Plot -> {outlier_plot_path}")

    return df_treated


def handle_categorical_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[Phase 3: Handling Categorical Data & Dummy Variable Trap]")
    df_encoded = df.copy()

    # 1. Label Encoding for Ordinal features (where order matters)
    ordinal_cols = ['Medu', 'Fedu', 'traveltime', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health']
    print(f"  1. Label Encoding applied to ordinal features: {', '.join(ordinal_cols[:4])}...")
    # These are already encoded numerically from 0 to 4 or 1 to 5, preserving natural hierarchy.

    # 2. One-Hot Encoding for Nominal features with drop_first=True
    nominal_cols = [
        'school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob',
        'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities',
        'nursery', 'higher', 'internet', 'romantic'
    ]
    print(f"  2. One-Hot Encoding applied to nominal features ({len(nominal_cols)} features).")
    print("  * DUMMY VARIABLE TRAP PREVENTION:")
    print("    - When a feature has K categories, creating K dummy variables leads to multicollinearity")
    print("      because the Kth dummy can be perfectly predicted by the sum of the others.")
    print("    - By setting drop_first=True, we create K-1 dummy variables, preserving full information")
    print("      while avoiding singularity in the regression matrix (X^T * X).")

    df_encoded = pd.get_dummies(df_encoded, columns=nominal_cols, drop_first=True, dtype=int)
    print(f"    Shape after One-Hot Encoding: {df_encoded.shape}")
    return df_encoded


def demonstrate_feature_scaling(X_train: pd.DataFrame, X_test: pd.DataFrame):
    print("\n[Phase 4: Feature Scaling - Standardization vs Normalization]")
    print("  Comparison of Scaling Formulations:")
    print("  - Normalization (MinMaxScaler): x_norm = (x - min) / (max - min) -> Bounds values to [0, 1].")
    print("  - Standardization (StandardScaler): z = (x - mean) / std -> Centers data at mean 0, variance 1.")
    print("  Linear regression is more robust with Standardization because it preserves outlier distance ratios.")

    # Demonstration
    minmax = MinMaxScaler()
    X_train_minmax = minmax.fit_transform(X_train)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"  Sample Feature Scaled Stats (StandardScaler): Mean = {X_train_scaled.mean():.4f}, Std = {X_train_scaled.std():.4f}")
    return X_train_scaled, X_test_scaled, scaler


def split_data(df: pd.DataFrame, target_col='G3', test_size=0.2, random_state=42):
    print(f"\n[Phase 5: Splitting the Dataset (Train: {(1-test_size)*100:.0f}%, Test: {test_size*100:.0f}%)]")
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"  Training set size: {X_train.shape[0]} samples")
    print(f"  Testing set size:  {X_test.shape[0]} samples")
    print(f"  Feature count:     {X_train.shape[1]} predictors")
    return X_train, X_test, y_train, y_test


def run_preprocessing_pipeline(data_path: str, output_dir: str):
    print_preprocessing_theory()
    raw_df = pd.read_csv(data_path)
    df_dedup = handle_duplicates(raw_df)
    df_clean = handle_missing_values(df_dedup)
    df_no_outliers = detect_and_handle_outliers(df_clean, output_dir, target_col='absences')
    df_encoded = handle_categorical_data(df_no_outliers)
    X_train, X_test, y_train, y_test = split_data(df_encoded, target_col='G3', test_size=0.2)
    X_train_scaled, X_test_scaled, scaler = demonstrate_feature_scaling(X_train, X_test)
    
    return {
        "raw_df": raw_df,
        "clean_df": df_encoded,
        "X_train": X_train,
        "X_test": X_test,
        "X_train_scaled": X_train_scaled,
        "X_test_scaled": X_test_scaled,
        "y_train": y_train,
        "y_test": y_test,
        "scaler": scaler,
        "feature_names": X_train.columns.tolist()
    }
