# A4 — Recommendation Memo



## Executive recommendation



The original fertility headline should not be used for production cost planning.



On the FLORES-200 devtest corpus, GPT-2 fertility is 1.278 tok/word for English, 7.827 for Hindi, 22.819 for Kannada, and 25.049 for Tamil. However, changing only the tokenizer to XLM-R reduces Indic fertility substantially: 1.491 for Hindi, 2.576 for Kannada, and 2.466 for Tamil.



This demonstrates that the large Indic fertility gap is strongly tokenizer-dependent rather than solely a property of the writing system.



## Routing recommendation



Do not route requests using Unicode character count or a fixed language-based cost multiplier.



Instead, production routing and capacity planning should use measurements from the actual production model/tokenizer:



- input tokens per request

- output tokens per request

- total tokens per request

- latency

- request cost



If the production model has a tokenizer with poor Indic efficiency, measure that tokenizer directly and use its observed token distribution for capacity planning.



## Corrected headline numbers



GPT-2 corpus-level fertility:



| Language | Tokens/word |

|---|---:|

| English | 1.278 |

| Hindi | 7.827 |

| Kannada | 22.819 |

| Tamil | 25.049 |



XLM-R corpus-level fertility:



| Language | Tokens/word |

|---|---:|

| English | 1.425 |

| Hindi | 1.491 |

| Kannada | 2.576 |

| Tamil | 2.466 |



The GPT-2/XLM-R fertility ratio is approximately 5.25× for Hindi, 8.86× for Kannada, and 10.16× for Tamil.



These are benchmark tokenization ratios, not direct serving-cost multipliers.



## Biggest caveat



FLORES-200 is a general multilingual benchmark rather than a production conversational workload. In addition, XLM-R is not the FLM-4B tokenizer specified in the serving benchmark.



Therefore the results establish tokenizer sensitivity but do not establish the exact production cost of FLM-4B.



A final production decision should be validated using the actual model tokenizer and representative production traffic.



## Production metric to monitor



The single most useful production metric is:



\*\*input tokens and output tokens per request, measured using the actual production tokenizer.\*\*



This directly connects language mix and request workload to inference capacity and cost.

