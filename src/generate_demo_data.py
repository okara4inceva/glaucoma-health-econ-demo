"""
Generate simulated glaucoma demo data.

This script creates a synthetic patient-level dataset for a portfolio project.
It does not use real patient data.
"""

from pathlib import Path
import numpy as np
import pandas as pd

np.random.seed(42)

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data"
DATA_DIR.mkdir(exist_ok=True)

n = 300
ages = np.clip(np.random.normal(62, 12, n).round().astype(int), 40, 89)
gender = np.random.choice(["Female", "Male"], size=n, p=[0.52, 0.48])
family_history = np.random.choice(["Yes", "No"], size=n, p=[0.22, 0.78])
diabetes = np.random.choice(["Yes", "No"], size=n, p=[0.28, 0.72])
hypertension = np.random.choice(["Yes", "No"], size=n, p=[0.34, 0.66])

risk_score = (
    (ages >= 60).astype(int) * 2
    + (ages >= 70).astype(int)
    + (family_history == "Yes").astype(int) * 2
    + (diabetes == "Yes").astype(int)
    + (hypertension == "Yes").astype(int)
)

risk_group = np.where(risk_score >= 5, "High", np.where(risk_score >= 3, "Medium", "Low"))

iop = np.random.normal(18, 3.5, n) + (risk_group == "High") * 3 + (risk_group == "Medium") * 1.5
iop = np.clip(iop.round(1), 10, 34)

prob_glaucoma = 0.02 + (risk_group == "Medium") * 0.06 + (risk_group == "High") * 0.14 + (iop >= 24) * 0.12
confirmed = np.random.binomial(1, np.clip(prob_glaucoma, 0, 0.55), n)

stage = []
visual_field = []
oct_result = []
management = []
annual_cost = []
prod_loss = []

for c, rg, pressure in zip(confirmed, risk_group, iop):
    if c == 0:
        stage.append("No glaucoma")
        visual_field.append(np.random.choice(["Normal", "Borderline"], p=[0.85, 0.15]))
        oct_result.append(np.random.choice(["Normal", "Suspicious"], p=[0.88, 0.12]))
        management.append(np.random.choice(["Routine monitoring", "Repeat test"], p=[0.8, 0.2]))
        annual_cost.append(int(np.random.choice([300, 500, 750], p=[0.55, 0.35, 0.10])))
        prod_loss.append(0)
    else:
        st = np.random.choice(["Early", "Moderate", "Advanced"], p=[0.55, 0.30, 0.15])
        stage.append(st)
        if st == "Early":
            visual_field.append("Mild defect")
            oct_result.append(np.random.choice(["Suspicious", "Abnormal"], p=[0.45, 0.55]))
            management.append(np.random.choice(["Eye drops", "Monitoring + drops"], p=[0.75, 0.25]))
            annual_cost.append(int(np.random.normal(1500, 250)))
            prod_loss.append(int(np.random.normal(1000, 400)))
        elif st == "Moderate":
            visual_field.append("Moderate defect")
            oct_result.append("Abnormal")
            management.append(np.random.choice(["Eye drops", "Laser + drops"], p=[0.7, 0.3]))
            annual_cost.append(int(np.random.normal(3500, 600)))
            prod_loss.append(int(np.random.normal(3500, 900)))
        else:
            visual_field.append("Severe defect")
            oct_result.append("Abnormal")
            management.append(np.random.choice(["Surgery/laser", "Specialist follow-up"], p=[0.55, 0.45]))
            annual_cost.append(int(np.random.normal(6500, 1000)))
            prod_loss.append(int(np.random.normal(8000, 1800)))

df = pd.DataFrame({
    "patient_id": [f"GDEMO-{i:04d}" for i in range(1, n + 1)],
    "age": ages,
    "gender": gender,
    "family_history_glaucoma": family_history,
    "diabetes": diabetes,
    "hypertension": hypertension,
    "risk_score": risk_score,
    "risk_group": risk_group,
    "iop_mmhg": iop,
    "oct_result": oct_result,
    "visual_field_result": visual_field,
    "diagnosis": np.where(confirmed == 1, "Confirmed glaucoma", "No confirmed glaucoma"),
    "disease_stage": stage,
    "management_plan": management,
    "annual_direct_cost_aed": np.maximum(annual_cost, 0),
    "estimated_productivity_loss_aed": np.maximum(prod_loss, 0),
    "data_type": "SIMULATED - NOT REAL PATIENT DATA",
})

df.to_csv(DATA_DIR / "glaucoma_demo_patients.csv", index=False)
print(f"Saved {len(df)} simulated rows to {DATA_DIR / 'glaucoma_demo_patients.csv'}")
