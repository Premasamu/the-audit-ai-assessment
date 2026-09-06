from pathlib import Path
import unicodedata

CORPUS = Path("ai-assessment/partA/corpus/flores")

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
    path = CORPUS / f"{lang}.devtest"
    lines = read_lines(path)

    words_split_space = sum(len(line.split(" ")) for line in lines)
    words_split = sum(len(line.split()) for line in lines)

    difference = words_split - words_split_space

    print(f"\n{lang}")
    print(f"words using split(' ') : {words_split_space}")
    print(f"words using split()    : {words_split}")
    print(f"difference             : {difference}")

    if words_split_space > 0:
        pct = difference / words_split_space * 100
        print(f"relative difference    : {pct:.4f}%")