from lexica import Lexica
from parser import Parser
from  estruturasDados import AST
from semantica import Semantica
from tresEnderecos import tresEnderecos

print("\n\n---------------------FALTA IMPLEMENTAR SEMANTICA DE PARAR E CONTINUE------------------------\n\n")

with open("codigo.txt", 'r') as arquivo:
    codigo = arquivo.read()

listaTokens = Lexica(codigo)
"""
for token in listaTokens.tokens:
    print(f"Token: {token.token_type}\tValor: {token.valor}\tLinha: {token.linha}")
"""
print("----------------------Analise lexica: OK-----------------------")
parser = Parser(listaTokens)
ast = parser.inicio()
print("----------------------Analise sintatica: OK--------------------")
"""
for i in ast:
    tipoI = type(i)
    filhosI = []
    linhaI = 0

    if tipoI == AST:
        tipoI = type(i.tipo)
        filhosI = i.filhos
        linhaI = i.tipo.linha
    else:
        linhaI = i.linha

    print(f"Tipo: {tipoI}, numero de filhos: {len(filhosI)}, linha: {linhaI}")
    for j in filhosI:
        tipo = type(j)
        filhos = 0
        linha = 0
        if tipo == AST:
            tipo = type(j.tipo)
            filhos = len(j.filhos)
            linha = j.tipo.linha
        else:
            linha = j.linha
        print(f"\tEscopo de: {type(i.tipo)} Tipo: {tipo}, numero de filhos: {filhos}, linha: {linha}")

"""

semantica = Semantica()
semantica.iniciar(ast)
tresEnd = tresEnderecos()
tresEnd.gerarCodigo(ast)
for linha in tresEnd.codigo:
    print(linha)
