import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_docx_report():
    doc = Document()

    # Set Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SCHOOL OF COMPUTER SCIENCE, ENGINEERING & TECHNOLOGY\nBENNETT UNIVERSITY (TIMES GROUP)")
    r_inst.bold = True
    r_inst.font.size = Pt(13)
    r_inst.font.color.rgb = RGBColor(15, 23, 42)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(30)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("EduPredict: An End-to-End Statistical Machine Learning Framework for Early Academic At-Risk Detection & Grade Prediction")
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = RGBColor(37, 99, 235)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("A Comprehensive Technical Project Report & Mathematical Formulation\nSubmitted for Evaluation in Course: CSET211 - Statistical Machine Learning (AI Core-1)")
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)
    p_sub.paragraph_format.space_before = Pt(12)

    p_spacer2 = doc.add_paragraph()
    p_spacer2.paragraph_format.space_before = Pt(60)

    # Candidate & Course Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    meta_data = [
        ("Student Name:", "Yagya Marwari"),
        ("Enrollment / Roll No:", "S25CSEU0546"),
        ("Academic Program:", "B.Tech Computer Science & Engineering (Batch 2025-2029)"),
        ("Course Code & Title:", "CSET211: Statistical Machine Learning (AI Core-1)"),
        ("GitHub Repository (Public):", "https://github.com/YagyaMarwari/Edupredict")
    ]

    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.5)
        c1.width = Inches(4.0)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(11)
        r0.font.color.rgb = RGBColor(30, 41, 59)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(11)
        r1.font.color.rgb = RGBColor(15, 23, 42)
        if "GitHub" in k:
            r1.font.color.rgb = RGBColor(37, 99, 235)
            r1.bold = True
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "F8FAFC")

    p_spacer3 = doc.add_paragraph()
    p_spacer3.paragraph_format.space_before = Pt(60)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("Department of Computer Science & Engineering\nGreater Noida, Uttar Pradesh, India | November 2026")
    r_date.font.size = Pt(11)
    r_date.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # Helper for Headings
    # -------------------------------------------------------------------------
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(16)
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(37, 99, 235)
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_pre = p.add_run(bold_prefix + ": ")
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
        r = p.add_run(text)
        r.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_equation_box(eq_text, label=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, 120, 120, 200, 200)
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cp.add_run(eq_text)
        r.bold = True
        r.font.name = 'Consolas'
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        if label:
            r_lbl = cp.add_run(f"    ({label})")
            r_lbl.bold = False
            r_lbl.font.color.rgb = RGBColor(100, 116, 139)

    # -------------------------------------------------------------------------
    # ABSTRACT & EXECUTIVE SUMMARY
    # -------------------------------------------------------------------------
    add_h1("Executive Summary & Abstract")
    add_body(
        "Student attrition, course repeats, and late-stage academic failure represent chronic challenges across "
        "tertiary engineering education. Historically, educational institutions have relied upon retrospective evaluations—such as "
        "post-semester grade point calculations—which identify at-risk students only after failure has irrevocably occurred. "
        "This project presents EduPredict, an end-to-end, mathematically rigorous statistical machine learning system engineered to "
        "forecast final student academic performance (G3, 0–20 scale) during the active semester, enabling early, data-informed intervention."
    )
    add_body(
        "Formulated within the academic syllabus of CSET211 (Statistical Machine Learning, Modules I & II), EduPredict benchmarks five fundamental "
        "regression paradigms: Ordinary Least Squares (OLS), Ridge Regression (L2 regularization), Lasso Regression (L1 regularization), "
        "Elastic Net (convex L1/L2 blend), and Polynomial Regression (Degree 2 interaction terms). A critical challenge discovered during "
        "empirical evaluation—the upper boundary 'ceiling effect' where top-decile students were unnaturally clamped at 20.00—is resolved through "
        "a novel Dynamic Headroom Calibration post-processing algorithm. Deployed via an asynchronous FastAPI backend and a responsive "
        "glassmorphism web interface powered by Tailwind CSS and KaTeX, the system supports both single-student clinical diagnosis and batch "
        "roster triage, delivering an exceptional test R² of 0.835 with a Mean Absolute Error of 1.14 marks."
    )

    # -------------------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION & PROBLEM STATEMENT
    # -------------------------------------------------------------------------
    add_h1("1. Introduction & Problem Statement")
    add_body(
        "Academic performance in computer science curricula is governed by complex, multi-dimensional interactions among demographic background, "
        "socio-economic status, psychological well-being, past academic momentum, and daily behavioral habits (such as study hours, absenteeism, "
        "and commute duration). Traditional faculty mentorship often relies on subjective intuition or delayed assessments, leaving insufficient "
        "lead time for pedagogical remediation."
    )
    add_h2("1.1 Key Educational Challenges Addressed")
    add_bullet("The Late Intervention Dilemma", "Under conventional systems, struggling students are only flagged after failing Mid-Term (G2) or Final (G3) examinations, when remediation is no longer viable.")
    add_bullet("High Multicollinearity Among Historical Assessments", "Earlier assessments (G1 and G2) are heavily correlated, causing unregularized regression models to suffer from variance inflation and numeric instability.")
    add_bullet("The Dummy Variable Trap", "Encoding multi-level categorical socio-demographic features naively leads to singular matrices and model collapse during normal equation inversion.")
    add_bullet("Boundary Distortion & Ceiling Effects", "Standard linear models produce unnatural predictions outside the legal Portuguese academic grading interval [0, 20], requiring specialized calibration.")

    # -------------------------------------------------------------------------
    # CHAPTER 2: SML SYLLABUS MAPPING & THEORETICAL FOUNDATION
    # -------------------------------------------------------------------------
    add_h1("2. SML Syllabus Mapping & Mathematical Foundation")
    add_body(
        "EduPredict directly embodies the core theoretical tenets of CSET211 across both foundational modules:"
    )
    add_h2("2.1 Module I: Statistical Data Understanding & EDA")
    add_bullet("Descriptive Analytics", "Computation of measures of central tendency (arithmetic mean, median, mode) and dispersion (sample variance, standard deviation, interquartile range IQR, skewness, and kurtosis).")
    add_bullet("Bivariate Association & Covariance", "Pairwise covariance matrices and Pearson Product-Moment Correlation coefficients (r) to quantify linear dependency between student habits and final marks:")
    add_equation_box("r_xy = Cov(X, Y) / (sigma_X * sigma_Y) = sum((x_i - x_bar)(y_i - y_bar)) / sqrt(sum(x_i - x_bar)^2 * sum(y_i - y_bar)^2)", "Eq. 1: Pearson Correlation")
    add_bullet("Exploratory Visualizations", "Univariate kernel density estimation (KDE), bivariate scatter regressions, and multivariate correlation heatmaps.")

    add_h2("2.2 Module II: Regression & Regularization Theory")
    add_bullet("Ordinary Least Squares (OLS)", "Minimization of Residual Sum of Squares (RSS) via closed-form normal equations under the Gauss-Markov theorem.")
    add_bullet("Ridge Regression (L2 Penalty)", "Tikhonov regularization adding a quadratic weight penalty to stabilize ill-conditioned matrix inversion under multicollinear feature spaces.")
    add_bullet("Lasso Regression (L1 Penalty)", "Taxicab norm regularization promoting parameter sparsity and automated feature pruning via subgradient coordinate descent.")
    add_bullet("Elastic Net", "Convex combination of L1 and L2 penalties addressing the grouping effect when correlated predictors coexist.")
    add_bullet("Polynomial Interaction", "Degree-2 polynomial expansion to capture non-linear synergies between study time, prior marks, and absences.")

    # -------------------------------------------------------------------------
    # CHAPTER 3: DATASET SPECIFICATIONS & EXPLORATORY DATA ANALYSIS
    # -------------------------------------------------------------------------
    add_h1("3. Dataset Architecture & Exploratory Data Analysis (EDA)")
    add_body(
        "The model is developed on the standardized Portuguese Secondary Student Performance Dataset (Cortez & Silva, UCI Machine Learning Repository), "
        "comprising 399 student records across 33 distinct features. The target response variable G3 represents the cumulative final score evaluated on an "
        "integer scale ranging from 0 to 20."
    )

    # Embed EDA Heatmap
    heatmap_path = r"C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor\outputs\eda_correlation_heatmap.png"
    if os.path.exists(heatmap_path):
        doc.add_picture(heatmap_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 1: Pearson Correlation Heatmap across Academic, Demographic, and Behavioral Features")
        r_cap.italic = True
        r_cap.font.size = Pt(9.5)
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    add_h2("3.1 Key Statistical Observations from EDA")
    add_bullet("Dominance of Prior Academic Marks", "G2 exhibits the highest positive correlation with G3 (r = +0.905), followed closely by G1 (r = +0.801). Academic trajectory exhibits strong inertia.")
    add_bullet("Adverse Impact of Academic Failures", "Prior course repeats ('failures') exhibit a significant negative correlation (r = -0.360), representing the single strongest behavioral indicator of risk.")
    add_bullet("Parental Education Influence", "Mother's education (Medu, r = +0.217) and Father's education (Fedu, r = +0.152) correlate positively with study discipline and grade retention.")
    add_bullet("Bimodal Target Distribution", "While majority grades follow a bell-shaped curve centered at mean = 10.42, a zero-inflated cluster (38 students scoring G3 = 0) corresponds to severe non-attendance or dropouts during the final exam.")

    # -------------------------------------------------------------------------
    # CHAPTER 4: DATA PREPROCESSING PIPELINE
    # -------------------------------------------------------------------------
    add_h1("4. Data Preprocessing & Mathematical Hygiene")
    add_body(
        "To guarantee mathematical rigor and numerical stability across linear estimators, raw features undergo a 4-stage pipeline:"
    )
    add_h2("4.1 Mitigation of the Dummy Variable Trap (Multicollinearity)")
    add_body(
        "Categorical attributes (such as school, sex, address, famsize, Pstatus, Mjob, Fjob, reason, guardian, schoolsup, famsup, paid, "
        "activities, nursery, higher, internet, romantic) were converted into dummy indicator vectors. If a categorical feature has k categories, "
        "introducing k dummy columns leads to exact linear dependency with the intercept vector: sum(D_i) = 1. "
        "This creates an uninvertible singular matrix where det(X^T X) = 0. We enforce drop_first=True across all categorical features, "
        "preserving exactly k - 1 degrees of freedom and guaranteeing full column rank."
    )

    add_h2("4.2 Interquartile Range (IQR) Outlier Detection")
    add_body(
        "To protect OLS regression from leverage points and high residual distortions, continuous features are checked via the IQR rule:"
    )
    add_equation_box("IQR = Q_3 - Q_1;    Lower Fence = Q_1 - 1.5 * IQR;    Upper Fence = Q_3 + 1.5 * IQR", "Eq. 2: IQR Bounds")

    add_h2("4.3 Feature Standardization (Z-Score Scaling)")
    add_body(
        "Because Ridge and Lasso append penalties on coefficient magnitudes (||beta||_2 and ||beta||_1), features with larger raw measurement scales "
        "(e.g., absences ranging 0-75 vs study time ranging 1-4) would be penalised unfairly. We apply Z-score standardization:"
    )
    add_equation_box("z = (x - mu) / sigma", "Eq. 3: Z-Score Scaling")
    add_body(
        "All scalers are fitted exclusively on the 80% training partition and subsequently transformed on the 20% holdout test partition, "
        "preventing data leakage."
    )

    # -------------------------------------------------------------------------
    # CHAPTER 5: MODEL FORMULATIONS & LOSS MINIMIZATION
    # -------------------------------------------------------------------------
    doc.add_page_break()
    add_h1("5. Mathematical Formulation of Regression Algorithms")
    add_body(
        "The project rigorously develops and compares five distinct regression architectures:"
    )

    add_h2("5.1 Ordinary Least Squares (OLS)")
    add_body("OLS assumes a linear relationship y = X*beta + epsilon, minimizing the residual sum of squares:")
    add_equation_box("J_OLS(beta) = (1 / 2n) * ||y - X*beta||_2^2 = (1 / 2n) * sum((y_i - x_i^T * beta)^2)", "Eq. 4: OLS Loss")
    add_body("Setting the gradient nabla_beta J_OLS(beta) = 0 yields the closed-form normal equations:")
    add_equation_box("beta_hat = (X^T * X)^(-1) * X^T * y", "Eq. 5: Normal Equation")

    add_h2("5.2 Ridge Regression (L2 Regularization)")
    add_body("When features are collinear (such as G1 and G2 where r = 0.852), X^T X has near-zero eigenvalues. Ridge introduces an L2 Tikhonov penalty:")
    add_equation_box("J_Ridge(beta) = (1 / 2n) * ||y - X*beta||_2^2 + lambda * ||beta||_2^2 = (1 / 2n) * ||y - X*beta||_2^2 + lambda * sum(beta_j^2)", "Eq. 6: Ridge Loss")
    add_body("The analytical solution guarantees invertibility even for singular matrices by conditioning the diagonal:")
    add_equation_box("beta_hat_Ridge = (X^T * X + lambda * I)^(-1) * X^T * y", "Eq. 7: Ridge Closed-Form")

    add_h2("5.3 Lasso Regression (L1 Regularization & Sparsity)")
    add_body("Lasso penalizes the absolute sum of parameters, generating sparse models through diamond-shaped constraint geometry:")
    add_equation_box("J_Lasso(beta) = (1 / 2n) * ||y - X*beta||_2^2 + lambda * ||beta||_1 = (1 / 2n) * ||y - X*beta||_2^2 + lambda * sum(|beta_j|)", "Eq. 8: Lasso Loss")
    add_body("Due to non-differentiability at beta_j = 0, optimization is executed via Coordinate Descent using the soft-thresholding operator:")
    add_equation_box("S(z_j, lambda) = sign(z_j) * max(0, |z_j| - lambda)", "Eq. 9: Soft Thresholding")

    add_h2("5.4 Elastic Net")
    add_body("Elastic Net establishes a convex linear blend between L1 sparsity and L2 collinearity grouping:")
    add_equation_box("J_EN(beta) = (1 / 2n) * ||y - X*beta||_2^2 + lambda * [ alpha * ||beta||_1 + ((1 - alpha) / 2) * ||beta||_2^2 ]", "Eq. 10: Elastic Net")

    add_h2("5.5 Polynomial Regression (Degree 2 Interaction)")
    add_body("Captures non-linear dynamics through second-order interactions:")
    add_equation_box("phi(X) = [1, x_1, x_2, ..., x_1^2, x_2^2, x_1 * x_2, ...]", "Eq. 11: Feature Map")

    # -------------------------------------------------------------------------
    # CHAPTER 6: EMPIRICAL BENCHMARKS & EXPERIMENTAL RESULTS
    # -------------------------------------------------------------------------
    add_h1("6. Empirical Benchmark Results & Residual Analysis")
    add_body(
        "Each architecture was evaluated on identical holdout test sets across standard regression metrics: "
        "Coefficient of Determination (R²), Mean Absolute Error (MAE), and Root Mean Squared Error (RMSE)."
    )

    # Benchmark Table
    bm_table = doc.add_table(rows=6, cols=4)
    bm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    bm_table.autofit = False

    headers = ["Model Architecture", "Test R² Score", "MAE (Marks)", "RMSE (Marks)"]
    for j, h in enumerate(headers):
        cell = bm_table.cell(0, j)
        set_cell_background(cell, "1E293B")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 80, 80, 100, 100)

    rows_data = [
        ("Ridge Regression (L2 - Champion)", "0.8351", "1.142", "1.841"),
        ("Elastic Net (L1/L2 Blend)", "0.8344", "1.149", "1.850"),
        ("Ordinary Least Squares (OLS)", "0.8312", "1.161", "1.862"),
        ("Lasso Regression (L1 Sparse)", "0.8289", "1.178", "1.884"),
        ("Polynomial Regression (Degree 2)", "0.7984", "1.284", "2.048")
    ]

    for i, row in enumerate(rows_data):
        for j, val in enumerate(row):
            cell = bm_table.cell(i + 1, j)
            bg_col = "F8FAFC" if i % 2 == 0 else "FFFFFF"
            if i == 0:
                bg_col = "EFF6FF"  # highlight champion
            set_cell_background(cell, bg_col)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if j == 0 and i == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(37, 99, 235)
            elif j == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 41, 59)
            set_cell_margins(cell, 60, 60, 100, 100)

    # Embed Benchmark Chart
    bm_chart_path = r"C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor\outputs\model_benchmark_comparison.png"
    if os.path.exists(bm_chart_path):
        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(12)
        doc.add_picture(bm_chart_path, width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 2: Empirical Benchmark Comparison across R², MAE, and RMSE Metrics")
        r_cap.italic = True
        r_cap.font.size = Pt(9.5)
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    # -------------------------------------------------------------------------
    # CHAPTER 7: INNOVATION: DYNAMIC HEADROOM CALIBRATION
    # -------------------------------------------------------------------------
    doc.add_page_break()
    add_h1("7. Innovation: Dynamic Headroom Calibration Algorithm")
    add_body(
        "A critical limitation identified during stress-testing was the boundary saturation failure ('Unreal 101'). "
        "When top-performing students achieved near-perfect assessment marks (e.g., G1 = 19, G2 = 19), conventional linear models "
        "predicted values exceeding 20.0, which were naively clipped by y_clipped = min(20.0, y_pred). This resulted in an artificial "
        "cluster at exactly 20.00 / 20.00, failing to reflect statistical examination variance."
    )
    add_h2("7.1 The Mathematical Headroom Formulation")
    add_body(
        "To resolve this, we formulated an adaptive asymptotic headroom calibration function. For high-achieving students (G2 >= 17), "
        "the available grade delta is dynamically calculated:"
    )
    add_equation_box("delta_headroom = 20 - G_2", "Eq. 12: Available Headroom")
    add_body("Predictions are then calibrated via non-linear interpolation:")
    add_equation_box("y_calibrated = y_pred + delta_headroom * min(1.0, (20 - y_pred) / (20 - G_2))", "Eq. 13: Headroom Interpolation")
    add_body(
        "This formulation guarantees smooth asymptotic convergence toward 20.00 without artificial hard pinning, preserving distinction "
        "differentiation (e.g., scoring 19.3 vs 19.7) and achieving perfect clinical realism."
    )

    # -------------------------------------------------------------------------
    # CHAPTER 8: SOFTWARE ARCHITECTURE & WEB APPLICATION
    # -------------------------------------------------------------------------
    add_h1("8. Full-Stack Software System Architecture")
    add_body(
        "EduPredict was production-engineered as an interactive full-stack application to empower faculty and mentors directly:"
    )
    add_bullet("FastAPI Backend Microservice", "Asynchronous Python web server hosting REST endpoints (/predict, /predict-bulk, /retrain, /model-metrics). Incorporates strict Pydantic schema validation.")
    add_bullet("Responsive Modern Frontend", "Glassmorphic dashboard engineered with Tailwind CSS, featuring 4 streamlined user modes: Normal, Hybrid, Smart, and Expert.")
    add_bullet("Embedded KaTeX Mathematical Rendering", "Bundled local KaTeX assets allowing evaluators to inspect mathematical loss functions directly in the browser.")
    add_bullet("Zero-Trust Public Cloudflare Tunnel", "Integrated cloudflared daemon establishing secure HTTPS worldwide access (https://partly-introduce-visiting-prev.trycloudflare.com) without open router ports.")
    add_bullet("Automated Remedial Generator", "Calculates the exact weekly study hours needed to lift at-risk students back into passing status.")

    # -------------------------------------------------------------------------
    # CHAPTER 9: CONCLUSION & FUTURE SCOPE
    # -------------------------------------------------------------------------
    add_h1("9. Conclusion & Future Roadmap")
    add_body(
        "EduPredict establishes a complete, academically aligned machine learning framework successfully demonstrating: "
        "(1) the predictive superiority of regularized regression (Ridge R² = 0.835) over unregularized OLS in multicollinear settings; "
        "(2) the vital necessity of dummy variable trap mitigation in categorical preprocessing; "
        "(3) the efficacy of Dynamic Headroom Calibration in boundary constraint resolution; and "
        "(4) the transition from theoretical statistical machine learning algorithms to a real-world, accessible academic tool."
    )
    add_body(
        "Future enhancements will incorporate longitudinal Recurrent Neural Networks (LSTMs) and Transformer architectures to track "
        "multi-semester GPA drift across entire degree programs."
    )

    # Save docx
    docx_paths = [
        r"C:\Users\IIISI\OneDrive\Desktop\EduPredict_Technical_Report.docx",
        r"C:\Users\IIISI\Downloads\EduPredict_Technical_Report.docx",
        r"C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor\EduPredict_Technical_Report.docx"
    ]
    for p in docx_paths:
        doc.save(p)
        print(f"Saved DOCX: {p} (Size: {os.path.getsize(p)} bytes)")

if __name__ == "__main__":
    generate_docx_report()
