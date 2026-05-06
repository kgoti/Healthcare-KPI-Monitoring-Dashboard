# 🏥 Healthcare KPI Monitoring Dashboard

**Tools:** Python · SQL · Power BI · DAX
**Domain:** Healthcare / Hospital Operations

---

## 📌 Project Overview

Builds an operational KPI dashboard for hospital management, tracking patient safety, capacity, and financial metrics across 8 departments.

Healthcare is one of Germany's largest sectors (AOK, Barmer, Charité, Helios, Asklepios). A domain-specific analytics project signals both technical skill and industry awareness.

---

## 📁 Repository Structure

```
4_healthcare_kpi/
│
├── data/
│   ├── patients.csv         # 5,000 patients (demographics, insurance)
│   ├── admissions.csv       # 13,852 admissions with LOS, wait time, costs
│   └── bed_occupancy.csv    # 2,920 daily bed occupancy records
│
├── python/
│   └── generate_data.py     # Dataset generator
│
├── sql/
│   └── analysis_queries.sql # 8 KPI queries
│
└── README.md
```

---

## 📊 Key KPIs Tracked

| KPI                          | Definition                                      | Target     |
|-----------------------------|--------------------------------------------------|------------|
| Bed Occupancy Rate          | Occupied / Total beds × 100                     | 80–90%     |
| Average Length of Stay (LOS)| Discharge date − Admission date                  | Dept-based |
| 30-Day Readmission Rate     | Re-admitted within 30 days of discharge          | < 10%      |
| Emergency Wait Time         | Time from arrival to first clinical contact      | < 60 min   |
| Mortality Rate              | Deceased discharges / Total admissions × 100     | < 2%       |
| Avg Treatment Cost          | Total cost / Admissions                          | Benchmarked |

---

## 🏗 Data Model

```
patients ─────┐
              ├──→ admissions (fact)
bed_occupancy  └──→ (joined on patient_id)
```

---

## 🚀 How to Run

```bash
# Generate datasets
python python/generate_data.py

# Run SQL analysis
# Load CSVs into MySQL/PostgreSQL, then run sql/analysis_queries.sql

# Power BI
# Import all 3 CSVs → create relationships → build dashboard
```

## 💡 Power BI Dashboard Pages

1. **Executive Overview** - Admissions, LOS, readmission rate KPI cards
2. **Bed Occupancy** - Heatmap by department × day, capacity alerts
3. **Emergency Performance** - Wait times, breach rates, trend
4. **Patient Demographics** - Age group, insurance type, cost breakdown
5. **Department Deep Dive** - Slicer-driven per-department analysis

---

*Built as part of a Data & BI Analyst portfolio targeting the German job market.*
