lines = [
    "short sentence",
    "this is a much much much much longer sentence with many words"
]

token_counts = [4, 20]

per_line = []
for line, tokens in zip(lines, token_counts):
    words = line.split()
    per_line.append(tokens / len(words))

line_average = sum(per_line) / len(per_line)

total_tokens = sum(token_counts)
total_words = sum(len(line.split()) for line in lines)

corpus_average = total_tokens / total_words

print("Per-line fertility:", line_average)
print("Corpus-level fertility:", corpus_average)