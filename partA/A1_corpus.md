# A1 — Multilingual Evaluation Corpus



## Dataset



I used the FLORES-200 devtest corpus for the multilingual evaluation.



Languages selected:



| Language | FLORES code | Sentences |

|---|---|---:|

| English | eng_Latn | 1012 |

| Hindi | hin_Deva | 1012 |

| Kannada | kan_Knda | 1012 |

| Tamil | tam_Taml | 1012 |



Total: 4 languages × 1012 sentences = 4048 language-sentence instances.



## Alignment



The four language files contain the same number of sentences. FLORES provides the sentences in aligned order across languages, allowing corresponding sentences to be compared across languages.



## Domain



The FLORES devtest corpus contains multilingual sentences drawn from varied domains. The metadata includes topics such as health, business, music, sports and research.



Therefore, this is not a single-domain legal or conversational corpus.



## Preprocessing



The benchmark:



1\. Reads UTF-8 text.

2\. Removes leading/trailing whitespace.

3\. Skips empty lines.

4\. Applies Unicode NFC normalization.



The original benchmark also converts text to lowercase before tokenization. I separately tested the effect of this operation.



## Caveats



1\. FLORES is a general multilingual benchmark, not a domain-specific production workload.

2\. Whitespace-delimited words are only one possible denominator for multilingual text.

3\. Unicode code points are not equivalent to user-perceived characters.

4\. Tokenizer behavior varies substantially across languages and tokenizer families.

5\. XLM-R was used as a multilingual comparison tokenizer, but its token counts should not be interpreted as the production FLM-4B model's token counts.

6\. For production cost/routing, actual model tokens per request are more directly relevant than words, characters or bytes.



## Corpus Verification



All four selected language files contain exactly 1012 sentences.



Verified line counts:



- English: 1012

- Hindi: 1012

- Kannada: 1012

- Tamil: 1012



Thus the corpus contains 4048 aligned language-sentence instances.

