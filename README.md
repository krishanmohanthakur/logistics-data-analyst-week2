# Logistics Data Analyst – Week 2

## Data Collection, Cleaning and Preprocessing for Logistics Analysis

### Project Overview

This project is part of the Yuva Intern Logistics Data Analyst Internship – Week 2 task.

The objective is to develop a systematic data collection, cleaning, and preprocessing pipeline for logistics analysis using Python and Pandas.

The Brazilian E-Commerce Public Dataset by Olist is used as the reference dataset.

---

## Objectives

- Understand logistics-related datasets and their structure.
- Identify missing values and data quality issues.
- Detect duplicate and inconsistent records.
- Convert and standardize date and time fields.
- Create logistics-related features.
- Detect potential outliers using the IQR method.
- Apply Min-Max normalization to numerical variables.
- Prepare data for further analysis and visualization.

---

## Dataset

Dataset Used:

Brazilian E-Commerce Public Dataset by Olist

The dataset contains information related to:

- Orders
- Order Items
- Customers
- Sellers
- Products
- Payments
- Reviews
- Geolocation
- Product Categories

The dataset contains approximately 100,000 e-commerce orders from Brazil.

Raw dataset files are not uploaded to this repository.

---

## Data Preprocessing Workflow

The preprocessing workflow follows these steps:

1. Data Collection
2. Dataset Inspection
3. Data Quality Assessment
4. Missing Value Analysis
5. Duplicate Detection
6. Date and Time Conversion
7. Data Cleaning
8. Feature Engineering
9. Outlier Detection
10. Data Normalization
11. Validation
12. Preparation for Further Analysis

---

## Data Cleaning

### Missing Values

Different strategies are used depending on the type of data.

- Review text → `No comment`
- Product category → `Unknown`
- Numerical product attributes → Median imputation where required
- Delivery timestamps → Retained as missing when delivery did not occur or information was unavailable

Missing values are not removed blindly because some missing logistics events can be legitimate.

---

## Duplicate Detection

Exact duplicate records are checked before analysis.

Special attention is given to the geolocation dataset because duplicate location records can affect location-based analysis.

Business-level repeated records such as multiple products within one order are not treated as duplicates automatically.

---

## Date and Time Processing

Order timestamp fields are converted into proper datetime format using Pandas.

Important fields include:

- Order purchase timestamp
- Order approval timestamp
- Carrier delivery date
- Customer delivery date
- Estimated delivery date

---

## Logistics Feature Engineering

### Delivery Time

Delivery time is calculated as:

Delivery Time = Customer Delivery Date − Order Purchase Date

### Delivery Delay

Delivery delay is calculated as:

Delivery Delay = Actual Delivery Date − Estimated Delivery Date

These features can be used to analyse delivery performance and late deliveries.

---

## Outlier Detection

The Interquartile Range (IQR) method is used for detecting potential outliers.

Formula:

IQR = Q3 − Q1

Lower Bound = Q1 − 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR

Outliers are flagged for investigation rather than automatically deleted because extreme logistics values may represent genuine business cases.

---

## Normalization

Min-Max normalization is applied to selected numerical variables such as:

- Price
- Freight Value

Formula:

X_normalized = (X − X_min) / (X_max − X_min)

Original values are retained for business interpretation.

---

## Python Technologies

The project uses:

- Python
- Pandas
- NumPy

Main Python operations include:

- `read_csv()`
- `isna()`
- `fillna()`
- `drop_duplicates()`
- `to_datetime()`
- Quantile / IQR calculations
- Feature engineering
- Min-Max normalization

---

## Repository Contents

```text
logistics-data-analyst-week2/
│
├── README.md
├── week2_logistics_preprocessing.py
├── Week2_Logistics_Data_Preprocessing_Report.docx
├── Week2_Olist_Dataset_Profile.csv
└── Week2_Olist_Outlier_Analysis.csv
