class Token:
    linha = -1
    coluna = -1
    tipo = ""
    palavra = ""
    escopo = ""

    def __init__(self, linha: int, coluna: int, tipo: str, palavra: str, escopo: str):
        self.linha = linha
        self.coluna = coluna
        self.tipo = tipo
        self.palavra = palavra
        self.escopo = escopo


