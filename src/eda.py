"""
Module I: Exploratory Data Analysis (EDA) using Matplotlib and Seaborn
- Univariate distribution analysis
- Bivariate scatter and box plots
- Multivariate correlation heatmaps
"""

import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless saving
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def perform_eda(df: pd.DataFrame, output_dir: str):
    """
    Generates and saves visual EDA figures demonstrating all syllabus requirements.
    """
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted")
    
    print("\n" + "=" * 70)
    print("MODULE I: EXPLORATORY DATA ANALYSIS (MATPLOTLIB & SEABORN)")
    print("=" * 70)

    # 1. Target Variable Distribution (Univariate Analysis)
    plt.figure(figsize=(8, 5))
    sns.histplot(df['G3'].dropna(), kde=True, color="#2b5c8f", bins=20)
    plt.title("Distribution of Student Final Exam Score (G3)", fontsize=13, fontweight='bold')
    plt.xlabel("Final Grade (G3) [Scale: 0 - 20]", fontsize=11)
    plt.ylabel("Frequency (Student Count)", fontsize=11)
    plt.axvline(df['G3'].mean(), color='crimson', linestyle='--', label=f"Mean: {df['G3'].mean():.2f}")
    plt.axvline(df['G3'].median(), color='darkgreen', linestyle=':', label=f"Median: {df['G3'].median():.2f}")
    plt.legend()
    dist_path = os.path.join(output_dir, "eda_target_distribution.png")
    plt.tight_layout()
    plt.savefig(dist_path, dpi=300)
    plt.close()
    print(f"[Saved] Target Distribution Plot -> {dist_path}")

    # 2. Bivariate Relationships (Scatter & Boxplots)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # A: Study Time vs Final Grade
    sns.boxplot(ax=axes[0, 0], data=df, x='studytime', y='G3', hue='studytime', palette='Blues', legend=False)
    axes[0, 0].set_title("Study Time Category (1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h) vs G3", fontweight='bold')
    axes[0, 0].set_xlabel("Weekly Study Time Level")
    axes[0, 0].set_ylabel("Final Grade (G3)")

    # B: Past Failures vs Final Grade
    sns.boxplot(ax=axes[0, 1], data=df, x='failures', y='G3', hue='failures', palette='Reds_r', legend=False)
    axes[0, 1].set_title("Past Class Failures vs G3", fontweight='bold')
    axes[0, 1].set_xlabel("Number of Past Failures")
    axes[0, 1].set_ylabel("Final Grade (G3)")

    # C: Absences vs Final Grade (Scatter with trendline)
    sns.regplot(ax=axes[1, 0], data=df, x='absences', y='G3',
                scatter_kws={'alpha': 0.6, 'color': '#1f77b4'}, line_kws={'color': 'red'})
    axes[1, 0].set_title("School Absences vs Final Grade", fontweight='bold')
    axes[1, 0].set_xlabel("Number of Absences")
    axes[1, 0].set_ylabel("Final Grade (G3)")

    # D: Prior Period Grade (G2) vs Final Grade (G3)
    sns.regplot(ax=axes[1, 1], data=df, x='G2', y='G3',
                scatter_kws={'alpha': 0.6, 'color': '#2ca02c'}, line_kws={'color': 'darkgreen'})
    axes[1, 1].set_title("Period 2 Exam Score (G2) vs Final Grade (G3)", fontweight='bold')
    axes[1, 1].set_xlabel("Period 2 Grade (G2)")
    axes[1, 1].set_ylabel("Final Grade (G3)")

    bivar_path = os.path.join(output_dir, "eda_bivariate_relationships.png")
    plt.tight_layout()
    plt.savefig(bivar_path, dpi=300)
    plt.close()
    print(f"[Saved] Bivariate Relationships Plot -> {bivar_path}")

    # 3. Correlation Heatmap (Multivariate Analysis)
    numerical_cols = ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
                      'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3']
    corr_matrix = df[numerical_cols].corr()

    plt.figure(figsize=(12, 9))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='vlag', center=0, square=True, linewidths=0.5)
    plt.title("Correlation Matrix of Numerical Features (Seaborn Heatmap)", fontsize=14, fontweight='bold')
    corr_path = os.path.join(output_dir, "eda_correlation_heatmap.png")
    plt.tight_layout()
    plt.savefig(corr_path, dpi=300)
    plt.close()
    print(f"[Saved] Correlation Heatmap -> {corr_path}")
    print("-" * 70)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "data", "student_data.csv")
    out_dir = os.path.join(base_dir, "outputs")
    df = pd.read_csv(data_file)
    perform_eda(df, out_dir)
