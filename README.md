# The Audit

This repository contains my submission for the **AI Team Intern – The Audit** take-home assignment.

## Project Overview

The assignment audits multilingual tokenizer evaluation and model-serving benchmark results, identifies implementation and metric issues, and provides evidence-based recommendations.

### Part A — Multilingual Tokenizer Audit
- Evaluated a real multilingual corpus using English, Hindi, Kannada, and Tamil.
- Audited the provided tokenizer fertility benchmark.
- Identified implementation and conceptual metric issues.
- Compared GPT-2 and XLM-R tokenization behavior.
- Provided corrected cross-language analysis and production recommendations.

### Part B — Model Serving Audit
- Calculated KV-cache memory requirements.
- Investigated long-context throughput behavior.
- Corrected the reported output goodput calculation.
- Proposed a serving-stack monitoring metric to validate the identified mechanism.

### Part C — Product Recommendation
- Evaluated three approaches for generating casual conversational responses in six Indian languages.
- Recommended a local inference-time rewriter (≤1B parameters).
- Included assumptions, cost/effort estimates, success criteria, kill criterion, and a day-1 experiment.

## Repository Structure

```text
ai-assessment/
├── NOTEBOOK.md
├── AI_USAGE.md
├── partA/
│   ├── A1_corpus.md
│   ├── A2_audit.md
│   ├── A3_corrected_analysis.md
│   ├── A4_recommendation_memo.md
│   ├── fertility_original.py
│   ├── corpus/
│   ├── experiments/
│   └── results/
├── partB/
│   ├── model_spec.md
│   ├── bench_log.csv
│   ├── B1_kv_cache.md
│   ├── B2_throughput_audit.md
│   ├── B3_goodput_audit.md
│   └── B4_monitoring.md
└── partC/
    └── memo.md
