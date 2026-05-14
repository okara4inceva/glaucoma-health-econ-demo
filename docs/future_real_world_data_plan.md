# Future Real-World Data Collection Plan

## Objective

To replace demo assumptions with real-world, de-identified ophthalmology data after ethics and data governance approval.

## Potential hospital data sources

| Source | Variables |
|---|---|
| CCAD-approved de-identified hospital clinical data sources | age, gender, nationality, encounters, diagnosis codes, comorbidities, referrals |
| Ophthalmology clinic notes | confirmed glaucoma, suspected glaucoma, disease stage, treatment plan |
| OCT system | RNFL thickness, cup-to-disc ratio, optic nerve findings |
| Visual field system | mean deviation, pattern standard deviation, defect severity |
| Pharmacy | eye drops, medication class, refill history, medication cost |
| Billing / finance | consultation cost, OCT cost, visual field cost, laser cost, surgery cost |
| Patient questionnaires | EQ-5D, vision-related quality of life, productivity loss, caregiver support |

## Governance requirements

- IRB / ethics approval
- Data access approval
- De-identification
- Data dictionary
- Clinician validation of disease stage and outcomes
- Secure storage and controlled access
- Reproducible analysis scripts

## Suggested minimum dataset

- patient_id_deidentified
- age
- gender
- risk factors
- IOP
- OCT result
- visual field result
- glaucoma diagnosis
- glaucoma stage
- management plan
- annual visit count
- medication use
- procedures
- direct cost
- quality-of-life score if available
