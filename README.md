# 🏥 ClearCare: Healthcare Pricing Transparency Platform

**Course**: BUAN 6390.002 | **Instructor**: Prof. Mandar Samant  
**Mentor**: Mr. Vijay Koneru  

---

## 📌 Overview

ClearCare is a data-driven platform built to simplify and standardize U.S. hospital pricing data to help patients make **cost-conscious healthcare decisions**. It tackles the challenge of fragmented and opaque healthcare pricing data by providing a robust pipeline—from raw data ingestion and standardization to dynamic, patient-facing dashboards—enabling transparency, comparability, and informed healthcare decision-making.

---

## 🎯 Objectives

- 🔍 Identify and clean inconsistently formatted hospital price files (CSV, JSON).
- 🧹 Standardize key fields such as CPT billing codes, addresses, and negotiated charges.
- 🏥 Model relationships between hospitals, procedures, and insurance plans for robust analysis.
- 📊 Build interactive visualizations to empower patients to compare charges across **regions**, **providers**, and **insurance networks**.

---

## 🧾 Final Output Schema

The cleaned dataset contains the following standardized columns in the specified order:

| **Column Name**            | **Description**                                                                 |
|----------------------------|---------------------------------------------------------------------------------|
| `hospital_name`            | Name of the hospital providing the service                                     |
| `street_address`           | Parsed and standardized street address of the hospital                         |
| `city`                     | City where the hospital is located                                             |
| `state`                    | Two-letter state abbreviation                                                  |
| `zip_code`                 | ZIP or postal code of the hospital location                                    |
| `description`              | Description of the billed procedure or service                                 |
| `billing_code`             | CPT or internal billing code used to identify the procedure                    |
| `billing_code_type`        | Type of billing code (e.g., CPT )                              |
| `standard_charge`          | Published gross charge for the procedure/service                               |
| `discounted_cash_charge`   | Discounted rate offered to self-pay patients                                   |
| `payer_name`               | Name of the insurance provider                                                 |
| `plan_name`                | Specific plan under the listed insurance provider                              |
| `negotiated_dollar`        | Dollar amount negotiated between hospital and insurer                          |
| `negotiated_percentage`    | Percentage of the standard charge negotiated (if provided)                     |
| `estimated_amount`         | Estimated patient out-of-pocket cost (if disclosed by the hospital)            |
| `min_charge`               | Minimum charge negotiated under this plan                                      |
| `max_charge`               | Maximum charge negotiated under this plan                                      |

- This standardized schema enables consistent loading into PostgreSQL and easy integration into Tableau dashboards for cross-provider analysis.

---
## ❗ Problem Statement

Despite regulatory requirements:
- Hospitals publish pricing data in inconsistent structures.
- Charge types (e.g., gross charge, discounted cash price, negotiated rate) are often not user-friendly.
- Patients lack a unified view to compare prices and choose providers based on both location and insurer coverage.

---

## ⚙️ Tech Stack

| Layer               | Tools Used                                           |
|--------------------|------------------------------------------------------|
| **Programming**     | Python (`pandas`, `regex`, `os`, `json`, `glob`)     |
| **Database**        | PostgreSQL (Normalized schema using ERD)            |
| **Data Infrastructure** | Docker (local database deployment), Tailscale (secure remote access) |
| **Visualization**   | Tableau, Power BI                                    |
| **Schema Modeling** | dbdiagram.io                                         |

---

## 🔄 Project Pipeline

### 1. **Data Collection**
- Pulled price transparency files from hospital websites across **California**, **Florida**, **Oregon**, and **Washington**.
- Handled both JSON and CSVs containing negotiated prices and metadata.

### 2. **Data Cleaning & ETL**
- **Automated Python Scripts**:
  - Extracted CPT-coded charges from files with nested and scattered column structures.
  - Used regex to parse billing code types and identify valid entries.
  - Standardized address fields by detecting patterns and splitting them into:
    - `street_address`, `city`, `state`, `zip_code`
  - Converted wide-format payer-plan negotiated prices into a normalized tall format.

### 3. **Data Modeling**
- Created a **relational schema** to model:
  - Hospitals
  - Procedures
  - Insurance providers and plans
  - Charges (joining the three)
- Tools: **dbdiagram.io**, PostgreSQL
- ERD enabled efficient joins and queries, ensuring analytical depth and speed.

### 4. **Data Storage**
- Used **PostgreSQL** for structured storage and complex querying.
- Deployed via **Docker** to ensure consistency across team environments.
- Integrated **Tailscale** for secure, remote team access to the local database.

### 5. **Data Visualization**
- Built state-wise dashboards in **Tableau** to:
  - Compare costs by procedure and hospital
  - Analyze variation by region and insurer
  - Visualize negotiated charges vs standard prices

Dashboards were built for:
- **California**
- **Florida**
- **Oregon & Washington**

---

## ✅ Key Outcomes

- 🚀 Reduced data preparation time via fully automated cleaning scripts.
- 🧱 Delivered a **scalable, replicable pipeline** for adding more hospital datasets.
- 🔐 Ensured secure team collaboration using **Docker + Tailscale**.
- 📊 Published **interactive dashboards** for real-world impact on healthcare decision-making.
- 📥 Advanced **price transparency** and **patient empowerment** in healthcare.

---


## 📚 Resources & Acknowledgments

- PostgreSQL Docs, Docker Docs, Tableau Public
- Special thanks to **Prof. Mandar Samant** and **Mr. Vijay Koneru** for their mentorship and guidance.
