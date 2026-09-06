\# Part A — Experimental Results



\## A1 — Multilingual Corpus



Dataset: FLORES-200 devtest



Languages:

\- English (eng\_Latn)

\- Hindi (hin\_Deva)

\- Kannada (kan\_Knda)

\- Tamil (tam\_Taml)



Sentences per language: 1012



Total language-sentence instances: 4048



The four language files contain the same number of sentences and are aligned by sentence order.



\---



\## A2 — Audit Findings



\### Finding 1 — `split(" ")` denominator bug



Experiment:

`test\_whitespace\_fertility.py`



Result:

\- English: 0.0000% change

\- Hindi: +0.0234%

\- Kannada: +2.3416%

\- Tamil: +0.5961%



Conclusion:

`split(" ")` can count empty fields created by repeated whitespace. The maximum observed distortion was +2.3416% for Kannada.



\---



\### Finding 2 — Per-line averaging changes the corpus metric



Experiment:

`test\_aggregation\_flores.py`



Result:

\- English: -0.7114%

\- Hindi: -0.5128%

\- Kannada: -0.8694%

\- Tamil: -0.8057%



Conclusion:

The original script averages sentence-level fertility values equally. A corpus-level calculation uses total tokens / total words. These are different estimands.



\---



\### Finding 3 — Tokenizer choice has a major effect



Experiment:

`test\_tokenizer\_comparison.py`



GPT-2 vs XLM-R:



| Language | GPT-2 | XLM-R |

|---|---:|---:|

| English | 1.278 | 1.425 |

| Hindi | 7.827 | 1.491 |

| Kannada | 22.819 | 2.576 |

| Tamil | 25.049 | 2.466 |



Conclusion:

Tokenizer choice strongly affects Indic fertility. Therefore tokenizer behavior, not Unicode/script alone, must be considered.



\---



\### Finding 4 — `tok/char` does not independently confirm `tok/word`



Experiment:

`test\_ratios.py`



Results:

\- Fertility ratio: 5.928x

\- Token/character ratio: 6.987x



Conclusion:

The two ratios differ and share the same token count, so the second metric is not independent confirmation of the first.



\---



\### Finding 5 — Lowercasing is not a major Indic distortion



Experiment:

`test\_lowercase\_effect.py`



GPT-2:

\- English: -3.3936%

\- Hindi: -0.0040%

\- Kannada: -0.0060%

\- Tamil: -0.0055%



XLM-R:

\- English: -1.7874%

\- Hindi: -0.0157%

\- Kannada: -0.0530%

\- Tamil: -0.0242%



Conclusion:

Lowercasing changes English tokenization modestly but has negligible effect on these Indic languages.



\---



\### Finding 6 — `random.seed(1337)` is harmless



The script sets a random seed but does not use any random operation.



Conclusion:

This is suspicious-looking but does not affect the benchmark result.



\---



\## A3 — Corrected Benchmark



Production cost/routing should ultimately use actual model tokens per request, preferably separating input and output tokens.



Whitespace words, Unicode code points, grapheme clusters and UTF-8 bytes are useful diagnostic denominators, but they are not direct substitutes for production model-token counts.



XLM-R results demonstrate tokenizer sensitivity, but XLM-R token counts should not be interpreted as FLM-4B serving costs because the production model's tokenizer is not established by this experiment.

