# A2 — Audit of fertility.py and REPORT_v0



## Finding 1 — Whitespace splitting is a real denominator bug



The original code uses:



    words = line.split(" ")



Using `split(" ")` can create empty fields when repeated spaces occur.



I compared the original behavior with `split()` on the FLORES-200 devtest corpus.



| Language | Original fertility | Corrected fertility | Relative change |

|---|---:|---:|---:|

| English | 1.278206 | 1.278206 | 0.0000% |

| Hindi | 7.824711 | 7.826541 | +0.0234% |

| Kannada | 22.297020 | 22.819130 | +2.3416% |

| Tamil | 24.900385 | 25.048823 | +0.5961% |



The largest observed distortion is +2.3416% for Kannada.



Therefore this is a verified implementation bug in the denominator.



---



## Finding 2 — Per-line averaging is a conceptual metric issue



The original code calculates fertility separately for every sentence and then averages those values:



    sum(per_line_fertility) / n



This gives every sentence equal weight.



I compared this with corpus-level fertility:



    total_tokens / total_words



| Language | Per-line average | Corpus aggregate | Relative difference |

|---|---:|---:|---:|

| English | 1.287365 | 1.278206 | -0.7114% |

| Hindi | 7.866883 | 7.826541 | -0.5128% |

| Kannada | 23.019266 | 22.819130 | -0.8694% |

| Tamil | 25.252269 | 25.048823 | -0.8057% |



The largest difference is 0.8694% for Kannada.



This is not necessarily a programming error; it is a metric-definition choice. However, the report presents the resulting number as if it were an overall corpus fertility measure without discussing the weighting choice.



---



## Finding 3 — Tokenizer choice dominates Indic fertility



I evaluated the same FLORES corpus using GPT-2 and XLM-R.



| Language | GPT-2 fertility | XLM-R fertility |

|---|---:|---:|

| English | 1.278206 | 1.425460 |

| Hindi | 7.826541 | 1.490738 |

| Kannada | 22.819130 | 2.576460 |

| Tamil | 25.048823 | 2.465812 |



The largest difference occurs for Tamil:



25.048823 / 2.465812 = approximately 10.16×.



Kannada differs by approximately 8.86× and Hindi by approximately 5.25×.



Therefore the REPORT_v0 statement that Hindi's high fertility is simply a property of Unicode/script and that any tokenizer will struggle is not supported.



The experiment changes the tokenizer while keeping the corpus and denominator fixed. The resulting large changes demonstrate strong tokenizer dependence.



Important limitation: XLM-R is not the FLM-4B tokenizer, so these numbers demonstrate tokenizer sensitivity rather than direct production cost savings.



---



## Finding 4 — tok/char does not independently confirm tok/word



The original report states that the tok/char metric confirms the tok/word result.



The ratio experiment produced:



- Fertility ratio: 5.928×

- tok/char ratio: 6.987×



The ratios differ substantially.



Furthermore, both metrics contain the same token count in the numerator. Therefore tok/char is not independent evidence confirming tok/word.



The two metrics answer different normalization questions and should not be presented as independent confirmation.



---



## Finding 5 — `len()` is not itself a bug, but "character" is ambiguous



Python's `len()` counts Unicode code points.



On the test samples:



- English: 38 code points, 38 UTF-8 bytes

- Hindi: 30 code points, 78 UTF-8 bytes



On FLORES, code-point and grapheme-cluster counts also differ substantially for Indic languages.



Therefore the implementation is technically counting code points, not necessarily user-perceived characters.



This makes tok/code-point a legitimate diagnostic metric, but it should not automatically be interpreted as tokens per human-perceived character.



---



## Finding 6 — Lowercasing is suspicious-looking but not a major Indic problem



The original benchmark applies:



    line = line.lower()



I tested token counts with and without lowercasing.



GPT-2 relative changes:



- English: -3.3936%

- Hindi: -0.0040%

- Kannada: -0.0060%

- Tamil: -0.0055%



XLM-R relative changes:



- English: -1.7874%

- Hindi: -0.0157%

- Kannada: -0.0530%

- Tamil: -0.0242%



Therefore lowercasing affects English modestly but has negligible effect on the three Indic languages tested.



I would not classify this as a major bug.



---



## Finding 7 — `random.seed(1337)` is harmless



The script initializes:



    random.seed(1337)



However, no random operation is subsequently used.



Therefore the seed has no measurable effect on the benchmark output.



This is an example of code that looks suspicious but is actually harmless.

