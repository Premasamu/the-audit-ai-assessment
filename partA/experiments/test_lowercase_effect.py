from pathlib import Path
import unicodedata
import tiktoken
from transformers import AutoTokenizer

CORPUS = Path("ai-assessment/partA/corpus/flores")

gpt2 = tiktoken.get_encoding("gpt2")
xlmr = AutoTokenizer.from_pretrained("xlm-roberta-base")

languages = ["eng_Latn", "hin_Deva", "kan_Knda", "tam_Taml"]


def read_lines(path):
    lines = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()

            if not line:
                continue

            line = unicodedata.normalize("NFC", line)
            lines.append(line)

    return lines


tokenizers = {
    "gpt2": lambda text: gpt2.encode(text),
    "xlmr": lambda text: xlmr.encode(
        text,
        add_special_tokens=False
    ),
}


for tokenizer_name, encode in tokenizers.items():

    print("\n" + "=" * 70)
    print(f"TOKENIZER: {tokenizer_name}")
    print("=" * 70)

    for lang in languages:

        lines = read_lines(
            CORPUS / f"{lang}.devtest"
        )

        original_tokens = 0
        preserved_case_tokens = 0

        for line in lines:

            original_tokens += len(
                encode(line.lower())
            )

            preserved_case_tokens += len(
                encode(line)
            )

        original_fertility = original_tokens / len(lines)
        preserved_case = preserved_case_tokens / len(lines)

        change = preserved_case - original_fertility
        pct_change = change / original_fertility * 100

        print(f"\n{lang}")
        print(f"lowercase tokens/sentence : {original_fertility:.3f}")
        print(f"preserve-case tokens/sent : {preserved_case:.3f}")
        print(f"absolute change            : {change:.3f}")
        print(f"relative change            : {pct_change:.4f}%")