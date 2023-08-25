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




