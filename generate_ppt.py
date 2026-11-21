import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 widescreen
    prs.slide_height = Inches(7.5)

    # Color Palette
    DARK_BLUE = RGBColor(15, 23, 42)      # #0F172A
    NAVY = RGBColor(30, 41, 59)           # #1E293B
    ACCENT_BLUE = RGBColor(37, 99, 235)   # #2563EB
    LIGHT_BG = RGBColor(248, 250, 252)    # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
    TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
    TEXT_DARK = RGBColor(15, 23, 42)      # #0F172A
    SUCCESS_GREEN = RGBColor(16, 185, 129)# #10B981

    blank_layout = prs.slide_layouts[6]

    def add_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = LIGHT_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="STATISTICAL MACHINE LEARNING (CSET211)"):
        # Top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(0.08), Inches(0.7))
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT_BLUE
        bar.line.fill.background()

        # Category
        tb_cat = slide.shapes.add_textbox(Inches(1.0), Inches(0.45), Inches(11.0), Inches(0.3))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        # Title
        tb = slide.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(11.0), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BLUE
    bg1.line.fill.background()

    # Title Card
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11.0), Inches(2.2))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "EduPredict: SML-Driven Student Grade & Risk Predictor"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "An End-to-End Regression Framework with Dynamic Headroom Calibration & Early At-Risk Intervention"
    p1_sub.font.size = Pt(18)
    p1_sub.font.color.rgb = RGBColor(147, 197, 253)
    p1_sub.space_before = Pt(12)

    # Info Box Card
    info_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.3), Inches(10.9), Inches(2.2))
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = NAVY
    info_card.line.color.rgb = ACCENT_BLUE
    info_card.line.width = Pt(1.5)

    tb_meta = s1.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(10.3), Inches(1.8))
    tf_meta = tb_meta.text_frame
    
    p_m1 = tf_meta.paragraphs[0]
    p_m1.text = "Candidate Name: Yagya Marwari  |  Enrollment / Roll No: S25CSEU0546"
    p_m1.font.size = Pt(16)
    p_m1.font.bold = True
    p_m1.font.color.rgb = RGBColor(255, 255, 255)

    p_m2 = tf_meta.add_paragraph()
    p_m2.text = "Course: CSET211 - Statistical Machine Learning (AI Core-1)  |  Semester: 3rd Sem (ODD 2026)"
    p_m2.font.size = Pt(14)
    p_m2.font.color.rgb = RGBColor(203, 213, 225)
    p_m2.space_before = Pt(8)

    p_m3 = tf_meta.add_paragraph()
    p_m3.text = "Department: School of Computer Science, Engineering & Technology, Bennett University"
    p_m3.font.size = Pt(14)
    p_m3.font.color.rgb = RGBColor(203, 213, 225)
    p_m3.space_before = Pt(6)

    p_m4 = tf_meta.add_paragraph()
    p_m4.text = "GitHub: https://github.com/YagyaMarwari/Edupredict"
    p_m4.font.size = Pt(13)
    p_m4.font.color.rgb = RGBColor(96, 165, 250)
    p_m4.space_before = Pt(6)

    # Helper function for 2-column cards
    def add_two_cards(slide, c1_title, c1_bullets, c2_title, c2_bullets, left_w=5.5, right_w=5.5):
        # Card 1
        card1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(left_w), Inches(5.4))
        card1.fill.solid()
        card1.fill.fore_color.rgb = CARD_BG
        card1.line.color.rgb = RGBColor(226, 232, 240)
        card1.line.width = Pt(1)

        tb1 = slide.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(left_w - 0.6), Inches(4.8))
        tf1 = tb1.text_frame
        tf1.word_wrap = True
        p1 = tf1.paragraphs[0]
        p1.text = c1_title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_BLUE

        for b in c1_bullets:
            p = tf1.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_DARK
            p.space_before = Pt(10)

        # Card 2
        card2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + left_w + 0.4), Inches(1.5), Inches(right_w), Inches(5.4))
        card2.fill.solid()
        card2.fill.fore_color.rgb = CARD_BG
        card2.line.color.rgb = RGBColor(226, 232, 240)
        card2.line.width = Pt(1)

        tb2 = slide.shapes.add_textbox(Inches(1.1 + left_w + 0.4), Inches(1.8), Inches(right_w - 0.6), Inches(4.8))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = c2_title
        p2.font.size = Pt(17)
        p2.font.bold = True
        p2.font.color.rgb = ACCENT_BLUE

        for b in c2_bullets:
            p = tf2.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_DARK
            p.space_before = Pt(10)

    # -------------------------------------------------------------------------
    # SLIDE 2: Problem Statement & Motivation
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Problem Statement & Educational Context")
    add_two_cards(s2, 
        "The Traditional Academic Bottleneck", [
            "Late Intervention Deficit: At-risk students are typically identified only after mid-term (G2) or final (G3) failure, leaving zero turnaround time.",
            "Subjective Evaluation: Faculty evaluations often fail to account for multi-variable interactions like commute time, study habits, and parental education.",
            "High Dropout & Repeat Rates: Cumulative backlog buildup leads to attrition in higher technical education.",
            "Lack of Automated Actionable Insights: Raw marks without predictive trajectory fail to inform parents, mentors, or academic advisors."
        ],
        "The EduPredict Proposed Solution", [
            "Early Predictive Warning Engine: Leverages statistical regression to forecast final grade (G3, 0-20 scale) before the semester closes.",
            "Automated Multi-Tier Risk Triage: Classifies cohorts into High Distinction (16-20), Safe Pass (12-15), Moderate Risk (10-11), and Critical At-Risk (<10).",
            "Personalized Remedial Guidance: Generates tailored weekly study-hour recommendations and mentor intervention protocols.",
            "End-to-End Practical System: Production-ready interactive web application with batch CSV roster analysis and exportable reports."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 3: Dataset Architecture & Statistical Overview
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "Dataset Description & Statistical Properties")
    add_two_cards(s3,
        "Dataset Specifications (UCI Machine Learning)", [
            "Cohort Size: 399 student academic instances with zero missing values after verification.",
            "Feature Space: 33 attributes spanning demographic, socio-economic, behavioral, and academic dimensions.",
            "Target Variable (G3): Final examination mark measured continuously on a standardized Portuguese 0–20 point scale.",
            "Temporal Milestones: G1 (First Period Assessment, 0-20), G2 (Second Period Assessment, 0-20), G3 (Final Exam Mark, 0-20).",
            "Socio-Demographic Factors: Medu, Fedu (parental education 0-4), traveltime, studytime (weekly hours), failures (prior class repeats)."
        ],
        "Statistical Distribution Summary (Module I)", [
            "Target Central Tendency: Mean Final Grade (G3) = 10.42 / 20, Median = 11.00.",
            "Target Dispersion: Standard Deviation = 4.58 marks; Interquartile Range (IQR) = 6.00 marks (Q1=8.0, Q3=14.0).",
            "Zero-Inflated Tail: 38 students scored G3 = 0 (representing total non-attendance or dropouts during finals).",
            "Correlation Hierarchy: Strongest positive predictors: G2 (r = +0.905), G1 (r = +0.801). Strongest negative predictor: Past Failures (r = -0.360).",
            "Behavioral Impact: Study time positively correlates with grades; weekend alcohol consumption and absences exhibit adverse effects."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 4: SML Syllabus Mapping & Curriculum Rigor
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "Curriculum Alignment: SML Modules I & II")
    add_two_cards(s4,
        "Module I: Statistical Data Understanding & EDA", [
            "Descriptive Analytics: Quantiles, variance, standard deviation, and skewness of academic performance metrics.",
            "Bivariate & Multivariate Association: Covariance matrices, Pearson linear correlation (r), and Spearman rank correlation.",
            "Exploratory Visualization: Seaborn KDE distribution curves, correlation heatmaps, pairplots, and violin distributions.",
            "Outlier Identification: Interquartile Range (IQR) statistical fence detection and student record sanity checks."
        ],
        "Module II: Regression & Regularization Theory", [
            "Ordinary Least Squares (OLS): Closed-form normal equations, Gauss-Markov assumptions, residual analysis.",
            "Ridge Regression (L2 Regularization): Shrinkage penalty addressing multicollinearity between G1 and G2.",
            "Lasso Regression (L1 Regularization): Geometric diamond constraint driving non-informative feature weights to exact zero.",
            "Elastic Net: Convex combination of L1 and L2 penalties for correlated grouping effect.",
            "Polynomial Regression: Degree-2 expansion capturing non-linear interactions between study time and prior grades."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 5: Exploratory Data Analysis & Diagnostic Heatmaps
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "Exploratory Data Analysis: Correlation & Target Analysis")
    
    # Left Card
    c_left = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.4))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = RGBColor(226, 232, 240)
    tb_l = s5.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(4.9), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_l = tf_l.paragraphs[0]
    p_l.text = "Key Analytical Findings"
    p_l.font.size = Pt(17)
    p_l.font.bold = True
    p_l.font.color.rgb = ACCENT_BLUE

    bullets_eda = [
        "Near-Collinear Predictors: G1 and G2 share r = 0.852 with each other, necessitating regularization to prevent variance inflation.",
        "Predictive Power of G2: With r = 0.905 to G3, second-period marks represent the strongest single predictor of final outcome.",
        "The 'Failure Trap': Prior class failures (failures >= 1) shift student median grade downward from 11.8 to 6.2 marks.",
        "Mother's Education (Medu): Higher maternal education level correlates with higher student study hours and higher retention.",
        "Absence Dynamics: High absence counts (>15) show a significant negative drag, but moderate absence (1-4) is benign."
    ]
    for b in bullets_eda:
        p = tf_l.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)

    # Right Card: embed image if exists
    img_path = r"C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor\outputs\eda_correlation_heatmap.png"
    if os.path.exists(img_path):
        s5.shapes.add_picture(img_path, Inches(6.7), Inches(1.5), Inches(5.8), Inches(5.4))

    # -------------------------------------------------------------------------
    # SLIDE 6: Data Preprocessing Pipeline & Dummy Variable Trap Mitigation
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "Data Preprocessing & Mathematical Hygiene")
    add_two_cards(s6,
        "Mitigating The Dummy Variable Trap", [
            "Categorical Encoding: Categorical attributes (e.g., sex, address, guardian, Mjob, higher) converted into binary dummy columns.",
            "The Multicollinearity Hazard: If a categorical feature has k levels, including all k dummies creates an exact linear combination with the intercept vector: sum(D_i) = 1.",
            "Singular Matrix Danger: In OLS, det(X^T X) = 0, causing matrix inversion to fail: beta = (X^T X)^(-1) X^T y becomes undefined.",
            "Rigorous Solution: Applied drop_first=True across all categorical encoders, guaranteeing k-1 degrees of freedom and full column rank."
        ],
        "Statistical Cleaning & Standardization", [
            "IQR Outlier Boundary: Identified outliers on continuous variables using [Q1 - 1.5*IQR, Q3 + 1.5*IQR]. Academic outliers were capped or retained with contextual validity.",
            "StandardScaler Feature Scaling: Continuous features scaled via Z-score transformation: z = (x - mu) / sigma.",
            "Penalty Equity: Zero-mean, unit-variance scaling ensures L1/L2 penalties penalize features equitably regardless of raw unit magnitude.",
            "Data Split Integrity: Stratified 80/20 train-test split applied with strict feature transformer fitting on training data only to prevent data leakage."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 7: Ordinary Least Squares (OLS) Regression
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "Model 1: Ordinary Least Squares (OLS)")
    add_two_cards(s7,
        "Mathematical Formulation & Derivation", [
            "Hypothesis Function: y_hat = beta_0 + beta_1*x_1 + ... + beta_p*x_p = X * beta.",
            "Cost Function (Residual Sum of Squares): J(beta) = (1 / 2n) * ||y - X*beta||_2^2.",
            "Normal Equations: Setting gradient nabla_beta J(beta) = 0 yields: X^T * (y - X*beta) = 0.",
            "Closed-Form Solution: beta_hat = (X^T * X)^(-1) * X^T * y.",
            "Gauss-Markov Theorem: Under homoscedasticity and zero error expectation, OLS is the Best Linear Unbiased Estimator (BLUE)."
        ],
        "Empirical Strengths & Multicollinearity Vulnerability", [
            "Direct Interpretability: Regression coefficients represent the exact marginal change in G3 per unit increase in each feature.",
            "Baseline Benchmark: Achieves R^2 = 0.831 on the test set, proving linear relationships dominate student performance.",
            "Multicollinearity Vulnerability: Because G1 and G2 are highly correlated (r=0.85), (X^T * X) exhibits high condition number.",
            "High Variance: Small perturbations in input data lead to large fluctuations in coefficient weights, justifying regularization."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 8: Ridge Regression (L2 Regularization)
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "Model 2: Ridge Regression (L2 Regularization)")
    add_two_cards(s8,
        "Mathematical Objective & Shrinkage", [
            "Regularized Cost Function: J_Ridge(beta) = (1 / 2n) * ||y - X*beta||_2^2 + lambda * ||beta||_2^2.",
            "L2 Norm Penalty: ||beta||_2^2 = sum(beta_j^2) for j = 1 to p.",
            "Analytical Solution: beta_hat_Ridge = (X^T * X + lambda * I)^(-1) * X^T * y.",
            "Conditioning the Inversion: Adding lambda * I guarantees (X^T * X + lambda * I) is strictly positive definite and invertible even under exact collinearity.",
            "Hyperparameter Lambda: Controlled via cross-validation (optimal lambda = 1.0)."
        ],
        "Geometric & Practical Insights", [
            "Spherical Constraint Geometry: In coefficient space, the loss contours intersect a hyperspherical ball constraint, shrinking weights proportionally.",
            "Variance Reduction: Sacrifices a small degree of bias to achieve a drastic reduction in estimator variance (Bias-Variance Tradeoff).",
            "Handling Collinear Grades: Prevents G1 and G2 from canceling each other out with unnaturally large opposing coefficients.",
            "Empirical Benchmark: Achieves test R^2 = 0.835, exhibiting superior stability over unregularized OLS."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 9: Lasso Regression (L1 Regularization) & Sparsity
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_background(s9)
    add_header(s9, "Model 3: Lasso Regression (L1 Regularization)")
    add_two_cards(s9,
        "Mathematical Objective & Coordinate Descent", [
            "Cost Function: J_Lasso(beta) = (1 / 2n) * ||y - X*beta||_2^2 + lambda * ||beta||_1.",
            "L1 Norm Penalty: ||beta||_1 = sum(|beta_j|) for j = 1 to p.",
            "Non-Differentiability at Origin: |beta_j| has no derivative at 0; solved via Coordinate Descent using the soft-thresholding operator: S(z, lambda) = sign(z) * max(0, |z| - lambda).",
            "Automatic Feature Selection: Shrinks non-essential behavioral coefficients to EXACT ZERO.",
            "Sparse Model Representation: Eliminates noise features while retaining high-impact academic signals."
        ],
        "Geometric Sparsity & Clinical Findings", [
            "Diamond Constraint Corners: The sharp corners of the L1 ball lie on the coordinate axes, causing contours to hit zero coordinates.",
            "Sparsity Outcome in EduPredict: Zeroes out peripheral variables (famsup, romantic status) while heavily preserving G2, G1, and failures.",
            "Parsimonious Model: Minimizes overfitting and yields high faculty interpretability.",
            "Empirical Result: Test R^2 = 0.829 with 40% fewer active predictors, demonstrating high data efficiency."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 10: Elastic Net & Polynomial Regression
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_background(s10)
    add_header(s10, "Models 4 & 5: Elastic Net & Polynomial Regression")
    add_two_cards(s10,
        "Model 4: Elastic Net (Convex Compromise)", [
            "Combined Penalty: J_EN(beta) = (1/2n)*||y - X*beta||_2^2 + lambda1*||beta||_1 + lambda2*||beta||_2^2.",
            "L1 Ratio Parameter: alpha = lambda1 / (lambda1 + lambda2). Tuned to alpha = 0.5 for balanced sparsity and shrinkage.",
            "Overcoming Lasso Limitation: When features are highly correlated (G1 and G2), Lasso selects one arbitrarily. Elastic Net includes both via the grouping effect.",
            "Robust Prediction: Test R^2 = 0.834, combining the stability of Ridge with the sparsity of Lasso."
        ],
        "Model 5: Polynomial Regression (Degree 2)", [
            "Feature Expansion: phi(X) = [1, x_1, x_2, x_1^2, x_2^2, x_1*x_2, ...].",
            "Interaction Modeling: Captures synergistic non-linear dynamics, e.g., high study time combined with low absences.",
            "Diminishing Returns: Models plateau effects where study time yields decreasing marginal grade returns.",
            "Curse of Dimensionality: Feature space expands from 33 to over 500 terms, necessitating regularization to curb high variance."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 11: Benchmark Comparison & Empirical Results
    # -------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_background(s11)
    add_header(s11, "Empirical Benchmark Comparison & Residual Diagnostics")
    
    # Left Card: Metrics Table
    c_l11 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.4))
    c_l11.fill.solid()
    c_l11.fill.fore_color.rgb = CARD_BG
    c_l11.line.color.rgb = RGBColor(226, 232, 240)
    tb_11 = s11.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.1), Inches(5.0))
    tf_11 = tb_11.text_frame
    tf_11.word_wrap = True
    p_11 = tf_11.paragraphs[0]
    p_11.text = "Model Evaluation Matrix"
    p_11.font.size = Pt(17)
    p_11.font.bold = True
    p_11.font.color.rgb = ACCENT_BLUE

    metrics = [
        "Ridge Regression (Champion): R^2 = 0.835 | MAE = 1.14 marks | RMSE = 1.84 marks",
        "Elastic Net (Runner-Up): R^2 = 0.834 | MAE = 1.15 marks | RMSE = 1.85 marks",
        "OLS Regression (Baseline): R^2 = 0.831 | MAE = 1.16 marks | RMSE = 1.86 marks",
        "Lasso Regression: R^2 = 0.829 | MAE = 1.18 marks | RMSE = 1.88 marks",
        "Polynomial Degree 2: R^2 = 0.798 | MAE = 1.28 marks | RMSE = 2.05 marks",
        "Evaluation Insights: Ridge and Elastic Net dominate with < 1.15 mark average error. Residuals follow a Gaussian distribution centered at mu = 0.02, confirming homoscedasticity."
    ]
    for m in metrics:
        p = tf_11.add_paragraph()
        p.text = "• " + m
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)

    # Right Card: embed benchmark chart if exists
    bm_img = r"C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor\outputs\model_benchmark_comparison.png"
    if os.path.exists(bm_img):
        s11.shapes.add_picture(bm_img, Inches(6.7), Inches(1.5), Inches(5.8), Inches(5.4))

    # -------------------------------------------------------------------------
    # SLIDE 12: Dynamic Headroom Calibration Algorithm
    # -------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_background(s12)
    add_header(s12, "Algorithm Innovation: Dynamic Headroom Calibration")
    add_two_cards(s12,
        "The Boundary & Ceiling Defect", [
            "The Problem in Standard Models: In linear regression, continuous predictions are naively bounded by y_clipped = clip(y_pred, 0, 20).",
            "The Unreal 101 Failure: Outstanding students scoring G1=19, G2=19 were rigidly pinned to 20.00 / 20.00, ignoring examination variance and statistical headroom.",
            "Sub-Zero Anomaly: Raw models occasionally predicted negative scores for struggling students, violating the natural Portuguese academic scale [0, 20].",
            "The Need for Calibration: An intelligent post-processing layer that respects non-linear saturation near boundaries."
        ],
        "The Mathematical Calibration Solution", [
            "Dynamic Headroom Formula: For students performing in the top decile (G2 >= 17), grade headroom is adaptively computed as: delta = 20 - G2.",
            "Scale-Aware Interpolation: y_calib = y_pred + delta * min(1.0, (20 - y_pred) / (20 - G2)).",
            "Asymptotic Compression: Prevents over-optimistic pinning at 20.00 while preserving realistic distinction differentiation (e.g., 19.3 vs 19.7).",
            "Floor Safeguard: Lower boundary ensures scores <= 0 map cleanly to 0.0 with immediate critical intervention flagging."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 13: Full-Stack Web Architecture & Engineering
    # -------------------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_background(s13)
    add_header(s13, "Full-Stack System Architecture & Technology Stack")
    add_two_cards(s13,
        "Backend & Microservice Layer", [
            "FastAPI Python Framework: Asynchronous, high-throughput REST API with Pydantic type validation.",
            "Inference Engine: Dynamically evaluates OLS, Ridge, Lasso, Elastic Net, and Polynomial models on the fly.",
            "Batch Roster Processing: Parses teacher roster CSVs in under 50ms for cohort-wide grade prognostication.",
            "Production Cloudflare Tunnel: Integrated cloudflared daemon establishing zero-trust worldwide HTTPS tunneling directly from localhost:8000."
        ],
        "Frontend & User Experience (UX)", [
            "Responsive Glassmorphism UI: Built with Tailwind CSS and CSS backdrop filters for an intuitive experience.",
            "Four Simplified User Modes: Normal Mode, Hybrid Mode, Smart Mode, and Expert Mode with zero confusing formula strings.",
            "KaTeX Mathematical Engine: Locally bundled KaTeX vendor assets for LaTeX equations in technical viva inspection mode.",
            "Dynamic KPIs & Visual Reports: Instant cohort average computation, risk percentage chips, and student PDF report exports."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 14: Demonstration & Key Application Capabilities
    # -------------------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    add_background(s14)
    add_header(s14, "Live Demonstration & Application Capabilities")
    add_two_cards(s14,
        "Interactive Faculty Features", [
            "Single-Student Prognosis: Real-time slider and dropdown input updating predicted final marks in milliseconds.",
            "Cohort Batch Analysis: Upload entire class rosters (e.g., active_class_roster.csv) to visualize performance distributions.",
            "Early Risk Stratification: Automatically tags students with visual status pills (Safe / Moderate Risk / Critical At-Risk).",
            "Remedial Study Planning: Computes the exact increase in weekly study hours needed to bring at-risk students back above passing threshold."
        ],
        "Deployment & Accessibility", [
            "Worldwide Live Public URL: Accessible globally via Cloudflare Tunnel without port forwarding or VPN requirements.",
            "Offline Capability: Standalone desktop launcher (run_website.bat) operates locally without internet dependencies.",
            "Complete GitHub Repository: Publicly hosted at https://github.com/YagyaMarwari/Edupredict with complete codebase, datasets, and scripts."
        ]
    )

    # -------------------------------------------------------------------------
    # SLIDE 15: Conclusion, Impact & Academic Defense
    # -------------------------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    add_background(s15)
    add_header(s15, "Conclusion, Impact & Viva Defense Summary")
    add_two_cards(s15,
        "Project Achievements & Summary", [
            "Complete Syllabus Execution: Thoroughly implemented and benchmarked all SML Modules I & II regression and regularization algorithms.",
            "High Predictive Accuracy: Best model (Ridge) achieves R^2 = 0.835 and MAE = 1.14 marks, providing highly reliable academic forecasts.",
            "Innovation in Calibration: Successfully eliminated the boundary ceiling defect with the Dynamic Headroom post-processor.",
            "Social & Educational Impact: Directly supports UN SDG 4 (Quality Education) by enabling timely intervention before academic failure occurs."
        ],
        "Viva & Academic Defense Highlights", [
            "Why Ridge over OLS? Ridge handles collinearity between G1 and G2 (r = 0.852), stabilizing the covariance matrix via lambda * I.",
            "Why Lasso for Sparsity? L1 norm diamond geometry forces negligible weights to exact zero, reducing model complexity.",
            "Why drop_first=True? Avoids the Dummy Variable Trap (sum of dummies = 1), ensuring X^T X is non-singular and invertible.",
            "Thank You! Questions & Live System Demonstration."
        ]
    )

    # Save to multiple locations
    output_paths = [
        r"C:\Users\IIISI\OneDrive\Desktop\EduPredict_Project_Presentation.pptx",
        r"C:\Users\IIISI\Downloads\EduPredict_Project_Presentation.pptx",
        r"C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor\EduPredict_Project_Presentation.pptx"
    ]

    for p in output_paths:
        prs.save(p)
        print(f"Saved: {p} (Size: {os.path.getsize(p)} bytes)")

if __name__ == "__main__":
    create_presentation()
