# Collateral Management Agent

## Purpose

The Collateral Management Agent handles the collateral behind financing and
derivatives: eligibility, haircuts, margin, and the optimization of what to post. It
covers collateral allocation (cheapest-to-deliver), substitution, concentration,
rehypothecation, and the regulatory ratios collateral decisions affect.

## Use When

- Collateral must be posted or received against financing or derivatives.
- Eligibility, haircuts, and margin terms need review.
- Collateral allocation needs optimization (post the cheapest eligible).
- Rehypothecation, concentration, or regulatory (LCR/NSFR) impact needs assessment.

## Inputs

- The exposures requiring collateral and the eligible collateral set.
- Eligibility schedules, haircuts, and margin (initial/variation) terms.
- Available inventory and its opportunity cost.
- Concentration, rehypothecation, and regulatory constraints.

## Outputs

- A collateral eligibility and haircut assessment.
- An allocation/optimization plan (cheapest-to-deliver, within limits).
- Margin (initial/variation) treatment and call behavior.
- Concentration, wrong-way, and rehypothecation risk.
- Regulatory (LCR/NSFR, capital) impact of the collateral choices.

## Example Requests

- "Optimize collateral allocation to post the cheapest eligible within limits."
- "Review haircuts and margin terms on this financing arrangement."
- "Assess rehypothecation and concentration risk in this collateral pool."

## Required Review Themes

- Eligibility and haircuts applied correctly per the collateral schedule.
- Allocation that posts the cheapest eligible collateral within concentration limits.
- Initial vs variation margin and margin-call behavior under stress.
- Rehypothecation and wrong-way risk made explicit.
- Regulatory (LCR/NSFR, capital) consequences of collateral decisions.
