import tiktoken

enc = tiktoken.get_encoding("gpt2")


def read_lines(path):
    lines = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()

            if not line:
                continue

            lines.append(line)

    return lines


def analyze(path):
    lines = read_lines(path)

    # Current fertility.py method
    per_line = []

    total_tokens = 0
    total_words = 0

    for line in lines:
        line = line.lower()

        tokens = enc.encode(line)
        words = line.split()

        per_line.append(len(tokens) / len(words))

        total_tokens += len(tokens)
        total_words += len(words)

    line_average = sum(per_line) / len(per_line)

    # Corpus-level method
    corpus_average = total_tokens / total_words

    return line_average, corpus_average


for lang, path in [
    ("eng", "corpus_sample/eng_sample.txt"),
    ("hin", "corpus_sample/hin_sample.txt"),
]:
    line_avg, corpus_avg = analyze(path)

    print(lang)
    print("Per-line average :", line_avg)
    print("Corpus aggregate :", corpus_avg)
    print()