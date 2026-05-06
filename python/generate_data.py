"""
Healthcare KPI Dataset Generator
Generates realistic hospital operational data:
patient admissions, wait times, bed occupancy, staff, departments
"""

import csv, random
from datetime import datetime, timedelta

random.seed(55)

DEPARTMENTS  = ["Emergency","Cardiology","Orthopedics","Neurology","Oncology","General Surgery","Pediatrics","ICU"]
ADMISSION_TYPES = ["Emergency","Elective","Urgent"]
DIAGNOSES    = {
    "Emergency":       ["Chest Pain","Fracture","Stroke","Trauma","Appendicitis"],
    "Cardiology":      ["Heart Failure","Arrhythmia","Coronary Artery Disease","Hypertension","Valve Disorder"],
    "Orthopedics":     ["Hip Replacement","Knee Surgery","Spinal Disorder","Sports Injury","Fracture"],
    "Neurology":       ["Epilepsy","Migraine","MS","Parkinson's","Brain Tumor"],
    "Oncology":        ["Lung Cancer","Breast Cancer","Colon Cancer","Leukemia","Lymphoma"],
    "General Surgery": ["Gallbladder","Hernia","Appendectomy","Bowel Resection","Thyroid"],
    "Pediatrics":      ["Respiratory Infection","Fever","Asthma","Gastroenteritis","Ear Infection"],
    "ICU":             ["Sepsis","Respiratory Failure","Cardiac Arrest","Multi-organ Failure","Post-Surgery"]
}
DISCHARGE_STATUS = ["Recovered","Transferred","Against Advice","Deceased"]
DISCHARGE_WEIGHTS = [85, 8, 4, 3]
BED_CAPACITY = {"Emergency":30,"Cardiology":40,"Orthopedics":35,"Neurology":30,"Oncology":45,"General Surgery":50,"Pediatrics":25,"ICU":20}

start_date = datetime(2023, 1, 1)
patients = []
admissions = []
bed_occupancy = []
staff_roster = []

# ── 1. patients.csv ──────────────────────────────────────────────────────────
for i in range(1, 5001):
    age = int(random.gauss(52, 20))
    age = max(0, min(95, age))
    patients.append([f"P{i:05d}", random.choice(["M","F"]), age,
                     "Private" if random.random() > 0.6 else "Public",
                     random.choice(["Berlin","Hamburg","Munich","Cologne","Frankfurt","Stuttgart"])])

with open("/home/claude/projects/4_healthcare_kpi/data/patients.csv", "w", newline="") as f:
    csv.writer(f).writerows([["patient_id","gender","age","insurance_type","city"]] + patients)
print(f"patients.csv → {len(patients)} rows")

# ── 2. admissions.csv ────────────────────────────────────────────────────────
adm_id = 1
for day_offset in range(365):
    date = start_date + timedelta(days=day_offset)
    daily = random.randint(20, 55)
    for _ in range(daily):
        dept  = random.choice(DEPARTMENTS)
        atype = random.choice(ADMISSION_TYPES)
        if dept == "ICU":
            atype = "Emergency"
        los   = max(1, int(random.gauss(5.5, 3.2)))  # length of stay (days)
        wait  = random.randint(5, 240) if atype == "Emergency" else random.randint(0, 60)
        disch_status = random.choices(DISCHARGE_STATUS, DISCHARGE_WEIGHTS)[0]
        readmit = 1 if random.random() < 0.08 else 0
        adm_date = date
        dis_date = date + timedelta(days=los)
        pat  = random.choice(patients)
        admissions.append([
            f"ADM{adm_id:06d}", pat[0], adm_date.strftime("%Y-%m-%d"),
            dis_date.strftime("%Y-%m-%d"), dept, atype,
            random.choice(DIAGNOSES[dept]), los, wait, disch_status, readmit,
            round(random.uniform(500, 25000), 2)
        ])
        adm_id += 1

with open("/home/claude/projects/4_healthcare_kpi/data/admissions.csv", "w", newline="") as f:
    csv.writer(f).writerows([["admission_id","patient_id","admission_date","discharge_date","department",
                               "admission_type","diagnosis","length_of_stay_days","wait_time_min",
                               "discharge_status","readmitted_30d","treatment_cost"]] + admissions)
print(f"admissions.csv → {len(admissions)} rows")

# ── 3. bed_occupancy.csv ─────────────────────────────────────────────────────
for day_offset in range(365):
    date = start_date + timedelta(days=day_offset)
    for dept, capacity in BED_CAPACITY.items():
        occupied = random.randint(int(capacity*0.5), capacity)
        bed_occupancy.append([date.strftime("%Y-%m-%d"), dept, capacity, occupied,
                               round(occupied/capacity*100, 1)])

with open("/home/claude/projects/4_healthcare_kpi/data/bed_occupancy.csv", "w", newline="") as f:
    csv.writer(f).writerows([["date","department","total_beds","occupied_beds","occupancy_rate_pct"]] + bed_occupancy)
print(f"bed_occupancy.csv → {len(bed_occupancy)} rows")
print("All datasets generated.")
