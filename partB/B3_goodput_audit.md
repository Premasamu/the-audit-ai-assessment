# B3 — Throughput Counter and Goodput Audit

## Problem with the original report

The original report states:

> "Longer prompts clearly give better GPU utilization."

It also estimates that batch 48 should provide approximately 3200 tok/s.

These conclusions result from interpreting `reported_tok_s` without accounting for the prompt tokens included in that counter.

## Batch-24 long-context row

The relevant benchmark row is:

- batch size = 24
- prompt length = 3584
- generation length = 512
- wall-clock time = 61.16 seconds
- reported throughput = 1607.4 tok/s

Each request therefore contains:

3584 + 512 = 4096 total tokens.

## Method 1 — Direct output goodput

Generated tokens are:

24 × 512 = 12,288 output tokens.

Therefore:

12,288 / 61.16 = 200.13 output tok/s.

## Method 2 — Recover output goodput from reported throughput

The reported counter includes 4096 total tokens per request.

The fraction corresponding to generated tokens is:

512 / 4096 = 0.125.

Therefore:

1607.4 × (512 / 4096)
= 200.925 output tok/s.

The small difference between 200.13 and 200.93 is explained by rounding of the reported throughput value.

Both methods therefore give approximately:

**200 output tokens/s.**

## Batch-48 claim

The actual batch-48 long-context result is:

- reported throughput = 1298.5 tok/s
- wall-clock time = 151.41 seconds
- output goodput = 48 × 512 / 151.41
- output goodput ≈ 162.31 output tok/s

Therefore the claim that batch 48 would provide approximately 3200 tok/s is not supported by the benchmark.

## What the report should have said

The batch-24 workload achieves approximately 1607 total-token/s according to the harness, but only approximately 200 generated output tokens/s.

The high total-token throughput is partly due to counting the 3584-token prompt in the throughput counter. It should not be interpreted as 1607 generated output tokens/s.

Furthermore, increasing batch size beyond 24 decreases reported throughput and output goodput:

- batch 24: 1607.4 reported tok/s; 200.13 output tok/s
- batch 32: 1384.0 reported tok/s; 173.09 output tok/s
- batch 48: 1298.5 reported tok/s; 162.31 output tok/s

Thus the original batch-48 estimate of approximately 3200 tok/s is incorrect.