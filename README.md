# Student Performance Predictor (Statistical Machine Learning)

An end-to-end Python implementation for predicting student academic performance, mapped to **Module I** and **Module II** of the **Statistical Machine Learning (SML)** syllabus.

---

## 👩‍🏫 Teacher Portal & Batch Marks Evaluator (New Feature)
The application includes a specialized **Faculty & Teacher Portal** allowing teachers to:
1. **Log in securely** with faculty credentials (Demo: `teacher@school.edu` / `admin123`).
2. **Download CSV Templates** with predefined academic schema.
3. **Upload Class Marksheet CSVs** containing whole sections/classes.
4. **Automated Batch Predictions**: Feeds each student through the Multilinear Regression pipeline to calculate predicted Final Score ($G_3$), percentage, and letter grade (A/B/C/D/F).
5. **Academic Risk Detection**: Flags at-risk students ($G_3 < 10/20$) with urgent interventions (e.g. attendance counseling, remedial tutoring).
6. **Class-Level Analytics**: Class average, pass rate %, distinction count, and distribution bar charts.
7. **Export Evaluated Reports**: Download evaluated CSV with final scores and personalized recommendations.

---

## 👨‍🎓 Student Portal (New Feature)
Students can log in to view their personalized academic scorecard:
* **Student Login Credentials**:
  * **Roll Number**: Any student roll number (e.g. `101`, `104`, `105`) or Email: `student@school.edu`
  * **Password**: `student123`
* **Features for Students**:
  * **Personalized Scorecard**: Midterm 1 ($G_1$), Midterm 2 ($G_2$), Weekly Study Hours, Absences.
  * **Predicted Final Grade ($G_3$)**: Instant prediction with Grade letter (`A`, `B`, `C`, `F`) and percentage.
  * **Faculty & Academic Feedback**: Targeted advice on study routine and attendance.
  * **Interactive Grade Improvement Simulator**: Test how increasing study hours or reducing absences boosts their final score!

---

## 📌 Project Architecture & Syllabus Alignment

### Module I: Statistical Foundations & Exploratory Data Analysis
1. **Statistical Machine Learning & Types of Learning**:
   - Categorized as **Supervised Learning** because the model learns from historical records with ground truth target labels ($G_3$, continuous final score).
2. **Data Understanding & Taxonomy**:
   - Structured tabular dataset with 33 variables.
   - Categorization into **Quantitative** (Continuous/Discrete: `age`, `studytime`, `failures`, `absences`, `G1`, `G2`, `G3`) vs **Qualitative** (Nominal: `school`, `sex`, `address`, `internet`, etc.; Ordinal: `Medu`, `Fedu`, `traveltime`, etc.).
3. **Statistical Theory & Measures**:
   - Mean, Median, Mode, Variance, Standard Deviation, Range, and Interquartile Range (IQR).
4. **Exploratory Data Analysis (EDA) with Matplotlib & Seaborn**:
   - Target distribution analysis (`eda_target_distribution.png`).
   - Bivariate relationship plots: Study time vs Score, Failures vs Score, Absences vs Score, Prior Grade vs Score (`eda_bivariate_relationships.png`).
   - Feature correlation matrix heatmap (`eda_correlation_heatmap.png`).

---

### Module II: Data Pre-processing, Regression Modeling & Metrics
1. **Need & Phases of Data Pre-processing**:
   - Cleaning, deduplication, imputation, outlier mitigation, encoding, and scaling.
2. **Handling Duplication**:
   - Duplicate identification and removal using `drop_duplicates()`.
3. **Handling Missing Values**:
   - Numerical feature imputation with **Median** (robust against skewness).
   - Categorical feature imputation with **Mode** (most frequent category).
4. **Outlier Detection Approaches**:
   - **IQR Method**: $Q_1 - 1.5 \times \text{IQR}$ to $Q_3 + 1.5 \times \text{IQR}$.
   - **Z-Score Method**: Flagging data points where $|z| > 3$.
   - Outlier capping (Winsorization) on `absences` (`outlier_detection_iqr.png`).
5. **Handling Categorical Data**:
   - **Label Encoding**: Retains natural ordering for ordinal features (`Medu`, `Fedu`).
   - **One-Hot Encoding**: Applied to nominal variables with `drop_first=True` to explicitly prevent the **Dummy Variable Trap** (multicollinearity).
6. **Feature Scaling**:
   - Comparison of **Standardization** (`StandardScaler`: zero mean, unit variance) vs **Normalization** (`MinMaxScaler`: $[0, 1]$ interval).
7. **Dataset Splitting**:
   - 80% Training / 20% Testing split using `train_test_split(random_state=42)`.
8. **Regression Models for Data Analysis**:
   - **Simple Linear Regression**: Fitting single dominant predictor ($G_2$ or `studytime`) $\rightarrow \hat{y} = \beta_0 + \beta_1 x$.
   - **Multilinear Regression**: Multivariate ordinary least squares $\rightarrow \hat{y} = \mathbf{X}\boldsymbol{\beta}$.
   - **Polynomial Regression**: Quadratic feature transformation ($\text{degree}=2$) capturing non-linear interactions.
9. **Performance Metrics**:
   - Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and Coefficient of Determination ($R^2$ Score).
   - Residual analysis checking homoscedasticity and error normality (`regression_residual_diagnostics.png`).

---

## 🚀 How to Run the Project

### Prerequisites
Make sure Python 3.9+ is installed.

```bash
# Install dependencies
py -m pip install -r requirements.txt

# Run the master pipeline
py main.py
```

All charts and visual outputs are automatically exported to the `outputs/` directory.

---

## 📊 Mathematical Formulations Checklist

1. **Mean**: $\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$
2. **Variance & Standard Deviation**: $s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2, \quad s = \sqrt{s^2}$
3. **Min-Max Normalization**: $x_{\text{norm}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$
4. **Standardization ($Z$-Score)**: $z = \frac{x - \mu}{\sigma}$
5. **Mean Absolute Error (MAE)**: $\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$
6. **Mean Squared Error (MSE)**: $\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$
7. **Root Mean Squared Error (RMSE)**: $\text{RMSE} = \sqrt{\text{MSE}}$
8. **$R^2$ Score**: $R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$

---

## 🎓 Viva Questions & Answers

1. **What is the Dummy Variable Trap, and why do we drop one dummy column?**
   * *Answer*: If a categorical attribute has $k$ categories and we create $k$ binary indicators, the sum of these columns is identically equal to 1. This creates an exact linear relationship with the intercept term (perfect multicollinearity), causing $(\mathbf{X}^T\mathbf{X})$ to be singular (non-invertible). Dropping one dummy (`drop_first=True`) resolves this.
2. **Why evaluate both MAE and RMSE?**
   * *Answer*: MAE penalizes all errors linearly, giving an intuitive measure of average error. RMSE squares errors before averaging, penalizing large deviations much more heavily. If RMSE is substantially higher than MAE, it indicates the presence of large prediction errors.
3. **When does Polynomial Regression overfit?**
   * *Answer*: When the polynomial degree $d$ is too high, the model fits random noise in the training set rather than the underlying trend (high variance), causing the training error to approach zero while the test MSE explodes.
