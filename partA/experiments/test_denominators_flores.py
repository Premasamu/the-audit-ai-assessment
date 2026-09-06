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

    total_tokens = 0
    total_words = 0
    total_codepoints = 0
    total_bytes = 0

    for line in lines:

        total_tokens += len(enc.encode(line))
        total_words += len(line.split())
        total_codepoints += len(line)
        total_bytes += len(line.encode("utf-8"))

    tok_per_word = total_tokens / total_words
    tok_per_codepoint = total_tokens / total_codepoints
    tok_per_byte = total_tokens / total_bytes

    print(f"\n{lang}")
    print(f"tokens                  : {total_tokens}")
    print(f"words                   : {total_words}")
    print(f"unicode code points     : {total_codepoints}")
    print(f"UTF-8 bytes             : {total_bytes}")
    print(f"tokens / word           : {tok_per_word:.6f}")
    print(f"tokens / code point     : {tok_per_codepoint:.6f}")
    print(f"tokens / UTF-8 byte     : {tok_per_byte:.6f}")