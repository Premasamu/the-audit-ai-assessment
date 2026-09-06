# AI Usage Disclosure

## How AI was used

AI assistance was used throughout the assignment as a reasoning, documentation and debugging aid.

AI was used to:

- explain the assignment requirements;
- inspect and reason about the supplied benchmark code;
- identify possible implementation and conceptual issues;
- suggest experiments that could distinguish real bugs from harmless code;
- help calculate and cross-check reported metrics;
- help interpret tokenizer and serving benchmark results;
- organize findings into Part A, Part B and Part C;
- draft and edit documentation and recommendation memos;
- check whether the submission addressed the requested deliverables.

## What was independently executed

The benchmark commands and experiments were executed in the local assignment environment.

Measured values in the submission were taken from those executions rather than invented by AI.

Examples include:

- tokenizer fertility measurements on the FLORES-200 corpus;
- `split(" ")` versus `split()` comparisons;
- per-line versus aggregate fertility calculations;
- Unicode/code-point/UTF-8 measurements;
- GPT-2 versus XLM-R comparisons;
- sentence-level token statistics;
- lowercasing comparisons;
- KV-cache arithmetic using the supplied model specification;
- throughput and goodput calculations using the supplied `bench_log.csv`.

## Treatment of assumptions

Where a value was not experimentally measured, it is explicitly labeled as an assumption, estimate or planning value.

This particularly applies to the Part C estimates for:

- synthetic training-data volume;
- training throughput;
- reserved GPU-hours;
- rewriter serving latency;
- reviewer throughput.

These estimates are not presented as measured production performance.

## AI limitations

AI-generated interpretations were treated as hypotheses until checked against the supplied code, benchmark data or independently calculated results.

The final submission therefore distinguishes:

1. measured benchmark results;
2. calculations derived from supplied measurements/specifications;
3. assumptions and planning estimates.

No claim is intended to imply an experiment was performed when it was not.