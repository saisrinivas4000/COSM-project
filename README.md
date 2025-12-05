# 📊 Statistical Analysis on Unified Student Dataset

This project performs five major hypothesis tests on a unified dataset containing academic and behavioral information of students from two schools. The tests include:

- **One-sample Z-test**
- **One-sample T-test**
- **Two-sample (independent) T-test**
- **F-test for variance comparison**
- **Z-test for difference between two means**

The dataset and scripts are designed for educational research, statistical modeling, and data analysis demonstrations.

---

## 📁 Dataset: `unified_student_dataset.csv`

### **Column Descriptions**

| Column Name     | Description |
|-----------------|-------------|
| `student_id`    | Unique student identifier |
| `school`        | School ID (A or B) |
| `gender`        | Student gender (M/F) |
| `age`           | Age of the student (15–18 years) |
| `attendance`    | Attendance rate (0–1) |
| `study_before`  | Weekly study hours before coaching |
| `study_after`   | Weekly study hours after coaching |
| `math_score`    | Final math exam score (0–100) |

---

# 📐 Hypothesis Tests Performed

Below are all the statistical tests run on the dataset, with **columns used**, **test purpose**, and **results summary**.

---

## 🧪 1️⃣ One-Sample Z-Test  
**Goal:** Test if the mean math score differs from the benchmark **75**.

**Column Used:** `math_score`

### **Results**
- **Sample Mean:** 70.2968  
- **Z Statistic:** -5.8572  
- **p-value:** 4.7065 × 10⁻⁹  

### **Conclusion:**  
Students scored **significantly lower** than the expected benchmark.

---

## 🧪 2️⃣ One-Sample T-Test  
**Goal:** Check if students study **6 hours per week** before coaching.

**Column Used:** `study_before`

### **Results**
- **Sample Mean:** 5.4666  
- **T Statistic:** -2.7522  
- **p-value:** 0.00704  

### **Conclusion:**  
Students study **significantly less** than 6 hours per week.

---

## 🧪 3️⃣ Two-Sample T-Test (Independent)  
**Goal:** Compare math performance between **male and female** students.

**Columns Used:**  
- `math_score`  
- `gender`  

### **Results**
- **Male Mean:** 70.4573  
- **Female Mean:** 70.1298  
- **T Statistic:** 0.2021  
- **p-value:** 0.8403  

### **Conclusion:**  
There is **no significant difference** in math scores based on gender.

---

## 🧪 4️⃣ F-Test (Variance Comparison)  
**Goal:** Compare variance in math scores between **School A** and **School B**.

**Columns Used:**  
- `math_score`  
- `school`  

### **Results**
- **Variance (School A):** 83.1642  
- **Variance (School B):** 47.0979  
- **F Statistic:** 1.7658  
- **p-value:** 0.04919  

### **Conclusion:**  
School A has **significantly higher variance** in student scores.

---

## 🧪 5️⃣ Z-Test for Difference Between Two Means  
**Goal:** Compare average math scores between **School A** and **School B**.

**Columns Used:**  
- `math_score`  
- `school`  

### **Results**
- **Mean A:** 70.3558  
- **Mean B:** 70.2378  
- **Z Statistic:** 0.0731  
- **p-value:** 0.9417  

### **Conclusion:**  
The two schools have **nearly identical** average math performance.

---

# 📂 Output Files

Running the analysis script (`run_all_tests.py`) generates the following:

**output_tests**
│

├── results.txt

└── **figures**

├── one_sample_z_test.png

├── one_sample_t_test.png

├── two_sample_t_test.png

├── f_test.png

└── z_test_two_means.png

