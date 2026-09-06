from pathlib import Path
import unicodedata
import tiktoken
import regex
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


tokenizers = {
    "gpt2": lambda text: gpt2.encode(text),
    "xlmr": lambda text: xlmr.encode(
        text,
        add_special_tokens=False
    ),
}


languages = ["eng_Latn", "hin_Deva", "kan_Knda", "tam_Taml"]


for tokenizer_name, encode in tokenizers.items():

    print("\n" + "=" * 70)
    print(f"TOKENIZER: {tokenizer_name}")
    print("=" * 70)

    for lang in languages:

        lines = read_lines(
            CORPUS / f"{lang}.devtest"
        )

        total_tokens = 0
        total_words = 0
        total_codepoints = 0
        total_graphemes = 0
        total_bytes = 0

        for line in lines:

            total_tokens += len(encode(line))

            total_words += len(line.split())

            total_codepoints += len(line)

            total_graphemes += len(
                regex.findall(r"\X", line)
            )

            total_bytes += len(
                line.encode("utf-8")
            )

        tok_per_word = total_tokens / total_words
        tok_per_codepoint = total_tokens / total_codepoints
        tok_per_grapheme = total_tokens / total_graphemes
        tok_per_byte = total_tokens / total_bytes

        print(f"\n{lang}")
        print(f"sentences               : {len(lines)}")
        print(f"tokens                  : {total_tokens}")
        print(f"words                   : {total_words}")
        print(f"code points             : {total_codepoints}")
        print(f"grapheme clusters       : {total_graphemes}")
        print(f"UTF-8 bytes             : {total_bytes}")
        print(f"tokens / word           : {tok_per_word:.6f}")
        print(f"tokens / code point     : {tok_per_codepoint:.6f}")
        print(f"tokens / grapheme       : {tok_per_grapheme:.6f}")
        print(f"tokens / byte           : {tok_per_byte:.6f}")