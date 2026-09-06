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

    token_total = 0
    words_space_total = 0
    words_normal_total = 0

    for line in lines:
        token_total += len(enc.encode(line))
        words_space_total += len(line.split(" "))
        words_normal_total += len(line.split())

    fertility_space = token_total / words_space_total
    fertility_normal = token_total / words_normal_total

    change = fertility_normal - fertility_space
    pct_change = change / fertility_space * 100

    print(f"\n{lang}")
    print(f"tokens                  : {token_total}")
    print(f"fertility split(' ')    : {fertility_space:.6f}")
    print(f"fertility split()       : {fertility_normal:.6f}")
    print(f"absolute change         : {change:.6f}")
    print(f"relative change         : {pct_change:.4f}%")