# The Audit - Submission Notebook

This submission audits a multilingual tokenizer benchmark and a model-serving benchmark, then provides a product recommendation for multilingual casual-response generation.

The work is organized into Part A, Part B and Part C.

---

# Part A - Multilingual Tokenizer Audit

## A1 - Real multilingual evaluation corpus

Corpus: FLORES-200 devtest.

Languages evaluated:

- English (`eng_Latn`)
- Hindi (`hin_Deva`)
- Kannada (`kan_Knda`)
- Tamil (`tam_Taml`)

Each language contains 1,012 sentences, for 4,048 language-sentence instances.

The corpus is a general multilingual benchmark rather than a production conversational corpus. Preprocessing includes UTF-8 decoding, trimming, empty-line removal and NFC normalization.

See:

`partA/A1_corpus.md`

## A2 - Audit of the starter fertility benchmark

The starter implementation was audited for:

1. `split(" ")` whitespace handling.
2. Per-line averaging versus corpus-level aggregation.
3. Dependence of fertility on tokenizer choice.
4. Misinterpretation of Unicode code points as a universal cost proxy.
5. Treating `tok/char` as independent confirmation of `tok/word`.
6. Lowercasing behavior.
7. Unused random seed.

The main material flaw is the whitespace split because repeated spaces create empty fields and can inflate the denominator.

The aggregation method is also a conceptual issue when interpreting a corpus-level statistic because every line receives equal weight regardless of word count.

See:

`partA/A2_audit.md`

The original implementation is preserved as:

`partA/fertility_original.py`

## A3 - Corrected cross-language analysis

The corrected analysis evaluates:

- GPT-2 tokenizer
- XLM-R (`xlm-roberta-base`)
- whitespace-word denominator
- code-point denominator
- grapheme denominator
- UTF-8 byte denominator
- sentence-level token counts

The major finding is that GPT-2 produces substantially higher Indic fertility than XLM-R, especially for Kannada and Tamil.

GPT-2 fertility:

| Language | Tokens/word |
|---|---:|
| English | 1.278 |
| Hindi | 7.827 |
| Kannada | 22.819 |
| Tamil | 25.049 |

XLM-R fertility:

| Language | Tokens/word |
|---|---:|
| English | 1.425 |
| Hindi | 1.491 |
| Kannada | 2.576 |
| Tamil | 2.466 |

This demonstrates that the large Indic tokenization overhead is strongly tokenizer-dependent rather than simply a property of Unicode/script.

See:

`partA/A3_corrected_analysis.md`

## A4 - Recommendation

The corrected evidence does not justify a fixed universal multiplier such as "all Indic traffic costs 6x".

Production cost/routing should use actual model/tokenizer token counts, measured separately for input and output, and should be monitored by language.

See:

`partA/A4_recommendation_memo.md`

---

# Part B - Serving Audit

## B1 - KV-cache calculation

Using GQA with 8 KV heads:

`2 x 28 layers x 8 KV heads x 128 head_dim x 2 bytes`

= **114,688 bytes/token = 112 KiB/token**

A 4,096-token sequence therefore requires approximately:

**469.76 MB decimal â‰ˆ 448 MiB**

Using the supplied memory budget:

- GPU memory = 24 GB
- GPU utilization budget = 92%
- FP16 weights = 8.4 GB
- non-KV runtime overhead = 1.6 GB

Remaining KV budget â‰ˆ 12.08 GB.

This supports approximately **25 full 4096-token sequences**.

See:

`partB/B1_kv_cache.md`

## B2 - Long-context throughput anomaly

Long-context throughput increases through batch 24:

- batch 4: 565.4 tok/s
- batch 8: 902.6 tok/s
- batch 16: 1311.4 tok/s
- batch 24: 1607.4 tok/s

It then decreases:

- batch 32: 1384.0 tok/s
- batch 48: 1298.5 tok/s

At the same point, KV utilization reaches approximately 0.93 at batch 24 and 0.97 at batches 32/48, while sequence preemption increases from 0 to 7 and then 23.

The evidence strongly supports KV-cache pressure/preemption as the mechanism.

See:

`partB/B2_throughput_audit.md`

## B3 - Honest goodput

For batch 24:

`24 x 512 output tokens / 61.16 seconds`

= **200.13 output tokens/s**

An independent calculation from the reported total-token throughput gives:

`1607.4 x (512 / 4096)`

= **200.93 output tokens/s**

Therefore the honest output goodput is approximately **200 output tokens/s**, not 1607 tok/s.

The reported throughput includes prompt/prefill tokens and should not be presented as generated-output goodput.

See:

`partB/B3_goodput_audit.md`

## B4 - Production monitoring

The recommended serving metric is a KV-cache sequence preemption/eviction counter.

Expected behavior:

- batch 24: approximately zero preemptions
- batch 32: nonzero preemptions
- batch 48: substantially more preemptions

This should confirm whether the observed throughput collapse continues to coincide with KV-cache pressure.

See:

`partB/B4_monitoring.md`

---

# Part C - Product Recommendation

Recommendation:

**Use option (b): a local inference-time rewriter â‰¤1B parameters.**

The rewriter preserves the main model and provides a reversible way to improve casual conversational style across six Indian languages.

The memo explicitly labels planning assumptions and estimates data volume, GPU usage, serving latency and reviewer throughput.

The primary risk is limited native-speaker review coverage: the available reviewer covers Hindi and Kannada but not Tamil, Telugu, Bengali or Marathi.

See:

`partC/memo.md`

---

# Evidence and reproducibility

The analysis was performed using the supplied starter benchmark and supplied serving benchmark data, together with the FLORES-200 devtest corpus.

Experiment outputs and supporting files are stored under:

- `partA/experiments/`
- `partA/results/`
- `partA/corpus/`

The submission distinguishes measured results from assumptions and does not treat planning estimates as experimental measurements.

AI assistance and the work performed with AI are documented separately in:

`AI_USAGE.md`
