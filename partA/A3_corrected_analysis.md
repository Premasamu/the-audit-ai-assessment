# A3 — Corrected Cross-Language Analysis



## Experimental setup



Corpus:

FLORES-200 devtest



Languages:

- English (eng_Latn)

- Hindi (hin_Deva)

- Kannada (kan_Knda)

- Tamil (tam_Taml)



Sentences:

1012 per language



Tokenizers:

1\. GPT-2

2\. XLM-R (xlm-roberta-base)



The same corpus and whitespace-word denominator were used for the tokenizer comparison.



---



## 1. Tokenizer comparison



| Language | GPT-2 fertility | XLM-R fertility |

|---|---:|---:|

| English | 1.278206 | 1.425460 |

| Hindi | 7.826541 | 1.490738 |

| Kannada | 22.819130 | 2.576460 |

| Tamil | 25.048823 | 2.465812 |



### Observation



Tokenizer choice has a very large effect on Indic languages.



Relative GPT-2/XLM-R fertility ratios:



- English: 0.8967×

- Hindi: 5.2501×

- Kannada: 8.8568×

- Tamil: 10.1584×



For Tamil, GPT-2 produces approximately 10.16 times the fertility of XLM-R on the same corpus and denominator.



Therefore language-level tokenization cannot be treated as a property of the script alone. The tokenizer/model pairing is a major factor.



---



## 2. Multiple denominator analysis



### GPT-2



| Language | Tok/word | Tok/code point | Tok/grapheme | Tok/byte |

|---|---:|---:|---:|---:|

| English | 1.278206 | 0.212129 | 0.212130 | 0.211920 |

| Hindi | 7.826541 | 1.529928 | 2.334842 | 0.594762 |

| Kannada | 22.819130 | 2.661711 | 4.065331 | 0.978811 |

| Tamil | 25.048823 | 2.726213 | 4.213569 | 0.996582 |



### XLM-R



| Language | Tok/word | Tok/code point | Tok/grapheme | Tok/byte |

|---|---:|---:|---:|---:|

| English | 1.425460 | 0.236567 | 0.236569 | 0.236334 |

| Hindi | 1.490738 | 0.291409 | 0.444722 | 0.113286 |

| Kannada | 2.576460 | 0.300528 | 0.459008 | 0.110516 |

| Tamil | 2.465812 | 0.268369 | 0.414785 | 0.098104 |



---



## 3. Sentence-level token counts



GPT-2:



| Language | Mean tokens/sentence | Median | P95 |

|---|---:|---:|---:|

| English | 27.662 | 27 | 44 |

| Hindi | 198.316 | 191 | 319 |

| Kannada | 363.032 | 345 | 589 |

| Tamil | 415.211 | 398 | 663 |



XLM-R:



| Language | Mean tokens/sentence | Median | P95 |

|---|---:|---:|---:|

| English | 30.849 | 30 | 48 |

| Hindi | 37.774 | 36 | 61 |

| Kannada | 40.989 | 39 | 68 |

| Tamil | 40.874 | 39 | 68 |



The sentence-level comparison reinforces the tokenizer effect. GPT-2 produces substantially more tokens for the Indic languages, while XLM-R produces much more similar token counts across the four languages.



---



## 4. Which denominator should drive production routing and cost?



The production metric should be:



\*\*actual model tokens per request\*\*, with input and output tokens measured separately.



This is preferable to:



- whitespace words

- Unicode code points

- grapheme clusters

- UTF-8 bytes



because the model's inference system actually processes model tokens.



The other denominators remain useful diagnostic metrics for understanding why tokenization behaves differently across languages.



---



## 5. Routing recommendation



Routing should be based on measured token behavior of the actual production model/tokenizer.



The experiments demonstrate that a tokenizer can change Indic token counts by large factors. Therefore, a routing policy based only on language or Unicode character count would be unreliable.



A production system should collect:



- language

- tokenizer/model

- input token count

- output token count

- total tokens

- latency

- request cost



and use these measurements for capacity planning.



---



## 6. Important limitation



XLM-R is used here as a multilingual comparison tokenizer. It is not the tokenizer of the FLM-4B production model specified in Part B.



Therefore the XLM-R token counts demonstrate tokenizer sensitivity but must not be presented as direct FLM-4B cost savings.



The final production routing decision should be validated using the actual production model tokenizer.

