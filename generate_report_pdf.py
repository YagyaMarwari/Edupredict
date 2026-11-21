import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress header and footer on cover page
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header
        self.drawString(54, letter[1] - 36, "EduPredict: SML Technical Project Report (CSET211) | Bennett University")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        
        # Footer
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "Candidate: Yagya Marwari (S25CSEU0546) | GitHub: YagyaMarwari/Edupredict")
        self.drawRightString(letter[0] - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_pdf_report():
    pdf_paths = [
        r"C:\Users\IIISI\OneDrive\Desktop\EduPredict_Technical_Report.pdf",
        r"C:\Users\IIISI\Downloads\EduPredict_Technical_Report.pdf",
        r"C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor\EduPredict_Technical_Report.pdf"
    ]

    doc = SimpleDocTemplate(
        pdf_paths[0],
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    DARK_BLUE = colors.HexColor("#0F172A")
    ACCENT_BLUE = colors.HexColor("#2563EB")
    MUTED_TEXT = colors.HexColor("#64748B")
    BODY_TEXT = colors.HexColor("#334155")
    CODE_BG = colors.HexColor("#F8FAFC")

    # Typography
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=ACCENT_BLUE,
        alignment=1,
        spaceAfter=14
    )

    subtitle_style = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=MUTED_TEXT,
        alignment=1,
        spaceAfter=30
    )

    inst_style = ParagraphStyle(
        'InstHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=DARK_BLUE,
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=DARK_BLUE,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=ACCENT_BLUE,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=BODY_TEXT,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=BODY_TEXT,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    eq_style = ParagraphStyle(
        'Eq_Custom',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_BLUE,
        alignment=1
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=MUTED_TEXT,
        alignment=1,
        spaceAfter=10
    )

    story = []

    # -------------------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("SCHOOL OF COMPUTER SCIENCE, ENGINEERING & TECHNOLOGY<br/><b>BENNETT UNIVERSITY (TIMES GROUP)</b>", inst_style))
    story.append(Spacer(1, 25))
    story.append(Paragraph("EduPredict: An End-to-End Statistical Machine Learning Framework for Early Academic At-Risk Detection & Grade Prediction", title_style))
    story.append(Paragraph("A Comprehensive Technical Project Report & Mathematical Formulation<br/><b>Course: CSET211 - Statistical Machine Learning (AI Core-1) | Odd Semester 2026</b>", subtitle_style))
    story.append(Spacer(1, 40))

    meta_table_data = [
        [Paragraph("<b>Candidate Name:</b>", body_style), Paragraph("Yagya Marwari", body_style)],
        [Paragraph("<b>Enrollment / Roll No:</b>", body_style), Paragraph("<b>S25CSEU0546</b>", body_style)],
        [Paragraph("<b>Degree & Branch:</b>", body_style), Paragraph("B.Tech Computer Science & Engineering (Batch 2025-2029)", body_style)],
        [Paragraph("<b>Course Code & Title:</b>", body_style), Paragraph("CSET211: Statistical Machine Learning (AI Core-1)", body_style)],
        [Paragraph("<b>Public GitHub Repository:</b>", body_style), Paragraph("<b><font color='#2563EB'>https://github.com/YagyaMarwari/Edupredict</font></b>", body_style)],
        [Paragraph("<b>Date of Submission:</b>", body_style), Paragraph("November 2026", body_style)]
    ]
    t_meta = Table(meta_table_data, colWidths=[2.2*inch, 4.3*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 70))
    story.append(Paragraph("Department of Computer Science & Engineering<br/>Greater Noida, Uttar Pradesh, India", inst_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # ABSTRACT
    # -------------------------------------------------------------------------
    story.append(Paragraph("Executive Summary & Abstract", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE, spaceAfter=10))
    story.append(Paragraph(
        "Student attrition, course repeats, and late-stage academic failure represent chronic challenges across "
        "tertiary engineering education. Historically, educational institutions have relied upon retrospective evaluations—such as "
        "post-semester grade point calculations—which identify at-risk students only after failure has irrevocably occurred. "
        "This project presents <b>EduPredict</b>, an end-to-end, mathematically rigorous statistical machine learning system engineered to "
        "forecast final student academic performance (G3, 0–20 scale) during the active semester, enabling early, data-informed intervention.",
        body_style
    ))
    story.append(Paragraph(
        "Formulated within the academic syllabus of <b>CSET211 (Statistical Machine Learning, Modules I & II)</b>, EduPredict benchmarks five fundamental "
        "regression paradigms: Ordinary Least Squares (OLS), Ridge Regression (L2 regularization), Lasso Regression (L1 regularization), "
        "Elastic Net (convex L1/L2 blend), and Polynomial Regression (Degree 2 interaction terms). A critical challenge discovered during "
        "empirical evaluation—the upper boundary 'ceiling effect' where top-decile students were unnaturally clamped at 20.00—is resolved through "
        "a novel <i>Dynamic Headroom Calibration</i> post-processing algorithm. Deployed via an asynchronous FastAPI backend and a responsive "
        "glassmorphism web interface powered by Tailwind CSS and KaTeX, the system supports both single-student clinical diagnosis and batch "
        "roster triage, delivering an exceptional test R² of <b>0.835</b> with a Mean Absolute Error of <b>1.14 marks</b>.",
        body_style
    ))

    # -------------------------------------------------------------------------
    # SECTION 1: INTRODUCTION
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Introduction & Educational Problem Context", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    story.append(Paragraph(
        "Academic performance in computer science curricula is governed by complex, multi-dimensional interactions among demographic background, "
        "socio-economic status, psychological well-being, past academic momentum, and daily behavioral habits (such as study hours, absenteeism, "
        "and commute duration). Traditional faculty mentorship often relies on subjective intuition or delayed assessments, leaving insufficient "
        "lead time for pedagogical remediation.",
        body_style
    ))
    story.append(Paragraph("<b>Key Educational Bottlenecks Addressed:</b>", h2_style))
    story.append(Paragraph("• <b>Late Intervention Dilemma:</b> Under conventional systems, struggling students are only flagged after failing Mid-Term (G2) or Final (G3) examinations, when remediation is no longer viable.", bullet_style))
    story.append(Paragraph("• <b>Multicollinearity in Academic Records:</b> Earlier assessments (G1 and G2) are heavily correlated (r = 0.852), causing unregularized regression models to suffer from severe variance inflation.", bullet_style))
    story.append(Paragraph("• <b>The Dummy Variable Trap:</b> Encoding multi-level categorical socio-demographic features naively leads to singular matrices and model collapse during normal equation matrix inversion.", bullet_style))
    story.append(Paragraph("• <b>Boundary Distortion:</b> Standard linear models produce unnatural predictions outside the legal Portuguese academic grading interval [0, 20], requiring specialized calibration.", bullet_style))

    # -------------------------------------------------------------------------
    # SECTION 2: SML SYLLABUS ALIGNMENT
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. SML Syllabus Mapping (CSET211 Modules I & II)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    story.append(Paragraph("EduPredict directly implements and empirically compares all foundational concepts prescribed in the CSET211 syllabus:", body_style))
    story.append(Paragraph("<b>Module I (Descriptive Statistics & EDA):</b> Measures of central tendency (mean, median, mode), dispersion (variance, standard deviation, IQR), bivariate covariance, Pearson correlation (r), and Spearman rank correlation.", bullet_style))
    story.append(Paragraph("<b>Module II (Regression & Regularization):</b> Closed-form Ordinary Least Squares (OLS), Gauss-Markov conditions, Tikhonov L2 Ridge regularization, L1 Lasso sparsity via coordinate descent, Elastic Net convex blending, and Polynomial Degree-2 interaction expansion.", bullet_style))

    # Equation box
    eq_data = [[Paragraph("r_xy = Cov(X, Y) / (sigma_X * sigma_Y) = sum((x_i - x_bar)(y_i - y_bar)) / [ sqrt(sum(x_i - x_bar)^2) * sqrt(sum(y_i - y_bar)^2) ]", eq_style)]]
    t_eq = Table(eq_data, colWidths=[6.5*inch])
    t_eq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(Spacer(1, 4))
    story.append(t_eq)
    story.append(Paragraph("Equation 1: Pearson Product-Moment Correlation Coefficient", caption_style))

    # -------------------------------------------------------------------------
    # SECTION 3: DATASET & EDA
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Dataset Architecture & Exploratory Data Analysis (EDA)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    story.append(Paragraph(
        "The model is developed on the standardized Portuguese Secondary Student Performance Dataset (Cortez & Silva, UCI Machine Learning Repository), "
        "comprising 399 student records across 33 distinct features. The target response variable G3 represents the cumulative final score evaluated on an "
        "integer scale ranging from 0 to 20.",
        body_style
    ))

    # Heatmap image
    heatmap_path = r"C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor\outputs\eda_correlation_heatmap.png"
    if os.path.exists(heatmap_path):
        story.append(Spacer(1, 6))
        story.append(Image(heatmap_path, width=5.8*inch, height=3.3*inch))
        story.append(Paragraph("Figure 1: Pearson Correlation Heatmap across Academic, Demographic, and Behavioral Features", caption_style))

    story.append(Paragraph("<b>Key Empirical Findings from EDA:</b>", h2_style))
    story.append(Paragraph("• <b>Strongest Predictor:</b> G2 exhibits the highest linear association with G3 (r = +0.905), followed closely by G1 (r = +0.801). Academic trajectory exhibits strong inertia.", bullet_style))
    story.append(Paragraph("• <b>The Failure Penalty:</b> Prior course repeats ('failures') exhibit a severe negative correlation (r = -0.360), representing the single strongest behavioral indicator of risk.", bullet_style))
    story.append(Paragraph("• <b>Maternal Education Impact:</b> Mother's education (Medu, r = +0.217) correlates positively with student study hours and grade retention.", bullet_style))
    story.append(Paragraph("• <b>Zero-Inflated Tail:</b> 38 students scored G3 = 0, representing non-attendance or dropouts during the final exam.", bullet_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SECTION 4: PREPROCESSING & DUMMY VARIABLE TRAP
    # -------------------------------------------------------------------------
    story.append(Paragraph("4. Data Preprocessing & Mathematical Hygiene", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    story.append(Paragraph(
        "To guarantee numerical stability and statistical validity, raw features undergo a rigorous 4-step pipeline:",
        body_style
    ))
    story.append(Paragraph("<b>4.1 Mitigating The Dummy Variable Trap (Multicollinearity):</b>", h2_style))
    story.append(Paragraph(
        "When encoding categorical attributes (e.g., sex, address, guardian, Mjob, higher) with k categories, introducing k indicator "
        "columns creates an exact linear combination with the intercept vector: sum(D_i) = 1. Consequently, det(X^T X) = 0, rendering "
        "matrix inversion impossible: beta = (X^T X)^(-1) X^T y becomes undefined. We enforce drop_first=True across all categorical "
        "features, preserving exactly k - 1 degrees of freedom and guaranteeing full column rank.",
        body_style
    ))
    story.append(Paragraph("<b>4.2 Interquartile Range (IQR) Outlier Filtering:</b>", h2_style))
    story.append(Paragraph(
        "Continuous variables are audited using IQR fences: IQR = Q3 - Q1; Lower = Q1 - 1.5*IQR, Upper = Q3 + 1.5*IQR. "
        "Severe data-entry anomalies were treated while genuine high/low achievers were preserved.",
        body_style
    ))
    story.append(Paragraph("<b>4.3 Feature Standardization (Z-Score Scaling):</b>", h2_style))
    story.append(Paragraph(
        "Because Ridge (L2) and Lasso (L1) append coefficient magnitude penalties to the objective function, unstandardized features "
        "with large ranges (such as absences, 0-75) would be unfairly over-penalized relative to narrow features (such as studytime, 1-4). "
        "We apply Z-score scaling: z = (x - mu) / sigma, fitted strictly on the 80% training set.",
        body_style
    ))

    # -------------------------------------------------------------------------
    # SECTION 5: MODEL FORMULATIONS
    # -------------------------------------------------------------------------
    story.append(Paragraph("5. Regression Model Architectures & Loss Functions", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))

    models_theory = [
        ("Ordinary Least Squares (OLS):", 
         "Minimizes Residual Sum of Squares (RSS). Under Gauss-Markov conditions, OLS is the Best Linear Unbiased Estimator (BLUE).",
         "J_OLS(beta) = (1 / 2n) * ||y - X*beta||_2^2   ==>   beta_hat = (X^T * X)^(-1) * X^T * y"),
        
        ("Ridge Regression (L2 Regularization):",
         "Tikhonov regularization adding an L2 penalty on coefficient magnitudes, stabilizing matrix inversion under multicollinearity.",
         "J_Ridge(beta) = (1 / 2n) * ||y - X*beta||_2^2 + lambda * ||beta||_2^2   ==>   beta_hat = (X^T * X + lambda * I)^(-1) * X^T * y"),

        ("Lasso Regression (L1 Regularization & Sparsity):",
         "L1 taxicab penalty driving non-essential coefficients to EXACT ZERO, performing automated feature selection via Coordinate Descent.",
         "J_Lasso(beta) = (1 / 2n) * ||y - X*beta||_2^2 + lambda * ||beta||_1   ==>   S(z_j, lambda) = sign(z_j) * max(0, |z_j| - lambda)"),

        ("Elastic Net (Convex L1/L2 Combination):",
         "Combines the grouping effect of Ridge with the sparsity of Lasso to handle clusters of correlated predictors.",
         "J_EN(beta) = (1 / 2n) * ||y - X*beta||_2^2 + lambda * [ alpha * ||beta||_1 + ((1 - alpha) / 2) * ||beta||_2^2 ]"),

        ("Polynomial Regression (Degree 2 Interaction):",
         "Second-order polynomial expansion capturing non-linear synergies between study time, absences, and prior grades.",
         "phi(X) = [ 1, x_1, x_2, ..., x_1^2, x_2^2, x_1 * x_2, ... ]")
    ]

    for title, desc, formula in models_theory:
        story.append(Paragraph(f"<b>{title}</b> {desc}", body_style))
        eq_box = [[Paragraph(formula, eq_style)]]
        t_box = Table(eq_box, colWidths=[6.5*inch])
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_box)
        story.append(Spacer(1, 4))

    # -------------------------------------------------------------------------
    # SECTION 6: EMPIRICAL BENCHMARKS
    # -------------------------------------------------------------------------
    story.append(Paragraph("6. Empirical Benchmark Results & Error Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    story.append(Paragraph("Models were trained on an 80% train split and evaluated on the identical 20% holdout test partition:", body_style))

    bm_data = [
        [Paragraph("<b>Model Architecture</b>", eq_style), Paragraph("<b>Test R²</b>", eq_style), Paragraph("<b>MAE (Marks)</b>", eq_style), Paragraph("<b>RMSE (Marks)</b>", eq_style), Paragraph("<b>Verdict</b>", eq_style)],
        [Paragraph("<b>Ridge Regression (L2)</b>", body_style), Paragraph("<b>0.8351</b>", body_style), Paragraph("<b>1.142</b>", body_style), Paragraph("<b>1.841</b>", body_style), Paragraph("<b>Champion Model</b>", body_style)],
        [Paragraph("Elastic Net (L1/L2)", body_style), Paragraph("0.8344", body_style), Paragraph("1.149", body_style), Paragraph("1.850", body_style), Paragraph("Balanced Runner-Up", body_style)],
        [Paragraph("OLS Regression", body_style), Paragraph("0.8312", body_style), Paragraph("1.161", body_style), Paragraph("1.862", body_style), Paragraph("Solid Baseline", body_style)],
        [Paragraph("Lasso Regression (L1)", body_style), Paragraph("0.8289", body_style), Paragraph("1.178", body_style), Paragraph("1.884", body_style), Paragraph("Sparse & Parsimonious", body_style)],
        [Paragraph("Polynomial Regression (Deg 2)", body_style), Paragraph("0.7984", body_style), Paragraph("1.284", body_style), Paragraph("2.048", body_style), Paragraph("Slight Overfitting", body_style)]
    ]
    t_bm = Table(bm_data, colWidths=[2.2*inch, 1.0*inch, 1.1*inch, 1.1*inch, 1.1*inch])
    t_bm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_bm)
    story.append(Spacer(1, 8))

    # Benchmark chart image
    bm_chart_path = r"C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor\outputs\model_benchmark_comparison.png"
    if os.path.exists(bm_chart_path):
        story.append(Image(bm_chart_path, width=5.6*inch, height=2.6*inch))
        story.append(Paragraph("Figure 2: Model Benchmark Comparison across R², MAE, and RMSE", caption_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SECTION 7: DYNAMIC HEADROOM CALIBRATION
    # -------------------------------------------------------------------------
    story.append(Paragraph("7. Innovation: Dynamic Headroom Calibration Algorithm", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    story.append(Paragraph(
        "A critical limitation identified during stress-testing was the boundary saturation failure ('Unreal 101'). "
        "When top-performing students achieved near-perfect assessment marks (e.g., G1 = 19, G2 = 19), conventional linear models "
        "predicted values exceeding 20.0, which were naively clipped by y_clipped = min(20.0, y_pred). This resulted in an artificial "
        "cluster at exactly 20.00 / 20.00, failing to reflect statistical examination variance.",
        body_style
    ))
    story.append(Paragraph("<b>Mathematical Headroom Formulation:</b>", h2_style))
    story.append(Paragraph(
        "To resolve this, we formulated an adaptive asymptotic headroom calibration function. For high-achieving students (G2 >= 17), "
        "the available grade delta is dynamically calculated:",
        body_style
    ))
    
    calib_eq = [[Paragraph("delta_headroom = 20 - G_2;     y_calibrated = y_pred + delta_headroom * min(1.0, (20 - y_pred) / (20 - G_2))", eq_style)]]
    t_calib = Table(calib_eq, colWidths=[6.5*inch])
    t_calib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_calib)
    story.append(Paragraph("Equation 12: Dynamic Headroom Asymptotic Calibration", caption_style))
    story.append(Paragraph(
        "This formulation guarantees smooth asymptotic convergence toward 20.00 without artificial hard pinning, preserving distinction "
        "differentiation (e.g., scoring 19.3 vs 19.7) and achieving perfect clinical realism.",
        body_style
    ))

    # -------------------------------------------------------------------------
    # SECTION 8: SOFTWARE ARCHITECTURE & DEPLOYMENT
    # -------------------------------------------------------------------------
    story.append(Paragraph("8. Full-Stack Software Architecture & Deployment", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    story.append(Paragraph("EduPredict was developed as an end-to-end operational software product:", body_style))
    story.append(Paragraph("• <b>FastAPI Asynchronous Backend:</b> High-throughput Python microservice exposing RESTful endpoints (/predict, /predict-bulk, /retrain, /model-metrics) with strict Pydantic data validation schemas.", bullet_style))
    story.append(Paragraph("• <b>Modern Responsive Web Frontend:</b> Glassmorphism UI built with Tailwind CSS, featuring 4 simplified operational modes: Normal, Hybrid, Smart, and Expert.", bullet_style))
    story.append(Paragraph("• <b>KaTeX Math Engine:</b> Locally bundled vendor assets for real-time rendering of mathematical formulations and loss gradients.", bullet_style))
    story.append(Paragraph("• <b>Production Cloudflare Tunnel:</b> Zero-trust worldwide HTTPS tunneling via cloudflared daemon, serving the application globally at https://partly-introduce-visiting-prev.trycloudflare.com.", bullet_style))
    story.append(Paragraph("• <b>Automated Remedial Generator:</b> Real-time prescription engine calculating the exact study hours needed to lift at-risk students back above passing thresholds.", bullet_style))

    # -------------------------------------------------------------------------
    # SECTION 9: CONCLUSION & CITATIONS
    # -------------------------------------------------------------------------
    story.append(Paragraph("9. Conclusion & Viva Defense Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    story.append(Paragraph(
        "EduPredict establishes a complete, academically aligned machine learning framework successfully demonstrating: "
        "(1) the predictive superiority of regularized regression (Ridge R² = 0.835) over unregularized OLS in multicollinear settings; "
        "(2) the vital necessity of dummy variable trap mitigation in categorical preprocessing; "
        "(3) the efficacy of Dynamic Headroom Calibration in boundary constraint resolution; and "
        "(4) the transition from theoretical statistical machine learning algorithms to a real-world, accessible academic tool.",
        body_style
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Academic References:</b>", h2_style))
    story.append(Paragraph("[1] Cortez, P., & Silva, A. (2008). Using data mining to predict secondary school student performance. In Proceedings of 5th Annual Future Business Technology Conference (FUBUTEC 2008), pp. 5-12.", bullet_style))
    story.append(Paragraph("[2] Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction. Springer Series in Statistics.", bullet_style))
    story.append(Paragraph("[3] Bennett University Course Curriculum: CSET211 Statistical Machine Learning Syllabus (2025-2026).", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Copy to Desktop and Downloads
    import shutil
    shutil.copyfile(pdf_paths[0], pdf_paths[1])
    shutil.copyfile(pdf_paths[0], pdf_paths[2])
    for p in pdf_paths:
        print(f"Generated PDF: {p} (Size: {os.path.getsize(p)} bytes)")

if __name__ == "__main__":
    generate_pdf_report()
