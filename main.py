from src.input.parse import DocumentLoader, TextParser


path = "data/aresin_doc.docx"
doc = DocumentLoader(path)

text = doc.text
chapter_one = doc.chapters['Stumme Tauben']

parser_full = TextParser(text)
parser_chap = TextParser(chapter_one)

print(parser_full.chars)
print(parser_chap.syllables)
