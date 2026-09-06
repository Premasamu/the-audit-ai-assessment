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
            lines.append(line.lower())

    return lines


corpora = {
    lang: read_lines(CORPUS / f"{lang}.devtest")
    for lang in languages
}


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

        lines = corpora[lang]

        token_counts = [
            len(encode(line))
            for line in lines
        ]

        total_tokens = sum(token_counts)
        sentence_count = len(token_counts)

        mean_tokens = total_tokens / sentence_count

        sorted_counts = sorted(token_counts)

        median_tokens = sorted_counts[
            sentence_count // 2
        ]

        p95_index = int(
            0.95 * sentence_count
        ) - 1

        p95_tokens = sorted_counts[p95_index]

        print(f"\n{lang}")
        print(f"sentences               : {sentence_count}")
        print(f"total tokens            : {total_tokens}")
        print(f"mean tokens/sentence    : {mean_tokens:.3f}")
        print(f"median tokens/sentence  : {median_tokens}")
        print(f"p95 tokens/sentence     : {p95_tokens}")