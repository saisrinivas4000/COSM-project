import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.weightstats import ztest
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------
# LOAD DATASET
# ---------------------------
df = pd.read_csv("unified_student_dataset.csv")

# Create output folders
OUT = Path("output_tests")
FIG = OUT / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)


def save_fig(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ================================================================
# 1️⃣ ONE-SAMPLE Z TEST (Mean Math Score vs Hypothesized Mean=75)
# ================================================================
def one_sample_z_test():
    scores = df["math_score"].values
    hypothesized_mean = 75

    z_stat, p_val = ztest(scores, value=hypothesized_mean)

    # Plot
    fig, ax = plt.subplots()
    ax.hist(scores, bins=20, alpha=0.7)
    ax.axvline(scores.mean(), color="red", label="Sample Mean")
    ax.axvline(hypothesized_mean, color="green", label="Hypothesized Mean")
    ax.legend()
    ax.set_title("One-Sample Z Test – Math Score")
    save_fig(fig, "one_sample_z_test")

    return {
        "test": "One-sample Z-test",
        "z_stat": float(z_stat),
        "p_value": float(p_val),
        "sample_mean": float(scores.mean())
    }


# ================================================================
# 2️⃣ ONE-SAMPLE T TEST (Mean Study Hours Before Coaching vs Mean=6)
# ================================================================
def one_sample_t_test():
    before = df["study_before"].values
    hypothesized_mean = 6

    t_stat, p_val = stats.ttest_1samp(before, hypothesized_mean)

    # Plot
    fig, ax = plt.subplots()
    ax.hist(before, bins=20, alpha=0.7)
    ax.axvline(before.mean(), color="red", label="Sample Mean")
    ax.axvline(hypothesized_mean, color="green", label="Hypothesized Mean")
    ax.legend()
    ax.set_title("One-Sample T Test – Study Hours Before")
    save_fig(fig, "one_sample_t_test")

    return {
        "test": "One-sample T-test",
        "t_stat": float(t_stat),
        "p_value": float(p_val),
        "sample_mean": float(before.mean())
    }


# ================================================================
# 3️⃣ TWO-SAMPLE T TEST (Male vs Female Math Scores)
# ================================================================
def two_sample_t_test():
    male = df[df["gender"] == "M"]["math_score"].values
    female = df[df["gender"] == "F"]["math_score"].values

    t_stat, p_val = stats.ttest_ind(male, female, equal_var=False)

    # Plot
    fig, ax = plt.subplots()
    ax.hist(male, bins=20, alpha=0.6, label="Male")
    ax.hist(female, bins=20, alpha=0.6, label="Female")
    ax.legend()
    ax.set_title("Two-Sample T Test – Gender Math Scores")
    save_fig(fig, "two_sample_t_test")

    return {
        "test": "Two-sample T-test",
        "t_stat": float(t_stat),
        "p_value": float(p_val),
        "male_mean": float(male.mean()),
        "female_mean": float(female.mean())
    }


# ================================================================
# 4️⃣ F TEST (Variance Difference Between School A & B)
# ================================================================
def f_test():
    A = df[df["school"] == "A"]["math_score"].values
    B = df[df["school"] == "B"]["math_score"].values

    varA = np.var(A, ddof=1)
    varB = np.var(B, ddof=1)

    F = varA / varB
    df1 = len(A) - 1
    df2 = len(B) - 1

    if F > 1:
        p_value = 2 * (1 - stats.f.cdf(F, df1, df2))
    else:
        p_value = 2 * stats.f.cdf(F, df1, df2)

    # Plot
    fig, ax = plt.subplots()
    ax.boxplot([A, B], labels=["School A", "School B"])
    ax.set_title("F Test – Variances of Math Scores")
    save_fig(fig, "f_test")

    return {
        "test": "F-test (variance)",
        "F_stat": float(F),
        "p_value": float(p_value),
        "var_A": float(varA),
        "var_B": float(varB)
    }


# =========================================================================
# 5️⃣ Z TEST FOR DIFFERENCE BETWEEN TWO MEANS (School A vs School B Means)
# =========================================================================
def z_test_two_means():
    A = df[df["school"] == "A"]["math_score"].values
    B = df[df["school"] == "B"]["math_score"].values

    z_stat, p_val = ztest(A, B)

    # Plot
    fig, ax = plt.subplots()
    ax.hist(A, bins=20, alpha=0.6, label="School A")
    ax.hist(B, bins=20, alpha=0.6, label="School B")
    ax.legend()
    ax.set_title("Z Test for Difference Between Two Means – Math Scores")
    save_fig(fig, "z_test_two_means")

    return {
        "test": "Z-test for Difference Between Two Means",
        "z_stat": float(z_stat),
        "p_value": float(p_val),
        "mean_A": float(A.mean()),
        "mean_B": float(B.mean())
    }


# ================================================================
# RUN ALL TESTS
# ================================================================
def main():
    results = []
    results.append(one_sample_z_test())
    results.append(one_sample_t_test())
    results.append(two_sample_t_test())
    results.append(f_test())
    results.append(z_test_two_means())

    # Save results
    with open(OUT / "results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n\n")

    print("All tests completed! Check the output_tests/ folder.")


if __name__ == "__main__":
    main()
