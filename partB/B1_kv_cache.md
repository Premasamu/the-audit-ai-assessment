# B1 — KV-Cache Capacity Calculation

## Model specification

From `model_spec.md`:

- Layers = 28
- KV heads = 8
- Head dimension = 128
- KV precision = fp16 = 2 bytes
- Parameters = 4.2B
- Weight precision = fp16
- GPU memory = 24 GB
- GPU memory utilization = 0.92
- Non-KV runtime overhead = 1.6 GB
- Maximum model length = 4096 tokens

## KV-cache bytes per token

Each token stores both K and V:

KV bytes/token =
2 × layers × KV heads × head_dim × bytes_per_fp16

= 2 × 28 × 8 × 128 × 2

= 114,688 bytes/token

= 112 KiB/token.

The number of Q heads (24) is not used because the model uses GQA with 8 KV heads.

## KV cache for a 4096-token sequence

114,688 × 4096
= 469,762,048 bytes

This is approximately 469.76 MB or 448 MiB per full 4096-token sequence.

## Available GPU memory

24 GB × 0.92 = 22.08 GB

FP16 model weights:

4.2B × 2 bytes = 8.4 GB

Remaining memory for KV cache:

22.08 - 8.4 - 1.6
= 12.08 GB

## Maximum concurrent full-length sequences

12.08 / 0.469762048
≈ 25.72

Therefore the approximate maximum number of complete 4096-token sequences is:

**25 sequences**

The 26th sequence would exceed the approximate KV budget.

## Comparison with benchmark

The benchmark reaches batch size 24 for the 3584-token prompt / 512-token generation workload without preemptions.

At batch 32, `preempted_seqs` becomes 7 and KV utilization reaches 0.97.

This is consistent with the calculated memory pressure, although the exact scheduler behavior cannot be derived from memory arithmetic alone.