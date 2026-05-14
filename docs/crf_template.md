# CRF Template: Early Glaucoma Detection Demo

## Patient information

| Variable | Description |
|---|---|
| study_id | De-identified study ID |
| age | Age at index visit |
| gender | Male / Female / Other |
| nationality_group | Optional grouped variable |
| visit_date | Index ophthalmology visit date |

## Risk factors

| Variable | Description |
|---|---|
| family_history_glaucoma | Yes / No |
| diabetes | Yes / No |
| hypertension | Yes / No |
| steroid_use | Yes / No |
| previous_eye_disease | Yes / No |

## Ophthalmology assessment

| Variable | Description |
|---|---|
| iop_mmhg | Intraocular pressure |
| oct_result | Normal / Suspicious / Abnormal |
| visual_field_result | Normal / Mild / Moderate / Severe |
| optic_nerve_finding | Normal / Suspicious / Abnormal |
| diagnosis | No glaucoma / Suspected / Confirmed |
| disease_stage | Early / Moderate / Advanced |

## Resource use

| Variable | Description |
|---|---|
| consultation_count | Number of ophthalmology visits |
| oct_count | Number of OCT tests |
| visual_field_count | Number of visual field tests |
| medications | Glaucoma medication classes |
| laser_procedure | Yes / No |
| surgery | Yes / No |

## Economic variables

| Variable | Description |
|---|---|
| screening_cost | Cost of early detection package |
| annual_direct_cost | Annual healthcare cost |
| productivity_loss | Estimated productivity loss |
| caregiver_cost | Optional caregiver burden |
