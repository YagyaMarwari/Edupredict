import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "student_data.csv")
DATA_PATH = DEFAULT_PATH
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
SHOW_PLOTS = False


def load_dataset(file_path):
    print("=" * 75)
    print("STAGE 1: DATA INGESTION & DATASET OVERVIEW")
    print("=" * 75)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset not found at: {file_path}\n"
            f"Please update the DATA_PATH variable at the top of this script."
        )
    
    df = pd.read_csv(file_path)
    print(f"Dataset successfully loaded from: {file_path}")
    print(f"Total Student Records: {df.shape[0]}")
    print(f"Total Attribute Columns: {df.shape[1]}")
    print("-" * 75)
    print("First 5 Sample Records:")
    print(df.head(5).to_string())
    print("=" * 75 + "\n")
    return df


def compute_statistical_foundations(df):
    print("=" * 75)
    print("STAGE 2: STATISTICAL MEASURES (CENTRAL TENDENCY & DISPERSION)")
    print("=" * 75)
    
    num_cols = ["age", "studytime", "failures", "absences", "G1", "G2", "G3"]
    available_cols = [c for c in num_cols if c in df.columns]
    
    stats = []
    for col in available_cols:
        s = df[col].dropna()
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        stats.append({
            "Feature": col,
            "Mean": round(float(s.mean()), 2),
            "Median": round(float(s.median()), 2),
            "Mode": round(float(s.mode().iloc[0]), 2),
            "Std Dev": round(float(s.std()), 2),
            "Variance": round(float(s.var()), 2),
            "IQR": round(float(q3 - q1), 2),
            "Min": round(float(s.min()), 2),
            "Max": round(float(s.max()), 2),
        })
    
    stats_df = pd.DataFrame(stats)
    print(stats_df.to_string(index=False))
    print("=" * 75 + "\n")
    return stats_df


def perform_exploratory_analysis(df, output_dir):
    print("=" * 75)
    print("STAGE 3: EXPLORATORY DATA ANALYSIS (EDA) & VISUALIZATION")
    print("=" * 75)
    
    target_col = "G3"
    
    if target_col in df.columns:
        plt.figure(figsize=(8, 4.5))
        sns.histplot(df[target_col].dropna(), kde=True, color="#2563eb", bins=20)
        plt.title("Distribution of Student Final Exam Scores (Target: G3)", fontweight="bold")
        plt.xlabel("Final Score (0 - 20 Scale)")
        plt.ylabel("Student Count")
        plt.tight_layout()
        chart_path = os.path.join(output_dir, "eda_target_distribution.png")
        plt.savefig(chart_path, dpi=200)
        if SHOW_PLOTS:
            plt.show()
        plt.close()
        print(f"[Chart Saved] Final Grade Distribution -> {chart_path}")
    
    num_cols = [c for c in ["age", "studytime", "failures", "absences", "G1", "G2", "G3"] if c in df.columns]
    if len(num_cols) > 1:
        plt.figure(figsize=(8, 6))
        sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Feature Correlation Heatmap", fontweight="bold")
        plt.tight_layout()
        chart_path = os.path.join(output_dir, "eda_correlation_heatmap.png")
        plt.savefig(chart_path, dpi=200)
        if SHOW_PLOTS:
            plt.show()
        plt.close()
        print(f"[Chart Saved] Correlation Heatmap -> {chart_path}")
    
    print("=" * 75 + "\n")


def run_data_preprocessing(df):
    print("=" * 75)
    print("STAGE 4: DATA PREPROCESSING PIPELINE")
    print("=" * 75)
    
    initial_count = len(df)
    df_clean = df.drop_duplicates().copy()
    print(f"Duplicate records removed: {initial_count - len(df_clean)}")
    
    for col in ["studytime", "absences", "G1", "G2"]:
        if col in df_clean.columns and df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            
    for col in df_clean.select_dtypes(include=["object", "string"]).columns:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
            
    print(f"Remaining Missing Values: {df_clean.isnull().sum().sum()}")
    
    if "absences" in df_clean.columns:
        q1 = df_clean["absences"].quantile(0.25)
        q3 = df_clean["absences"].quantile(0.75)
        iqr = q3 - q1
        lower_bound = max(0, q1 - 1.5 * iqr)
        upper_bound = q3 + 1.5 * iqr
        df_clean["absences"] = np.clip(df_clean["absences"], lower_bound, upper_bound)
        print(f"Absences capped within IQR interval: [{lower_bound:.1f}, {upper_bound:.1f}]")
        
    cat_cols = df_clean.select_dtypes(include=["object", "string"]).columns.tolist()
    if cat_cols:
        df_encoded = pd.get_dummies(df_clean, columns=cat_cols, drop_first=True, dtype=int)
        print(f"One-Hot Encoding applied (drop_first=True to avoid dummy trap).")
        print(f"Encoded Dataset Shape: {df_encoded.shape[0]} samples, {df_encoded.shape[1]} features")
    else:
        df_encoded = df_clean
        
    print("=" * 75 + "\n")
    return df_encoded


def train_and_evaluate_models(df_encoded, output_dir=OUTPUT_DIR):
    print("=" * 75)
    print("STAGE 5: MODEL TRAINING, TESTING & PERFORMANCE EVALUATION")
    print("=" * 75)
    
    target_col = "G3"
    X = df_encoded.drop(columns=[target_col])
    y = df_encoded[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train/Test Partition: Train Set = {len(X_train)} samples, Test Set = {len(X_test)} samples")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    pred_feature = "G2" if "G2" in X_train.columns else X_train.columns[0]
    m1 = LinearRegression()
    m1.fit(X_train[[pred_feature]], y_train)
    y_pred_m1 = m1.predict(X_test[[pred_feature]])
    
    m2 = LinearRegression()
    m2.fit(X_train_scaled, y_train)
    y_pred_m2 = m2.predict(X_test_scaled)
    
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_train_poly = poly.fit_transform(X_train_scaled)
    X_test_poly = poly.transform(X_test_scaled)
    
    m3 = Ridge(alpha=100.0)
    m3.fit(X_train_poly, y_train)
    y_pred_m3 = m3.predict(X_test_poly)
    
    def get_metrics(name, y_true, y_pred):
        return {
            "Model Name": name,
            "MAE": round(float(mean_absolute_error(y_true, y_pred)), 3),
            "MSE": round(float(mean_squared_error(y_true, y_pred)), 3),
            "RMSE": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 3),
            "R2 Score": round(float(r2_score(y_true, y_pred)), 4)
        }
        
    eval_results = pd.DataFrame([
        get_metrics(f"Simple Linear ({pred_feature})", y_test, y_pred_m1),
        get_metrics("Multiple Linear Regression", y_test, y_pred_m2),
        get_metrics("Polynomial Regression (Deg 2)", y_test, y_pred_m3)
    ])
    
    print("\nMODEL BENCHMARK COMPARISON TABLE:")
    print(eval_results.to_string(index=False))
    
    if output_dir:
        plt.figure(figsize=(10, 4.5))
        plt.subplot(1, 2, 1)
        sns.barplot(x="Model Name", y="R2 Score", data=eval_results, hue="Model Name", palette="Blues_r", legend=False)
        plt.title("Model R2 Score Benchmark", fontweight="bold")
        plt.xticks(rotation=20, ha="right")
        plt.ylim(0, 1.0)
        
        plt.subplot(1, 2, 2)
        plt.scatter(y_test, y_pred_m2, color="#2563eb", alpha=0.7, edgecolors="k")
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
        plt.title("Multiple Linear: Actual vs Predicted", fontweight="bold")
        plt.xlabel("Actual G3 Score")
        plt.ylabel("Predicted G3 Score")
        plt.tight_layout()
        chart_path = os.path.join(output_dir, "model_benchmark_comparison.png")
        plt.savefig(chart_path, dpi=200)
        if SHOW_PLOTS:
            plt.show()
        plt.close()
        print(f"[Chart Saved] Model Evaluation Visual -> {chart_path}")
        
    print("=" * 75 + "\n")
    return eval_results


if __name__ == "__main__":
    print("\nStarting Student Performance Predictor Pipeline...")
    
    dataset = load_dataset(DATA_PATH)
    compute_statistical_foundations(dataset)
    perform_exploratory_analysis(dataset, OUTPUT_DIR)
    processed_df = run_data_preprocessing(dataset)
    train_and_evaluate_models(processed_df)
    
    print("All pipeline stages completed successfully!")
