import lexica

with open("teste.txt", 'r') as arquivo:
    codigo = arquivo.read()

tokens = lexica.Lexica.buscarTokens(codigo)
for token_type, valor in tokens:
    print(f"Token: {token_type}\tValue: {valor}")
