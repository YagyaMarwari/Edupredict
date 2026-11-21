"""
Module II: Regression Models for Data Analysis (SML Syllabus)
- Simple Linear Regression (Baseline)
- Multilinear Regression (Ordinary Least Squares - OLS)
- Ridge Regression (L2 Regularization / Tikhonov)
- Lasso Regression (L1 Regularization / Sparse Feature Selection)
- Elastic Net Regression (Hybrid L1 + L2 Regularization)
- Polynomial Regression (Degree 2 with Non-Linear Interactions)
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures


def train_simple_linear_regression(X_train: pd.DataFrame, X_test: pd.DataFrame, 
                                   y_train: pd.Series, y_test: pd.Series,
                                   feature_name='G2'):
    """
    Fits Simple Linear Regression: y = beta_0 + beta_1 * x
    """
    print("\n" + "=" * 70)
    print("MODEL 1: SIMPLE LINEAR REGRESSION")
    print("=" * 70)
    
    # Extract single predictor
    X_train_single = X_train[[feature_name]].values
    X_test_single = X_test[[feature_name]].values

    model = LinearRegression()
    model.fit(X_train_single, y_train)

    y_train_pred = model.predict(X_train_single)
    y_test_pred = model.predict(X_test_single)

    beta_0 = model.intercept_
    beta_1 = model.coef_[0]

    print(f"Predictor Feature: '{feature_name}'")
    print(f"Regression Equation: G3_hat = {beta_0:.4f} + ({beta_1:.4f} * {feature_name})")
    print(f"Interpretation: For every 1 unit increase in {feature_name}, final score changes by {beta_1:.4f} points.")

    return {
        "model_name": f"Simple Linear Regression ({feature_name})",
        "model": model,
        "y_train_pred": y_train_pred,
        "y_test_pred": y_test_pred,
        "X_test_input": X_test_single,
        "feature_name": feature_name
    }


def train_multilinear_regression(X_train_scaled, X_test_scaled, 
                                 y_train: pd.Series, y_test: pd.Series,
                                 feature_names: list):
    """
    Fits Multilinear Regression: y = beta_0 + beta_1*x1 + ... + beta_p*xp
    """
    print("\n" + "=" * 70)
    print("MODEL 2: MULTILINEAR REGRESSION")
    print("=" * 70)

    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)

    # Feature importance via coefficients
    coef_series = pd.Series(model.coef_, index=feature_names)
    top_positive = coef_series.nlargest(3)
    top_negative = coef_series.nsmallest(3)

    print(f"Number of Input Predictors: {X_train_scaled.shape[1]}")
    print(f"Intercept (beta_0): {model.intercept_:.4f}")
    print("Top Positive Drivers of Performance:")
    for feat, coef in top_positive.items():
        print(f"  + {feat}: {coef:.4f}")
    print("Top Negative Drivers of Performance:")
    for feat, coef in top_negative.items():
        print(f"  - {feat}: {coef:.4f}")

    return {
        "model_name": "Multilinear Regression",
        "model": model,
        "y_train_pred": y_train_pred,
        "y_test_pred": y_test_pred,
        "coefficients": coef_series
    }


def train_ridge_regression(X_train_scaled, X_test_scaled,
                           y_train: pd.Series, y_test: pd.Series,
                           feature_names: list, alpha=1.0):
    """
    Fits Ridge Regression (L2 Regularization):
    Minimizes: ||y - X*beta||^2 + alpha * ||beta||_2^2
    Mitigates multicollinearity by shrinking large unstable coefficients.
    """
    print("\n" + "=" * 70)
    print(f"MODEL 3: RIDGE REGRESSION (L2 REGULARIZATION, alpha={alpha})")
    print("=" * 70)

    model = Ridge(alpha=alpha, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    coef_series = pd.Series(model.coef_, index=feature_names)

    return {
        "model_name": f"Ridge Regression (L2, alpha={alpha})",
        "model": model,
        "alpha": alpha,
        "y_train_pred": y_train_pred,
        "y_test_pred": y_test_pred,
        "coefficients": coef_series
    }


def train_lasso_regression(X_train_scaled, X_test_scaled,
                           y_train: pd.Series, y_test: pd.Series,
                           feature_names: list, alpha=0.05):
    """
    Fits Lasso Regression (L1 Regularization):
    Minimizes: (1 / 2n) * ||y - X*beta||^2 + alpha * ||beta||_1
    Enforces sparsity by shrinking non-essential feature weights to exactly 0.
    """
    print("\n" + "=" * 70)
    print(f"MODEL 4: LASSO REGRESSION (L1 REGULARIZATION, alpha={alpha})")
    print("=" * 70)

    model = Lasso(alpha=alpha, random_state=42, max_iter=2000)
    model.fit(X_train_scaled, y_train)

    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    coef_series = pd.Series(model.coef_, index=feature_names)

    retained_feats = coef_series[coef_series.abs() > 1e-4]
    print(f"Lasso Sparse Feature Selection: {len(retained_feats)} / {len(feature_names)} features active.")

    return {
        "model_name": f"Lasso Regression (L1, alpha={alpha})",
        "model": model,
        "alpha": alpha,
        "y_train_pred": y_train_pred,
        "y_test_pred": y_test_pred,
        "coefficients": coef_series,
        "active_features_count": len(retained_feats)
    }


def train_elastic_net_regression(X_train_scaled, X_test_scaled,
                                 y_train: pd.Series, y_test: pd.Series,
                                 feature_names: list, alpha=0.05, l1_ratio=0.5):
    """
    Fits Elastic Net Regression (Hybrid L1 + L2 Regularization):
    Blends L1 sparsity penalty and L2 grouping stability.
    """
    print("\n" + "=" * 70)
    print(f"MODEL 5: ELASTIC NET REGRESSION (alpha={alpha}, l1_ratio={l1_ratio})")
    print("=" * 70)

    model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42, max_iter=2000)
    model.fit(X_train_scaled, y_train)

    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    coef_series = pd.Series(model.coef_, index=feature_names)

    return {
        "model_name": f"Elastic Net Regression (alpha={alpha}, l1_ratio={l1_ratio})",
        "model": model,
        "alpha": alpha,
        "l1_ratio": l1_ratio,
        "y_train_pred": y_train_pred,
        "y_test_pred": y_test_pred,
        "coefficients": coef_series
    }



def train_polynomial_regression(X_train_scaled, X_test_scaled,
                                y_train: pd.Series, y_test: pd.Series,
                                feature_names: list = None,
                                degree=2):
    """
    Fits Polynomial Regression with Quadratic and Interaction terms.
    Focuses on primary academic drivers (G2, G1, studytime, absences, failures)
    to prevent dimension explosion while capturing synergistic non-linearities.
    """
    print("\n" + "=" * 70)
    print(f"MODEL 6: POLYNOMIAL REGRESSION (DEGREE = {degree} WITH INTERACTIONS)")
    print("=" * 70)

    key_indices = None
    if feature_names:
        core_cols = ["G2", "G1", "studytime", "absences", "failures"]
        key_indices = [feature_names.index(c) for c in core_cols if c in feature_names]
        X_tr = X_train_scaled[:, key_indices]
        X_te = X_test_scaled[:, key_indices]
    else:
        X_tr = X_train_scaled
        X_te = X_test_scaled

    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_poly = poly.fit_transform(X_tr)
    X_test_poly = poly.transform(X_te)

    print(f"Input Predictor Dimension:    {X_tr.shape[1]}")
    print(f"Polynomial Feature Dimension: {X_train_poly.shape[1]}")

    # Regularized fit to prevent overfitting (Bias-Variance tradeoff)
    model = Ridge(alpha=5.0, random_state=42)
    model.fit(X_train_poly, y_train)

    y_train_pred = model.predict(X_train_poly)
    y_test_pred = model.predict(X_test_poly)

    return {
        "model_name": f"Polynomial Regression (Degree {degree})",
        "model": model,
        "poly_transformer": poly,
        "key_indices": key_indices,
        "y_train_pred": y_train_pred,
        "y_test_pred": y_test_pred
    }
