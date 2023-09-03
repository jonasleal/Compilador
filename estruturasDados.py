class NoTipo:
    def __init__(self, valor, linha):
        self.valor = valor
        self.linha = linha
        self.escopo = []

    @staticmethod
    def resolve(token_type, valor, linha):
        if token_type == "ID":
            return NoTipoId(valor, linha)
        elif token_type == "TIPO_INT" or \
                token_type == "INT" or \
                token_type == "int":
            return NoTipoInt(valor, linha)
        elif token_type == "TIPO_BOOL" or \
                token_type == "BOOL" or \
                token_type == "bool":
            return NoTipoBool(valor, linha)


class NoTipoId(NoTipo):

    def __str__(self) -> str:
        return self.valor


class NoTipoInt(NoTipo):

    def __str__(self) -> str:
        return "INT"


class NoTipoBool(NoTipo):

    def __str__(self) -> str:
        return "BOOL"


class NoDeclaracaoVariavel:
    def __init__(self, tipo: NoTipo, id: str, linha):
        self.tipo: NoTipo = tipo
        self.id = id
        self.valor = None
        self.linha = linha
        self.escopo = []

    def __str__(self) -> str:
        return f"{self.tipo.__str__()}"


class NoAtribuicao:
    def __init__(self, tipo: NoTipo, id: str, valor, linha):
        self.tipo: NoTipo = tipo
        self.id = id
        self.valor = valor
        self.linha = linha


class NoParametro:
    def __init__(self, valor: str, tipo, linha):
        self.valor = valor
        self.tipo = tipo
        self.linha = linha
        self.escopo = []

    def __str__(self) -> str:
        return NoTipo.resolve(self.tipo, self.valor, self.linha).__str__()


class NoChamadaFuncProc:
    def __init__(self, id: str, parametros: list[NoParametro], linha, retorno=None):
        self.id = id
        self.parametros: list[NoParametro] = parametros
        self.retorno = retorno
        self.linha = linha

    def __str__(self):
        parametros = ""
        filhos = len(self.parametros) - 1
        for parametro in self.parametros:
            parametros += parametro.__str__()
            if (filhos > 0):
                filhos -= 1
                parametros += ","
        if self.retorno == None:
            return f"{self.id}({parametros})"
        else:
            return f"{self.retorno} {self.id}({parametros})"



class NoDeclaracaoFuncao:
    def __init__(self, retorno: NoTipo, id: str, parametros, linha):
        self.id = id
        self.parametros = parametros
        self.retorno = retorno
        self.linha = linha
        self.escopo = []

    def __str__(self):
        parametros = ""
        filhos = len(self.parametros) - 1
        for parametro in self.parametros:
            parametros += parametro.__str__()
            if (filhos > 0):
                filhos -= 1
                parametros += ","
        return f"{self.id}({parametros})"


class NoDeclaracaoProcedimento:
    def __init__(self, id: str, parametros, linha):
        self.id = id
        self.parametros = parametros
        self.linha = linha

    def __str__(self):
        parametros = ""
        filhos = len(self.parametros) - 1
        for parametro in self.parametros:
            parametros += parametro.__str__()
            if (filhos > 0):
                filhos -= 1
                parametros += ","
        return f"{self.id}({parametros})"


class NoExpressao:
    def __init__(self, termoA, operador, termoB, linha):
        self.termoA: NoTipo = termoA
        self.operador = operador
        self.termoB: NoTipo = termoB
        self.linha = linha

    def __str__(self):
        return f"{self.termoA}{self.operador}{self.termoB}"


class NoExpressaoAritimetica(NoExpressao):
    def __init__(self, termoA, operador, termoB, linha):
        super().__init__(termoA, operador, termoB, linha)


class NoExpressaoBool(NoExpressao):
    def __init__(self, termoA, operador, termoB, linha):
        super().__init__(termoA, operador, termoB, linha)


class NoImprimir:
    def __init__(self, tipo: NoTipo, linha):
        self.tipo: NoTipo = tipo
        self.linha = linha


class NoSe:
    def __init__(self, condicao, linha, casoContario=None):
        self.condicao = condicao
        self.casoContrario: NoSeNao = casoContario
        self.linha = linha
        self.escopo = []

    def __str__(self):
        return f"SE_LINHA_{self.linha}"


class NoSeNao:
    def __init__(self, condicao, linha):
        self.condicao = condicao
        self.linha = linha
        self.escopo = []

    def __str__(self):
        return f"SENAO_LINHA_{self.linha}"


class NoEnquanto:
    def __init__(self, condicao, linha):
        self.condicao = condicao
        self.linha = linha
        self.escopo = []

    def __str__(self):
        return f"ENQUANTO_LINHA_{self.linha}"


class AST:
    def __init__(self, tipo, filhos=None):
        if filhos is None:
            filhos = []
        self.tipo = tipo
        self.filhos = filhos
