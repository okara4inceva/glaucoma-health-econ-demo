"""
Run base-case glaucoma health economics model.
"""

from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

INPUTS = {
    "target_population_screened": 1000,
    "screening_cost_per_person_aed": 250,
    "glaucoma_prevalence_in_high_risk_group": 0.05,
    "usual_care_detection_rate": 0.40,
    "early_detection_rate": 0.80,
    "progression_to_advanced_usual_care": 0.25,
    "progression_to_advanced_early_detection": 0.10,
    "annual_cost_early_glaucoma_aed": 1500,
    "annual_cost_advanced_glaucoma_aed": 6000,
    "annual_productivity_loss_early_aed": 1000,
    "annual_productivity_loss_advanced_aed": 8000,
}

def run_model(params):
    pop = params["target_population_screened"]
    prevalence = params["glaucoma_prevalence_in_high_risk_group"]
    expected_cases = pop * prevalence
    detected_usual = expected_cases * params["usual_care_detection_rate"]
    detected_early = expected_cases * params["early_detection_rate"]
    additional_early_detected = detected_early - detected_usual

    screening_cost = pop * params["screening_cost_per_person_aed"]

    advanced_cases_usual = expected_cases * params["progression_to_advanced_usual_care"]
    advanced_cases_early = expected_cases * params["progression_to_advanced_early_detection"]
    advanced_cases_avoided = advanced_cases_usual - advanced_cases_early

    direct_cost_usual = (
        (expected_cases - advanced_cases_usual) * params["annual_cost_early_glaucoma_aed"]
        + advanced_cases_usual * params["annual_cost_advanced_glaucoma_aed"]
    )
    direct_cost_early = (
        screening_cost
        + (expected_cases - advanced_cases_early) * params["annual_cost_early_glaucoma_aed"]
        + advanced_cases_early * params["annual_cost_advanced_glaucoma_aed"]
    )

    productivity_usual = (
        (expected_cases - advanced_cases_usual) * params["annual_productivity_loss_early_aed"]
        + advanced_cases_usual * params["annual_productivity_loss_advanced_aed"]
    )
    productivity_early = (
        (expected_cases - advanced_cases_early) * params["annual_productivity_loss_early_aed"]
        + advanced_cases_early * params["annual_productivity_loss_advanced_aed"]
    )

    total_societal_usual = direct_cost_usual + productivity_usual
    total_societal_early = direct_cost_early + productivity_early

    return {
        "target_population_screened": pop,
        "expected_glaucoma_cases": expected_cases,
        "detected_cases_usual_care": detected_usual,
        "detected_cases_early_detection": detected_early,
        "additional_early_cases_detected": additional_early_detected,
        "screening_program_cost_aed": screening_cost,
        "advanced_cases_usual_care": advanced_cases_usual,
        "advanced_cases_early_detection": advanced_cases_early,
        "advanced_cases_avoided": advanced_cases_avoided,
        "direct_cost_usual_care_aed": direct_cost_usual,
        "direct_cost_early_detection_aed": direct_cost_early,
        "incremental_direct_budget_impact_aed": direct_cost_early - direct_cost_usual,
        "productivity_loss_usual_care_aed": productivity_usual,
        "productivity_loss_early_detection_aed": productivity_early,
        "productivity_loss_avoided_aed": productivity_usual - productivity_early,
        "total_societal_cost_usual_care_aed": total_societal_usual,
        "total_societal_cost_early_detection_aed": total_societal_early,
        "net_societal_budget_impact_aed": total_societal_early - total_societal_usual,
        "cost_per_additional_early_case_detected_aed": screening_cost / additional_early_detected,
        "cost_per_advanced_case_avoided_aed": (direct_cost_early - direct_cost_usual) / advanced_cases_avoided,
    }

if __name__ == "__main__":
    results = run_model(INPUTS)
    pd.DataFrame([results]).round(2).to_csv(OUT / "base_case_results.csv", index=False)

    with open(OUT / "model_summary.txt", "w") as f:
        f.write("Glaucoma Health Economics Demo - Base Case Results\n")
        f.write("=" * 58 + "\n\n")
        for key, value in results.items():
            f.write(f"{key}: {round(value, 2)}\n")

    print(pd.DataFrame([results]).round(2).T)
