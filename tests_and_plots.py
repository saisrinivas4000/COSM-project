#!/usr/bin/env python3
"""
tests_and_plots.py

Updated for professional datasets:
- student_math_scores.csv
- heart_patient_cholesterol.csv
- factory_machine_weights.csv

Outputs:
 - output/results.txt
 - output/figures/*.png

Requires: numpy, pandas, scipy, statsmodels, matplotlib, seaborn (optional)
"""
import os
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.weightstats import ztest
import matplotlib.pyplot as plt

OUT = Path("output")
FIG = OUT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

# ---------- utility functions ----------
def cohen_d_independent(x, y):
    """Cohen's d for independent samples (pooled sd)"""
    nx, ny = len(x), len(y)
    mx, my = np.mean(x), np.mean(y)
    vx, vy = np.var(x, ddof=1), np.var(y, ddof=1)
    pool_sd = np.sqrt(((nx-1)*vx + (ny-1)*vy) / (nx+ny-2))
    return (mx - my) / pool_sd

def cohen_d_paired(a, b):
    """Cohen's d for paired samples using sd of differences"""
    diff = a - b
    return np.mean(diff) / np.std(diff, ddof=1)

def two_tailed_from_z(z):
    """two-sided p-value from z-stat"""
    return 2 * stats.norm.sf(abs(z))

def save_fig(fig, name):
    path = FIG / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)

# ---------- 1) T-test: student_math_scores.csv (independent) ----------
def analyze_students(path="student_math_scores.csv"):
    df = pd.read_csv(path)
    # sanity
    assert {'student_id', 'teaching_method', 'math_score'} <= set(df.columns)

    a = df.loc[df['teaching_method'] == 'A', 'math_score'].dropna().values
    b = df.loc[df['teaching_method'] == 'B', 'math_score'].dropna().values

    # Welch's t-test
    t_stat, p_val = stats.ttest_ind(a, b, equal_var=False)
    mean_a, mean_b = a.mean(), b.mean()
    d = cohen_d_independent(a, b)

    # plots: hist, box
    fig, ax = plt.subplots()
    ax.hist(a, bins=15, alpha=0.6, label='Method A')
    ax.hist(b, bins=15, alpha=0.6, label='Method B')
    ax.legend()
    ax.set_title("Student Math Scores - Histogram")
    save_fig(fig, "students_hist")

    fig, ax = plt.subplots()
    ax.boxplot([a, b], labels=['Method A', 'Method B'])
    ax.set_title("Student Math Scores - Boxplot")
    save_fig(fig, "students_box")

    return {
        "test": "Welch t-test (students)",
        "t_stat": float(t_stat),
        "p_value": float(p_val),
        "mean_A": float(mean_a),
        "mean_B": float(mean_b),
        "cohens_d": float(d),
        "n_A": len(a),
        "n_B": len(b)
    }

# ---------- 2) Paired analysis: heart_patient_cholesterol.csv ----------
def analyze_heart(path="heart_patient_cholesterol.csv"):
    df = pd.read_csv(path)
    assert {'patient_id', 'cholesterol_before', 'cholesterol_after'} <= set(df.columns)
    before = df['cholesterol_before'].dropna().values
    after = df['cholesterol_after'].dropna().values
    if len(before) != len(after):
        # align by patient_id if mismatched lengths
        df = df.dropna(subset=['cholesterol_before','cholesterol_after'])
        before = df['cholesterol_before'].values
        after = df['cholesterol_after'].values

    # paired t-test
    t_stat, p_val = stats.ttest_rel(before, after)
    mean_diff = np.mean(before - after)
    sd_diff = np.std(before - after, ddof=1)
    n = len(before)
    # paired z-test approximation (large n) using mean diff and sd of differences
    z_stat = mean_diff / (sd_diff / np.sqrt(n))
    z_p = two_tailed_from_z(z_stat)

    d = cohen_d_paired(before, after)

    # plots: paired scatter and hist of differences
    fig, ax = plt.subplots()
    ax.scatter(before, after, alpha=0.4)
    lims = [min(before.min(), after.min()), max(before.max(), after.max())]
    ax.plot(lims, lims, 'k--', linewidth=0.8)
    ax.set_xlabel("Cholesterol Before")
    ax.set_ylabel("Cholesterol After")
    ax.set_title("Cholesterol: Before vs After (paired)")
    save_fig(fig, "chol_scatter")

    diffs = before - after
    fig, ax = plt.subplots()
    ax.hist(diffs, bins=25, alpha=0.7)
    ax.set_title("Cholesterol Differences (before - after)")
    save_fig(fig, "chol_diff_hist")

    return {
        "test": "Paired (cholesterol)",
        "paired_t_stat": float(t_stat),
        "paired_t_p": float(p_val),
        "paired_z_stat": float(z_stat),
        "paired_z_p": float(z_p),
        "mean_diff": float(mean_diff),
        "sd_diff": float(sd_diff),
        "cohens_d_paired": float(d),
        "n": n
    }

# ---------- 3) F-test: factory_machine_weights.csv ----------
def analyze_factory(path="factory_machine_weights.csv"):
    df = pd.read_csv(path)
    assert {'unit_id', 'machine', 'product_weight'} <= set(df.columns)
    x = df.loc[df['machine'] == 'A', 'product_weight'].dropna().values
    y = df.loc[df['machine'] == 'B', 'product_weight'].dropna().values

    varx = np.var(x, ddof=1)
    vary = np.var(y, ddof=1)
    f_stat = varx / vary
    dfn = len(x) - 1
    dfd = len(y) - 1
    # two-tailed p-value for F
    if f_stat > 1:
        p = 2 * (1 - stats.f.cdf(f_stat, dfn, dfd))
    else:
        p = 2 * stats.f.cdf(f_stat, dfn, dfd)

    # Levene's test for equality of variances (more robust)
    levene_stat, levene_p = stats.levene(x, y)

    # plots: hist + box
    fig, ax = plt.subplots()
    ax.hist(x, bins=20, alpha=0.6, label='Machine A')
    ax.hist(y, bins=20, alpha=0.6, label='Machine B')
    ax.legend()
    ax.set_title("Factory Product Weights - Histogram")
    save_fig(fig, "factory_hist")

    fig, ax = plt.subplots()
    ax.boxplot([x, y], labels=['Machine A', 'Machine B'])
    ax.set_title("Factory Product Weights - Boxplot")
    save_fig(fig, "factory_box")

    return {
        "test": "F-test (variance ratio)",
        "F_stat": float(f_stat),
        "F_p_two_sided": float(p),
        "var_A": float(varx),
        "var_B": float(vary),
        "n_A": len(x),
        "n_B": len(y),
        "levene_stat": float(levene_stat),
        "levene_p": float(levene_p)
    }

# ---------- run analyses ----------
def main():
    results = []
    try:
        students_res = analyze_students("student_math_scores.csv")
        results.append(students_res)
    except Exception as e:
        results.append({"test": "students", "error": str(e)})

    try:
        heart_res = analyze_heart("heart_patient_cholesterol.csv")
        results.append(heart_res)
    except Exception as e:
        results.append({"test": "heart", "error": str(e)})

    try:
        factory_res = analyze_factory("factory_machine_weights.csv")
        results.append(factory_res)
    except Exception as e:
        results.append({"test": "factory", "error": str(e)})

    # Save results as pretty text and CSV
    out_txt = OUT / "results.txt"
    with out_txt.open("w") as f:
        for r in results:
            f.write(f"{r}\n\n")

    # also save machine readable JSON and CSV summary (helpful for GitHub)
    try:
        import json
        (OUT / "results.json").write_text(json.dumps(results, indent=2))
    except Exception:
        pass

    print("Analysis complete. Results written to:", out_txt)
    print("Figures in:", FIG)

if __name__ == "__main__":
    main()
