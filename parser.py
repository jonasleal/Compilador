import palavraReservada as PR
from estruturasDados import *

class Parser:
    def __init__(self, listaTokens):
        self.listaTokens = listaTokens
        self.tokenAtual = self.listaTokens.getProxToken()
        self.arvoreSintatica = []

    def erro(self, tokenEsperado):
        raise SyntaxError(f"Na linha {self.tokenAtual.linha}, palavra '{self.tokenAtual.valor}' era esperado o token {tokenEsperado}, mas recebeu {self.tokenAtual.token_type}")

    def consumir(self, tokenEsperado):
        if self.tokenAtual.token_type == tokenEsperado:
            self.tokenAtual = self.listaTokens.getProxToken()
        else:
            self.erro(tokenEsperado)

    def inicio(self):
        self.corpo_inicio()
        while self.tokenAtual.token_type != "EOF":
            self.corpo_inicio()
        return self.arvoreSintatica

    def id(self):
        if self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "ATRIBUICAO":
            id = self.tokenAtual.valor
            self.consumir("ID")
            valor = self.atribuicao()
            return NoAtribuicao(None, id, valor, self.tokenAtual.linha)
        elif self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "PARENT_ESQ":
            return self.chamada_func_proc()
        else:
            self.erro("ATRIBUICAO ou PARENT_ESQ")

    def corpo_inicio(self):
        if self.tokenAtual.token_type == "DECLARACAO_VARIAVEL":
            self.arvoreSintatica.append(self.declaracao_variavel())
        elif self.tokenAtual.token_type == "DECLARACAO_FUNCAO":
            self.arvoreSintatica.append(self.declaracao_funcao())
        elif self.tokenAtual.token_type == "DECLARACAO_PROCEDIMENTO":
            self.arvoreSintatica.append(self.declaracao_procedimento())
        elif self.tokenAtual.token_type == "ENQUANTO":
            self.arvoreSintatica.append(self.se())
        elif self.tokenAtual.token_type == "IMPRIMIR":
            self.arvoreSintatica.append(self.imprimir())
        elif self.tokenAtual.token_type == "ID":
            self.arvoreSintatica.append(self.id())
        else:
            self.erro("DECLARACAO_VARIAVEL, DECLARACAO_FUNCAO, DECLARACAO_PROCEDIMENTO,CHAMADA_FUNCAO, "
                      "CHAMADA_PROCEDIMENTO")

    def declaracao_variavel(self):
        self.consumir("DECLARACAO_VARIAVEL")
        tipo = self.tipo()
        id = self.tokenAtual.valor
        linha = self.tokenAtual.linha
        self.consumir("ID")
        self.consumir("PONTO_VIRGULA")

        return AST(NoDeclaracaoVariavel(tipo, id, linha))

    def tipo(self):
        msg = ""
        for token_type, valor in PR.TOKEN_TIPO:
            if self.tokenAtual.token_type == token_type:
                tipo = NoTipo.resolve(self.tokenAtual.token_type, self.tokenAtual.valor, self.tokenAtual.linha )
                self.consumir(token_type)
                return tipo
            else:
                msg += token_type + ", "
        self.erro(msg)

    def declaracao_funcao(self):
        self.consumir("DECLARACAO_FUNCAO")
        linha = self.tokenAtual.linha
        tipoRetorno = self.tipo()
        id, parametros = self.cabecalho()
        corpo = []
        self.corpo_funcao(corpo)
        return AST(NoDeclaracaoFuncao(tipoRetorno, id, parametros, linha), corpo)

    def declaracao_procedimento(self):
        self.consumir("DECLARACAO_PROCEDIMENTO")
        linha = self.tokenAtual.linha
        id, parametros = self.cabecalho()
        corpo = []
        self.corpo_funcao(corpo)
        return AST(NoDeclaracaoProcedimento(id, parametros, linha), corpo)

    def cabecalho(self):
        id = self.tokenAtual.valor
        self.consumir("ID")
        self.consumir("PARENT_ESQ")
        parametros = []
        if self.tokenAtual.token_type != "PARENT_DIR":
            self.parametros(parametros)
        self.consumir("PARENT_DIR")
        return id, parametros

    def corpo(self):
        corpo = []
        self.consumir("CHAVE_ESQ")
        self.instrucoes(corpo)
        self.consumir("CHAVE_DIR")
        return corpo

    def corpo_funcao(self, corpo):
        self.consumir("CHAVE_ESQ")
        retorno = None
        if self.tokenAtual.token_type != "RETORNO":
            self.instrucoes(corpo)
        if self.tokenAtual.token_type == "RETORNO":
            retorno = self.retorno()
        self.consumir("CHAVE_DIR")
        return retorno

    def parametros(self, parametro):
        tipo = self.tipo()
        id = self.tokenAtual.valor
        parametro.append(NoDeclaracaoVariavel(tipo, id, self.tokenAtual.linha))
        self.consumir("ID")
        if self.tokenAtual.token_type == "VIRGULA":
            self.consumir("VIRGULA")
            self.parametros(parametro)

    def instrucoes(self, corpo):
        if self.tokenAtual.token_type == "DECLARACAO_VARIAVEL":
            corpo.append(self.declaracao_variavel())
        elif self.tokenAtual.token_type == "ID":
            corpo.append(self.id())
        elif self.tokenAtual.token_type == "SE":
            corpo.append(self.se())
        elif self.tokenAtual.token_type == "ENQUANTO":
            corpo.append(self.enquanto())
        elif self.tokenAtual.token_type == "IMPRIMIR":
            corpo.append(self.imprimir())
        else:
            self.erro("DECLARACAO_VARIAVEL, DECLARACAO_FUNCAO, DECLARACAO_PROCEDIMENTO,CHAMADA_FUNCAO, "
                      "CHAMADA_PROCEDIMENTO")
        if self.tokenAtual.token_type != "CHAVE_DIR" and self.tokenAtual.token_type != "RETORNO":
            self.instrucoes(corpo)

    def chamada_func_proc(self):
        id = self.tokenAtual.valor
        parametros = []
        linha = self.tokenAtual.linha
        self.consumir("ID")
        self.consumir("PARENT_ESQ")
        while self.tokenAtual.token_type != "PARENT_DIR":
            if self.tokenAtual.token_type == "ID":
                parametros.append(NoParametro(self.tokenAtual.valor, self.tokenAtual.token_type, self.tokenAtual.linha))
                self.consumir(self.tokenAtual.token_type)
            else:
                for token_type, valor in PR.VALOR_LITERAL:
                    if self.tokenAtual.token_type == token_type:
                        parametros.append(NoParametro(self.tokenAtual.valor, self.tokenAtual.token_type, self.tokenAtual.linha))
                        self.consumir(token_type)
            if self.tokenAtual.token_type == "VIRGULA":
                self.consumir("VIRGULA")
            elif self.tokenAtual.token_type != "PARENT_DIR":
                self.erro("VIRGULA ou PARENT_DIR")
        self.consumir("PARENT_DIR")
        self.consumir("PONTO_VIRGULA")
        return NoChamadaFuncProc(id, parametros, linha)

    def atribuicao(self):
        self.consumir("ATRIBUICAO")
        atribuiveis = None
        if self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "PONTO_VIRGULA":
            atribuiveis = NoTipo.resolve(self.tokenAtual.token_type, self.tokenAtual.valor, self.tokenAtual.linha)
            self.consumir("ID")
            self.consumir("PONTO_VIRGULA")
        elif self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "PARENT_ESQ":
            atribuiveis = self.chamada_func_proc()
        elif self.tokenAtual.token_type == "ID" and (self.listaTokens.lookAHead() == "OP_BOOLEANO" or
                                                     self.listaTokens.lookAHead() == "OP_ARITIMETICO"):
            atribuiveis = self.expressoes()
            self.consumir("PONTO_VIRGULA")
        else:
            msg = "ID, PONTO_VIRGULA, "
            for token_type, valor in PR.VALOR_LITERAL:
                if self.tokenAtual.token_type == token_type:
                    atribuiveis = self.expressoes()
                    self.consumir("PONTO_VIRGULA")
                    return atribuiveis
                else:
                    msg += token_type + ", "
            self.erro(msg)
        return atribuiveis

    def se(self):
        linhaSe = self.tokenAtual.linha
        self.consumir("SE")
        self.consumir("PARENT_ESQ")
        condicao = self.expressao_bool()
        self.consumir("PARENT_DIR")
        corpo = self.corpo()
        casoContrario = None
        if self.tokenAtual.token_type == "SENAO":
            linha = self.tokenAtual.linha
            self.consumir("SENAO")
            casoContrario = AST(NoSeNao(None, linha),self.corpo())
        return AST(NoSe(condicao, linhaSe,casoContrario), corpo)

    def enquanto(self):
        linha = self.tokenAtual.linha
        self.consumir("ENQUANTO")
        self.consumir("PARENT_ESQ")
        condicao = self.expressao_bool()
        self.consumir("PARENT_DIR")
        corpo = self.corpo()
        return AST(NoEnquanto(condicao, linha),corpo)

    def expressoes(self):

        msg = ""
        for token_type, valor in PR.VALOR_LITERAL:
            if (self.tokenAtual.token_type == token_type or self.tokenAtual.token_type == "ID") and\
                    self.listaTokens.lookAHead() == "PONTO_VIRGULA":
                atribuicao = NoTipo.resolve(self.tokenAtual.token_type, self.tokenAtual.valor, self.tokenAtual.linha)
                self.consumir(self.tokenAtual.token_type)
                return atribuicao
            elif (self.tokenAtual.token_type == token_type or self.tokenAtual.token_type == "ID") and\
                    self.listaTokens.lookAHead() == "OP_BOOLEANO":

                return self.expressao_bool()

            elif (self.tokenAtual.token_type == token_type or self.tokenAtual.token_type == "ID") and\
                     self.listaTokens.lookAHead() == "OP_ARITIMETICO":
                return self.expressao_aritimetica()

            else:
                msg += token_type + ", "
        self.erro(msg)

    def expressao_bool(self):
        termoA = self.termo_bool()
        operador = self.tokenAtual.valor
        linha = self.tokenAtual.linha
        self.consumir("OP_BOOLEANO")
        termoB = self.termo_bool()
        return NoExpressaoBool(termoA, operador,termoB, linha)

    def termo_bool(self):
        msg = "ID, "
        for token_type, valor in PR.VALOR_LITERAL:
            if self.tokenAtual.token_type == "ID" or self.tokenAtual.token_type == token_type:
                valor = NoTipo.resolve(self.tokenAtual.token_type, self.tokenAtual.valor, self.tokenAtual.linha)
                self.consumir(self.tokenAtual.token_type)
                return valor
            else:
                msg += ", " + token_type

        self.erro(msg)

    def expressao_aritimetica(self):
        termoA = self.termo_aritimatico()
        operador= self.tokenAtual.valor
        linha = self.tokenAtual.linha
        self.consumir("OP_ARITIMETICO")
        termoB = self.termo_aritimatico()
        return NoExpressaoAritimetica(termoA, operador, termoB, linha)

    def termo_aritimatico(self):
        msg = "ID"
        for token_type, valor in PR.VALOR_NUMERICO:
            if self.tokenAtual.token_type == "ID" or self.tokenAtual.token_type == token_type:
                valor = NoTipo.resolve(self.tokenAtual.token_type, self.tokenAtual.valor, self.tokenAtual.linha)
                self.consumir(self.tokenAtual.token_type)
                return valor
            else:
                msg += ", " + token_type

        self.erro(msg)

    def imprimir(self):
        self.consumir("IMPRIMIR")
        self.consumir("PARENT_ESQ")

        msg = "ID, "
        if self.listaTokens.lookAHead() == "PONTO_VIRGULA":
            for token_type, valor in PR.VALOR_LITERAL:
                if self.tokenAtual.token_type == "ID" or self.tokenAtual.token_type == token_type :
                    valor = NoTipo.resolve(self.tokenAtual.token_type, self.tokenAtual.valor, self.tokenAtual.linha)
                    self.consumir(token_type)
                    self.consumir("PARENT_DIR")
                    self.consumir("PONTO_VIRGULA")
                    return NoImprimir(valor, valor.linha)
                else:
                    msg += ", " + token_type
        elif self.listaTokens.lookAHead() == "OP_BOOLEANO" or self.listaTokens.lookAHead() == "OP_ARITIMETICO":
            expressao = self.expressoes()
            self.consumir("PARENT_DIR")
            self.consumir("PONTO_VIRGULA")
            return NoImprimir(expressao, expressao.linha)
        msg += "OP_BOOLEANO, OP_ARITIMETICO"
        self.erro(msg)

    #REVISAR
    def retorno(self):
        self.consumir("RETORNO")
        valor = None
        if self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "PARENT_ESQ":
            valor = self.chamada_func_proc()
        else:
            valor = self.expressoes()

        self.consumir("PONTO_VIRGULA")
        return valor
