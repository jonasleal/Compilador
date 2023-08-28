import re
import palavraReservada as PR
from tokenn import Token

class Lexica:

    def __init__(self, input_text):
        self.tokens = self.buscarTokens(input_text)
        self.tokenIndexAtual = 0

    def buscarTokens(self, input_text):
        tokens = []
        posicao = 0
        linha = 1
        coluna = 1

        while posicao < len(input_text):
            encontrado = None
            for token_type, padrao in PR.TOKENS_GRAMATICA:
                regex = re.compile(padrao)
                encontrado = regex.match(input_text, posicao)
                if encontrado:
                    valor = encontrado.group(0)
                    if token_type == "QUEBRA_LINHA":
                        linha += 1
                    elif token_type != "ESPACO_BRANCO":
                        tokens.append(Token(token_type, valor, linha, encontrado.start()))

                    break
            if not encontrado:
                raise ValueError(f"Invalid character: {input_text[posicao]}")
            posicao = encontrado.end()

        tokens.append(Token("EOF", "", linha, 0))
        return tokens

    def getProxToken(self):
        if self.tokenIndexAtual < len(self.tokens):
            token = self.tokens[self.tokenIndexAtual]
            self.tokenIndexAtual += 1
            return token
        return self.tokens[len(self.tokens)-1]

    def lookAHead(self):
        if self.tokenIndexAtual < len(self.tokens):
            token = self.tokens[self.tokenIndexAtual].token_type
            return token
        return self.tokens[len(self.tokens)-1].token_type