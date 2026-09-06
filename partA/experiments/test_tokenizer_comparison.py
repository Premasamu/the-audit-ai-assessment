from pathlib import Path
import unicodedata
import tiktoken
from transformers import AutoTokenizer

CORPUS = Path("ai-assessment/partA/corpus/flores")

gpt2 = tiktoken.get_encoding("gpt2")
xlmr = AutoTokenizer.from_pretrained("xlm-roberta-base")


def read_lines(path):
    lines = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()

            if not line:
                continue

            line = unicodedata.normalize("NFC", line)
            lines.append(line.lower())

    return lines


for lang in ["eng_Latn", "hin_Deva", "kan_Knda", "tam_Taml"]:

    lines = read_lines(CORPUS / f"{lang}.devtest")

    total_words = 0
    gpt2_tokens = 0
    xlmr_tokens = 0

    for line in lines:
        words = line.split()

        total_words += len(words)

        gpt2_tokens += len(gpt2.encode(line))

        xlmr_tokens += len(
            xlmr.encode(line, add_special_tokens=False)
        )

    gpt2_fertility = gpt2_tokens / total_words
    xlmr_fertility = xlmr_tokens / total_words

    ratio = gpt2_fertility / xlmr_fertility

    print(f"\n{lang}")
    print(f"words                   : {total_words}")
    print(f"GPT-2 tokens            : {gpt2_tokens}")
    print(f"XLM-R tokens            : {xlmr_tokens}")
    print(f"GPT-2 fertility         : {gpt2_fertility:.6f}")
    print(f"XLM-R fertility         : {xlmr_fertility:.6f}")
    print(f"GPT-2 / XLM-R ratio     : {ratio:.4f}x")