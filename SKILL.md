---
name: healthcare-social-benchmark-strategist
description: Executive healthcare social media benchmark workflow for hospitals, universities, academic medicine, public-health organizations, and medical faculties. Use when analyzing multi-platform KPI datasets, comparing Facebook/Instagram/TikTok/YouTube/X performance, scoring healthcare content strategy, evaluating earned media and institutional authority, producing board-ready reports, or building 90-day social media improvement roadmaps.
---

# Healthcare Social Benchmark Strategist

## Operating Standard

Analyze social media performance as an evidence-based executive workflow. Do not invent missing metrics, competitor data, reach, paid/organic splits, or platform definitions.

Separate:

- Fact: directly present in the dataset or verified source.
- Interpretation: analytic reading of facts.
- Assumption: required but not directly observed.
- Recommendation: action based on facts and assumptions.

Prioritize engagement quality, audience trust, public-health value, sustainability, and operational feasibility over vanity metrics or short-term spikes.

## Workflow

1. **Frame the benchmark**
   - Identify organization type: hospital, faculty of medicine, university, public-health agency, society, clinic network, or campaign.
   - Identify platforms, period, comparator set, campaign context, and target audience.
   - Read `references/kpi-definitions.md` before calculating metrics.
   - Read `references/healthcare-content-risk.md` for healthcare-specific safety, privacy, accessibility, and misinformation checks.

2. **Audit data quality**
   - Confirm whether metrics are native analytics, manual reports, scraped data, or third-party exports.
   - Check period coverage, missing platforms, inconsistent denominators, paid/organic mixing, duplicated posts, and campaign/event spikes.
   - State when reach, impressions, follower counts, or earned-media data are unavailable.

3. **Run deterministic scoring when CSV data is available**
   - Use `scripts/benchmark_score.py` for KPI summaries, platform scoring, weighted score, confidence grade, and Markdown/JSON executive output.
   - Use `references/scoring-rubric.md` before accepting weighted scores.
   - Use sensitivity analysis when score differences are small or weights are disputed.

4. **Interpret healthcare strategy**
   - Read `references/healthcare-content-risk.md` before recommendations.
   - Separate owned-media strength from earned-media influence.
   - Separate large audience size from efficiency.
   - Separate institutional credibility from actual content performance.
   - Assess whether content improves public understanding, trust, service navigation, prevention behavior, and research translation.

5. **Use MedCMU special mode when relevant**
   - Read `references/medcmu-special-mode.md` for Faculty of Medicine, Chiang Mai University, Maharaj Nakorn Chiang Mai Hospital, or Northern Thailand public-health context.
   - Prioritize PM2.5/respiratory health, seasonal outbreaks, cancer prevention, elderly health, emergency communication, medical education, research translation, and community trust.

6. **Create executive report**
   - Use `assets/executive_report_template.md` for board-ready output.
   - Include executive summary, data limitations, KPI dashboard, benchmark matrix, weighted scoring, risk matrix, SWOT, earned-media analysis, recommendations, 90-day plan, and roadmap.

## Required Outputs

For substantial analyses, produce:

- Data limitation summary.
- KPI dictionary and formulas used.
- Cross-platform benchmark matrix.
- Weighted scoring table with confidence.
- Healthcare content-risk review.
- Earned vs owned interpretation.
- Strategic recommendations.
- 90-day action plan.
- Executive conclusion.

## Default Scoring Weights

Use these weights unless the user specifies otherwise:

- Engagement Efficiency: 25%
- Engagement Quality: 20%
- Follower Growth Strength: 15%
- Growth Sustainability: 13%
- Reach Power: 10%
- Content Consistency: 10%
- Strategic Value: 5%
- Stability / Volatility Control: 2%

Score scale:

- 5: excellent
- 4: strong
- 3: moderate
- 2: weak
- 1: critical

Always report score confidence: high, medium, or low.

## Resource Guide

- `references/kpi-definitions.md`: KPI formulas, required columns, and denominator rules.
- `references/scoring-rubric.md`: Weighted scoring model, confidence rules, and sensitivity checks.
- `references/healthcare-content-risk.md`: Healthcare-specific risk, privacy, misinformation, accessibility, and trust review.
- `references/medcmu-special-mode.md`: Faculty of Medicine Chiang Mai University and Northern Thailand public-health strategy.
- `assets/executive_report_template.md`: Board-ready output template.
- `scripts/benchmark_score.py`: Deterministic CSV scoring and executive report generator.
