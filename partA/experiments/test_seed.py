import subprocess
import sys

cmd = [
    sys.executable,
    "fertility.py",
    "--corpus",
    "eng=corpus_sample/eng_sample.txt",
    "--corpus",
    "hin=corpus_sample/hin_sample.txt",
    "--tokenizer",
    "gpt2",
]

print("Run 1:")
result1 = subprocess.run(cmd, capture_output=True, text=True)
print(result1.stdout)

print("Run 2:")
result2 = subprocess.run(cmd, capture_output=True, text=True)
print(result2.stdout)

print("Outputs identical:", result1.stdout == result2.stdout)