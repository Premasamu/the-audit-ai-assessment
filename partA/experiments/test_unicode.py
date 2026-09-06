import unicodedata

samples = [
    ("English", "Please keep the books in the cupboard."),
    ("Hindi", "मुझे सुबह की चाय बहुत पसंद है।"),
]

for language, text in samples:
    codepoints = len(text)
    utf8_bytes = len(text.encode("utf-8"))

    print(language)
    print("Text:", text)
    print("Python len() / code points:", codepoints)
    print("UTF-8 bytes:", utf8_bytes)
    print("Bytes per code point:", utf8_bytes / codepoints)
    print()