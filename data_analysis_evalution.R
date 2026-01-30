library(readxl) # For importing Excel data
library(dplyr)  # For data wrangling and aggregation
library(lme4)   # For Mixed Models (GLMM/LMM)

# ------------------------------------------------------------------------------
# 1. Data Import and Preparation
# ------------------------------------------------------------------------------

# Load the datasets
# Ensure the file paths match your local directory
Curriculumrelevance <- read_excel("xxx/Dataset.xlsx", sheet = "Cleaned")
grade3_identification <- read_excel("xxx/Dataset.xlsx", sheet = "Grade 3 identification")
grade4_identification <- read_excel("xxx/Dataset.xlsx", sheet = "Grade 4 identification")

# Ensure variables are in the correct format (Numeric or Factor)
Curriculumrelevance$Qualitaet <- as.numeric(as.character(Curriculumrelevance$Qualitaet))
Curriculumrelevance$Lernplanrelevanz <- as.numeric(as.character(Curriculumrelevance$Lernplanrelevanz))


# ------------------------------------------------------------------------------
# 2. Curriculum Relevance (Fisher's Exact Test)
# ------------------------------------------------------------------------------
relevanz_table <- table(Curriculumrelevance$Source, Curriculumrelevance$Lernplanrelevanz)
contingency_table <- table(Curriculumrelevance$Source, Curriculumrelevance$Lernplanrelevanz)
print(contingency_table)
fisher_relevanz <- fisher.test(relevanz_table)
print(fisher_relevanz)


# ------------------------------------------------------------------------------
# 3. Grade Fitting (Chi-squared Test)
# ------------------------------------------------------------------------------

# 3.1 Analysis for grade 3
g3_matrix <- as.matrix(grade3_identification[, c("Correct", "Incorrect")])
rownames(g3_matrix) <- grade3_identification$Source
# Perform Pearson's Chi-squared test for Grade 3
chisq_g3 <- chisq.test(g3_matrix)
print(chisq_g3)
# Check if all expected counts > 5
print(chisq_g3$expected) 
# The expected count for real-life is 3.4, which is below 5. Therefore we ran a Fisher’s Exact test.
fisher.test(g3_matrix)

# 3.2 Analysis for grade 4
g4_matrix <- as.matrix(grade4_identification[, c("Correct", "Incorrect")])
rownames(g4_matrix) <- grade4_identification$Source
# Perform Pearson's Chi-squared test for Grade 4
chisq_g4 <- chisq.test(g4_matrix)
print(chisq_g4)
# Check if all expected counts > 5
print(chisq_g4$expected) 

# ------------------------------------------------------------------------------
# 4. Quality Analysis (Welch T-test and Wilcoxon Rank Sum Test)
# ------------------------------------------------------------------------------
# 4.1 Welch T-test: Does not assume equal variances
t_test_quality <- t.test(Qualitaet ~ Source, data = Curriculumrelevance, var.equal = FALSE)

# 4.2 Wilcoxon: Non-parametric alternative for non-Gaussian data
wilcox_quality <- wilcox.test(Qualitaet ~ Source, data = Curriculumrelevance)

print(t_test_quality)
print(wilcox_quality)

# ------------------------------------------------------------------------------
# 5. AI Identification (Z-test for Proportions)
# ------------------------------------------------------------------------------

# We have correct 16 identifications out of 28 trials
# 5.1 Manual calculation
# 5.1.1 Define summary statistics
successes <- 16 
total <- 28
p_hat <- successes / total  # Observed proportion (approx. 0.571)
p_0 <- 0.5                  # Theoretical proportion under the null hypothesis

# 5.1.2. Calculate the Z-statistic
z_score <- (p_hat - p_0) / sqrt(p_0 * (1 - p_0) / total)

# 5.1.3. Calculate the P-value (One-tailed test: alternative = "greater")
p_value <- pnorm(z_score, lower.tail = FALSE)

# 5.1.4. Output
cat("Z-score:", z_score, "\n")
cat("P-value:", p_value, "\n")

# 5.2 cross check with prop.test()
z_test_id <- prop.test(x = 16, n = 28, p = 0.5, alternative = "greater", correct = FALSE)
print(z_test_id)