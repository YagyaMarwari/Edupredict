"""
Module II: Regression Performance Metrics & Residual Diagnostics
- Mean Square Error (MSE)
- Root Mean Square Error (RMSE)
- Mean Absolute Error (MAE)
- R2_Score
- Residual Analysis & Comparison Visualizations
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def compute_metrics(y_true, y_pred):
    """
    Computes all standard regression performance metrics specified in Module II.
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    }


def compare_models(results_dict: dict):
    """
    Constructs a clear evaluation summary table across all models.
    """
    print("\n" + "=" * 70)
    print("MODULE II: REGRESSION PERFORMANCE METRICS COMPARISON")
    print("=" * 70)

    summary = []
    for name, res in results_dict.items():
        summary.append({
            "Model": name,
            "Train R2": round(res["train_metrics"]["R2"], 4),
            "Test R2": round(res["test_metrics"]["R2"], 4),
            "Test MAE": round(res["test_metrics"]["MAE"], 4),
            "Test MSE": round(res["test_metrics"]["MSE"], 4),
            "Test RMSE": round(res["test_metrics"]["RMSE"], 4),
        })

    summary_df = pd.DataFrame(summary)
    print(summary_df.to_string(index=False))
    print("=" * 70)
    return summary_df


def plot_model_evaluations(results_dict: dict, y_test: pd.Series, output_dir: str):
    """
    Generates actual vs predicted and residual diagnostic plots.
    """
    os.makedirs(output_dir, exist_ok=True)
    num_models = len(results_dict)
    fig, axes = plt.subplots(1, num_models, figsize=(6 * num_models, 5))
    if num_models == 1:
        axes = [axes]

    for idx, (name, res) in enumerate(results_dict.items()):
        y_pred = res["test_pred"]
        ax = axes[idx]
        ax.scatter(y_test, y_pred, alpha=0.6, color="#2980b9", edgecolors='k')
        
        # Perfect prediction line
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label="Ideal Line (y = y_hat)")
        
        ax.set_title(f"{name}\nR² = {res['test_metrics']['R2']:.3f} | RMSE = {res['test_metrics']['RMSE']:.2f}", fontweight='bold')
        ax.set_xlabel("Actual Exam Score (G3)")
        ax.set_ylabel("Predicted Exam Score (G3)")
        ax.legend(loc="upper left")

    plt_path = os.path.join(output_dir, "regression_comparison_predictions.png")
    plt.tight_layout()
    plt.savefig(plt_path, dpi=300)
    plt.close()
    print(f"[Saved] Actual vs Predicted Comparison -> {plt_path}")

    # Residual Diagnostics Plot for the Multilinear Regression model
    if "Multilinear Regression" in results_dict:
        y_pred = results_dict["Multilinear Regression"]["test_pred"]
        residuals = y_test.values - y_pred

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        # Residuals vs Predicted
        ax1.scatter(y_pred, residuals, alpha=0.6, color="#8e44ad")
        ax1.axhline(0, color='red', linestyle='--')
        ax1.set_title("Residuals vs Fitted Values (Homoscedasticity Check)", fontweight='bold')
        ax1.set_xlabel("Predicted G3 Score")
        ax1.set_ylabel("Residual (Actual - Predicted)")

        # Distribution of Residuals (Normality Check)
        sns.histplot(residuals, kde=True, ax=ax2, color="#16a085")
        ax2.set_title("Distribution of Residuals (Normality of Errors)", fontweight='bold')
        ax2.set_xlabel("Residual Value")

        res_path = os.path.join(output_dir, "regression_residual_diagnostics.png")
        plt.tight_layout()
        plt.savefig(res_path, dpi=300)
        plt.close()
        print(f"[Saved] Residual Diagnostics -> {res_path}")
