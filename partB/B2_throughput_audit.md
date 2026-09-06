# B2 — Long-Context Throughput Audit

## Workload

The long-context benchmark rows use:

- prompt length = 3584 tokens
- generation length = 512 tokens
- total context = 4096 tokens/request

## Observed throughput

| Batch | Reported tok/s | TTFT p50 (ms) | Preempted sequences | KV utilization |
|---:|---:|---:|---:|---:|
| 4 | 565.4 | 483.2 | 0 | 0.16 |
| 8 | 902.6 | 519.0 | 0 | 0.31 |
| 16 | 1311.4 | 498.3 | 0 | 0.62 |
| 24 | 1607.4 | 500.5 | 0 | 0.93 |
| 32 | 1384.0 | 636.9 | 7 | 0.97 |
| 48 | 1298.5 | 955.4 | 23 | 0.97 |

## Anomaly

Throughput increases from batch 4 through batch 24:

565.4 -> 902.6 -> 1311.4 -> 1607.4 tok/s

However, increasing the batch beyond 24 reduces throughput:

- batch 24: 1607.4 tok/s
- batch 32: 1384.0 tok/s
- batch 48: 1298.5 tok/s

Therefore throughput does not scale linearly with batch size.

## Evidence for the mechanism

KV utilization reaches 0.93 at batch 24 and 0.97 at batches 32 and 48.

At the same transition, scheduler preemption appears:

- batch 24: 0 preempted sequences
- batch 32: 7 preempted sequences
- batch 48: 23 preempted sequences

TTFT also increases:

- batch 24: 500.5 ms
- batch 32: 636.9 ms
- batch 48: 955.4 ms

The combination of near-saturated KV cache, increasing preemptions and increasing latency strongly supports KV-cache pressure/preemption as the mechanism behind the throughput degradation.

## Connection to B1

Each 4096-token sequence requires approximately 448 MiB of KV cache.

The B1 calculation gives an approximate capacity of 25 full 4096-token sequences after accounting for weights and non-KV runtime overhead.

The tested batch-24 workload has no preemptions, while batch 32 exceeds this approximate full-sequence capacity and shows 7 preempted sequences.

This is consistent with the observed memory-pressure behavior.

## Output goodput

Because `reported_tok_s` includes prompt and generated tokens, output goodput is calculated separately:

batch 24:

24 × 512 / 61.16 = 200.13 output tok/s

batch 32:

32 × 512 / 94.71 = 173.09 output tok/s

batch 48:

48 × 512 / 151.41 = 162.31 output tok/s

Batch 24 therefore provides approximately:

- 15.6% higher output goodput than batch 32
- 23.3% higher output goodput than batch 48

## Recommendation

Cap simultaneous long-context requests at batch 24 for this workload, or isolate long-context traffic into a separately controlled serving pool with an appropriate batch limit.

Batch 24 is the highest tested batch without preemption and provides the highest observed throughput.

This recommendation is specific to the tested 3584-prompt/512-generation workload. Different prompt and generation lengths should be benchmarked separately.

## Limitation

The benchmark log establishes correlation between KV-cache saturation, preemption and throughput degradation. It does not expose the serving scheduler's internal implementation, so the exact internal preemption mechanism cannot be established beyond the evidence available in the log.