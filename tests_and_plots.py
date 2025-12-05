import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.weightstats import ztest

# Load dataset
df = pd.read_csv("unified_student_dataset.csv")

# -----------------------------
# Utility functions
# -----------------------------
def one_sample_z_test(column, hypothesized_mean):
    data = df[column].dropna()
    z_stat, p_val = ztest(data, value=hypothesized_mean)
    return z_stat, p_val, data.mean()

def one_sample_t_test(column, hypothesized_mean):
    data = df[column].dropna()
    t_stat, p_val = stats.ttest_1samp(data, hypothesized_mean)
    return t_stat, p_val, data.mean()

def two_sample_t_test(column, group_col, group1, group2):
    g1 = df[df[group_col] == group1][column].dropna()
    g2 = df[df[group_col] == group2][column].dropna()
    t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
    return t_stat, p_val, g1.mean(), g2.mean()

def f_test(column, group_col, group1, group2):
    g1 = df[df[group_col] == group1][column].dropna()
    g2 = df[df[group_col] == group2][column].dropna()
    var1, var2 = g1.var(ddof=1), g2.var(ddof=1)
    F = var1 / var2
    dfn, dfd = len(g1)-1, len(g2)-1
    if F > 1:
        p_val = 2 * (1 - stats.f.cdf(F, dfn, dfd))
    else:
        p_val = 2 * stats.f.cdf(F, dfn, dfd)
    return F, p_val, var1, var2

def z_test_two_means(column, group_col, group1, group2):
    g1 = df[df[group_col] == group1][column].dropna()
    g2 = df[df[group_col] == group2][column].dropna()
    z_stat, p_val = ztest(g1, g2)
    return z_stat, p_val, g1.mean(), g2.mean()


# ------------------------------------------
# USER INTERACTIVE MENU
# ------------------------------------------
print("\n📌 AVAILABLE COLUMNS:")
for col in df.columns:
    print(" -", col)

print("\n📌 TEST OPTIONS:\n"
      "1. One-sample Z Test\n"
      "2. One-sample T Test\n"
      "3. Two-sample T Test\n"
      "4. F Test (variance)\n"
      "5. Z Test for Difference Between Two Means\n")

choice = int(input("Enter the test number you want to perform: "))

# ------------------------------------------
# ONE-SAMPLE TESTS
# ------------------------------------------
if choice in [1, 2]:
    col = input("Enter the column name to test: ")
    hypo = float(input("Enter the hypothesized mean value: "))

    if choice == 1:
        z, p, mean = one_sample_z_test(col, hypo)
        print("\n📌 ONE SAMPLE Z TEST RESULT")
        print("Column:", col)
        print("Sample Mean:", mean)
        print("Z-Statistic:", z)
        print("p-value:", p)

    else:
        t, p, mean = one_sample_t_test(col, hypo)
        print("\n📌 ONE SAMPLE T TEST RESULT")
        print("Column:", col)
        print("Sample Mean:", mean)
        print("T-Statistic:", t)
        print("p-value:", p)

# ------------------------------------------
# TWO-SAMPLE TESTS
# ------------------------------------------
else:
    col = input("Enter the measurement column: ")
    group_col = input("Enter the grouping column: ")
    g1 = input("Enter first group value: ")
    g2 = input("Enter second group value: ")

    if choice == 3:
        t, p, m1, m2 = two_sample_t_test(col, group_col, g1, g2)
        print("\n📌 TWO SAMPLE T TEST RESULT")
        print("Means:", m1, "(Group:", g1, ")  vs", m2, "(Group:", g2, ")")
        print("T-Statistic:", t)
        print("p-value:", p)

    elif choice == 4:
        F, p, v1, v2 = f_test(col, group_col, g1, g2)
        print("\n📌 F TEST RESULT")
        print("Variances:", v1, "(Group:", g1, ")  vs", v2, "(Group:", g2, ")")
        print("F-Statistic:", F)
        print("p-value:", p)

    elif choice == 5:
        z, p, m1, m2 = z_test_two_means(col, group_col, g1, g2)
        print("\n📌 Z TEST FOR DIFFERENCE OF TWO MEANS")
        print("Means:", m1, "(Group:", g1, ")  vs", m2, "(Group:", g2, ")")
        print("Z-Statistic:", z)
        print("p-value:", p)

print("\n✅ Test completed successfully!")
