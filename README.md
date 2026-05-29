# Healthcare Social Benchmark Strategist

Claude Code plugin and skill for executive healthcare social media benchmark analysis across Facebook, Instagram, TikTok, YouTube, X, and earned media.

Use it to analyze multi-platform KPI datasets, compare healthcare institutions, score content strategy, review healthcare communication risk, and produce board-ready benchmark reports.

## Claude Code Marketplace Installation

Add the marketplace:

```sh
claude plugin marketplace add chagkrit/Social-Platform-Analysis
```

Install the plugin:

```sh
claude plugin install healthcare-social-benchmark-strategist@social-platform-analysis
```

Reload plugins if Claude Code does not pick it up immediately:

```sh
/reload-plugins
```

Invoke the skill:

```text
/healthcare-social-benchmark-strategist:healthcare-social-benchmark-strategist
```

## Local Development

Run the deterministic CSV scorer with:

```sh
python3 scripts/benchmark_score.py --input benchmark.csv --organization "Faculty of Medicine, Chiang Mai University" --md-out report.md
```

The expected CSV columns and formulas are documented in `references/kpi-definitions.md`.

## Package Contents

- `SKILL.md`: skill workflow and operating standard.
- `.claude-plugin/plugin.json`: Claude Code plugin manifest.
- `.claude-plugin/marketplace.json`: marketplace catalog for install by repository.
- `scripts/benchmark_score.py`: standard-library KPI scorer.
- `references/`: formulas, scoring rubric, healthcare risk review, and MedCMU context.
- `assets/executive_report_template.md`: board-ready report template.
