# Dataset Validation & Schema Guide

This document specifies the validation architecture and test cases for testing
the **AI-Powered Data Cleaning Assistant** on complex, noisy tabular datasets.

---

## 1. Validation Dataset Schema Specification

The pipeline handles dirty, unstandardized CSV tables with heterogeneous
types:

* `transaction_id`: Alphanumeric IDs. Stripped and deduplicated.
* `customer_name`: Name strings with surrounding whitespace.
* `country`: Category values with missing tokens (`N/A`, `null`).
* `transaction_date`: Mixed date formats normalized to `YYYY-MM-DD`.
* `product_category`: Category strings with missing indicators.
* `quantity`: Numeric quantities with extreme outliers.
* `unit_price`: Multi-currency strings (`$`, `€`, `£`, `¥`).
* `discount_pct`: Discount rates with missing strings (`null`, `-999`).
* `total_amount`: Multi-currency, negative accounting, and outliers.
* `payment_status`: Status with missing cells in jagged rows.

---

## 2. Injected Anomalies & Cleaning Strategies

### 1. Duplicate Records
* **Injected:** Duplicated records in the raw input file.
* **Resolution:** Full-row and primary-key deduplication preserving the
  first occurrence.

### 2. Multi-Currency & Accounting Formats
* **Injected:** Strings formatted like `$1,250.00`, `€120.00`, `£850.00`,
  and accounting negatives `($150.00)`.
* **Resolution:** Stripped and converted to mathematical floats.

### 3. Statistical Outliers
* **Injected:** Extreme non-parametric anomalies (e.g. `$999,999,999.00`).
* **Resolution:** Calculates quartiles $Q_1, Q_3$ and bounds values to
  $[Q_1 - 1.5 \times IQR, \, Q_3 + 1.5 \times IQR]$.

### 4. Missing Values & Jagged Rows
* **Injected:** Missing values marked by `N/A`, `null`, or truncated rows.
* **Resolution:** Aligned to schema length and imputed using median
  (numeric) or mode (categorical).

---

## 3. Execution Instructions

```bash
# Clean any custom dataset directly
python3 -m ai_pair_programming.data_cleaner.main /path/to/dataset.csv
```
