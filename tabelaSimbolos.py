class TabelaSimbolos:

    def __init__(self):
        self.simbolos = {}
        self.delEsc = " | "  # Delimitador de escopo

    def addSimbolo(self, id: str, simbolo: object, escopo: list[str]):
        assinatura = id
        for i in escopo:
            assinatura += self.delEsc + i

        if assinatura in self.simbolos:
            raise ValueError(f"Ja existe uma simbolo com o identificador {id}")
        self.simbolos[assinatura] = simbolo

    def getSimbolo(self, id: str, escopo: list[str]):
        assinatura = id
        encontrado = None
        for i in escopo:
            assinatura += self.delEsc + i
            encontrado = self.simbolos.get(assinatura)
            if not (encontrado is None):
                break

        return encontrado

    def imprimirTudo(self):
        for i in self.simbolos:
            print(f"Nome: {i}, instancia de ")
