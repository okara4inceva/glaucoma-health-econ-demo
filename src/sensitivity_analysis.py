"""
Run one-way sensitivity analysis and generate charts.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from run_model import INPUTS, run_model

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "outputs"
CHARTS = OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

base_results = run_model(INPUTS)
base_net = base_results["net_societal_budget_impact_aed"]

sensitivity_params = {
    "screening_cost_per_person_aed": [150, 250, 400],
    "glaucoma_prevalence_in_high_risk_group": [0.03, 0.05, 0.08],
    "early_detection_rate": [0.65, 0.80, 0.90],
    "progression_to_advanced_early_detection": [0.05, 0.10, 0.15],
    "annual_cost_advanced_glaucoma_aed": [4000, 6000, 9000],
    "annual_productivity_loss_advanced_aed": [4000, 8000, 12000],
}

rows = []
for param, values in sensitivity_params.items():
    for value in values:
        scenario = INPUTS.copy()
        scenario[param] = value
        results = run_model(scenario)
        rows.append({
            "parameter": param,
            "value": value,
            "net_societal_budget_impact_aed": results["net_societal_budget_impact_aed"],
            "incremental_direct_budget_impact_aed": results["incremental_direct_budget_impact_aed"],
            "cost_per_additional_early_case_detected_aed": results["cost_per_additional_early_case_detected_aed"],
            "change_from_base_net_societal_aed": results["net_societal_budget_impact_aed"] - base_net,
        })

sens = pd.DataFrame(rows).round(2)
sens.to_csv(OUT / "sensitivity_one_way.csv", index=False)

# Chart 1: detection comparison
plt.figure(figsize=(7, 5))
plt.bar(["Usual care", "Early detection"], [
    base_results["detected_cases_usual_care"],
    base_results["detected_cases_early_detection"],
])
plt.title("Detected Glaucoma Cases: Usual Care vs Early Detection")
plt.ylabel("Number of cases")
plt.tight_layout()
plt.savefig(CHARTS / "detection_comparison.png", dpi=200)
plt.close()

# Chart 2: budget impact
plt.figure(figsize=(8, 5))
plt.bar(
    ["Direct cost\nusual care", "Direct cost\nearly detection", "Societal cost\nusual care", "Societal cost\nearly detection"],
    [
        base_results["direct_cost_usual_care_aed"],
        base_results["direct_cost_early_detection_aed"],
        base_results["total_societal_cost_usual_care_aed"],
        base_results["total_societal_cost_early_detection_aed"],
    ],
)
plt.title("One-Year Budget Impact")
plt.ylabel("AED")
plt.tight_layout()
plt.savefig(CHARTS / "budget_impact.png", dpi=200)
plt.close()

# Chart 3: tornado-style sensitivity chart
sens_summary = (
    sens.groupby("parameter")["net_societal_budget_impact_aed"]
    .agg(["min", "max"])
    .reset_index()
)
sens_summary["range"] = sens_summary["max"] - sens_summary["min"]
sens_summary = sens_summary.sort_values("range", ascending=True)

plt.figure(figsize=(9, 6))
y = np.arange(len(sens_summary))
plt.barh(y, sens_summary["max"] - sens_summary["min"], left=sens_summary["min"])
plt.axvline(base_net, linestyle="--")
plt.yticks(y, sens_summary["parameter"])
plt.title("One-Way Sensitivity Analysis: Net Societal Budget Impact")
plt.xlabel("AED")
plt.tight_layout()
plt.savefig(CHARTS / "sensitivity_tornado.png", dpi=200)
plt.close()

print("Sensitivity analysis and charts saved.")
