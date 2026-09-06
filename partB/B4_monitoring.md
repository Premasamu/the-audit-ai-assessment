# B4 — Production Metric to Confirm the Throughput Mechanism

## Recommended metric

Monitor a serving-stack counter for:

**KV-cache sequence preemptions/evictions**

The exact metric name depends on the serving stack and should not be assumed from the provided benchmark.

## Expected behavior

The benchmark already provides a corresponding `preempted_seqs` field:

| Batch | KV utilization | Preempted sequences |
|---:|---:|---:|
| 24 | 0.93 | 0 |
| 32 | 0.97 | 7 |
| 48 | 0.97 | 23 |

If KV-cache pressure is causing the throughput degradation, the production counter should remain near zero at safe operating points and increase when the system is pushed beyond the KV-cache capacity boundary.

The expected pattern is therefore:

- batch 24: approximately 0 preemptions
- batch 32: nonzero preemptions
- batch 48: substantially more preemptions

This metric would directly test the proposed B2 mechanism rather than relying only on throughput or latency.