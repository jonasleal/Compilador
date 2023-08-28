from lexica import Lexica
from parser import Parser

with open("codigo.txt", 'r') as arquivo:
    codigo = arquivo.read()

listaTokens = Lexica(codigo)
#"""
for token in listaTokens.tokens:
    print(f"Token: {token.token_type}\tValor: {token.valor}\tLinha: {token.linha}")
#"""
print("Analise lexica: OK")
parser = Parser(listaTokens)
parser.inicio()
print("Analise sintatica: OK")
