import palavraReservada
import meuToken
from enum import Enum


class TIPOCARAC(Enum):
    ALFABETICO = 1
    NUMERICO = 2
    ESPECIAL = 3
    UNDERLINE = 4


class Lexica:

    def __init__(self, nomeArq):
        self.nomeArq = nomeArq

    def imprimirToken(self, tk: meuToken.Token):
        print(
            f"Linha: {tk.linha}, Coluna: {tk.coluna}, Tipo: {tk.tipo}, Palavra: {tk.palavra}")

    def verificar(self):
        with open(self.nomeArq, 'r') as arquivo:
            linhas = arquivo.readlines()
            nLinha = 0

            for linha in linhas:
                nLinha += 1
                inicioPalavra = 1
                nColuna = 1
                palavra = ""
                tipo: TIPOCARAC
                for caractere in linha:

                    if caractere == '\n':
                        continue

                    if caractere.isalpha() or caractere.isnumeric() or caractere == '_':
                        if palavra == "":
                            inicioPalavra = nColuna
                        palavra += caractere

                    else:
                        if caractere in palavraReservada.LOGICO:
                            proxToken = meuToken.Token(nLinha, inicioPalavra, palavraReservada.LOGICO[caractere], caractere,
                                                    "logico")
                            self.imprimirToken(proxToken)
                        elif caractere in palavraReservada.DELIMITADORES:
                            proxToken = meuToken.Token(nLinha, inicioPalavra, palavraReservada.DELIMITADORES[caractere], caractere,
                                                    "delimitador")
                            self.imprimirToken(proxToken)
                        elif caractere in palavraReservada.ATRIBUICAO:
                            proxToken = meuToken.Token(nLinha, inicioPalavra, palavraReservada.ATRIBUICAO[caractere], caractere,
                                                    "atribuicao")
                            self.imprimirToken(proxToken)
                        elif caractere == " " and palavra != "":
                            if palavra in palavraReservada.TOKENS:
                                proxToken = meuToken.Token(nLinha, inicioPalavra, palavraReservada.TOKENS[palavra], palavra,
                                                    "palavra reservada")
                                self.imprimirToken(proxToken)
                            else:
                                eId = True
                                if(palavra[0].isalpha()):
                                    for subStr in palavra.split('_'):
                                        if not subStr.isalnum():
                                            eId = False
                                if eId:
                                    proxToken = meuToken.Token(nLinha, inicioPalavra, palavraReservada.TOKENS['id'], palavra,
                                                               "Identificador")
                                self.imprimirToken(proxToken)
                        else:
                            proxToken = meuToken.Token(nLinha, inicioPalavra, "erro", caractere, "erro")
                            self.imprimirToken(proxToken)
                        palavra = ""

                    nColuna += 1