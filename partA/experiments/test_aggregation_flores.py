from pathlib import Path
import unicodedata
import tiktoken

CORPUS = Path("ai-assessment/partA/corpus/flores")
enc = tiktoken.get_encoding("gpt2")


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

    per_line_fertility = []

    total_tokens = 0
    total_words = 0

    for line in lines:
        tokens = enc.encode(line)
        words = line.split()

        token_count = len(tokens)
        word_count = len(words)

        per_line_fertility.append(token_count / word_count)

        total_tokens += token_count
        total_words += word_count

    per_line_average = sum(per_line_fertility) / len(per_line_fertility)
    corpus_aggregate = total_tokens / total_words

    absolute_change = corpus_aggregate - per_line_average
    relative_change = absolute_change / per_line_average * 100

    print(f"\n{lang}")
    print(f"sentences               : {len(lines)}")
    print(f"total tokens            : {total_tokens}")
    print(f"total words             : {total_words}")
    print(f"per-line average        : {per_line_average:.6f}")
    print(f"corpus aggregate        : {corpus_aggregate:.6f}")
    print(f"absolute change         : {absolute_change:.6f}")
    print(f"relative change         : {relative_change:.4f}%")