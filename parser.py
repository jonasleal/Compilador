import palavraReservada as PR

class Parser:
    def __init__(self, listaTokens):
        self.listaTokens = listaTokens
        self.tokenAtual = self.listaTokens.getProxToken()

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

    def id(self):
        if self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "ATRIBUICAO":
            self.consumir("ID")
            self.atribuicao()
        elif self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "PARENT_ESQ":
            self.chamada_func_proc()
        else:
            self.erro("ATRIBUICAO ou PARENT_ESQ")

    def corpo_inicio(self):
        if self.tokenAtual.token_type == "DECLARACAO_VARIAVEL":
            self.declaracao_variavel()
        elif self.tokenAtual.token_type == "DECLARACAO_FUNCAO":
            self.declaracao_funcao()
        elif self.tokenAtual.token_type == "DECLARACAO_PROCEDIMENTO":
            self.declaracao_procedimento()
        elif self.tokenAtual.token_type == "ID":
            self.id()
        else:
            self.erro("DECLARACAO_VARIAVEL, DECLARACAO_FUNCAO, DECLARACAO_PROCEDIMENTO,CHAMADA_FUNCAO, "
                      "CHAMADA_PROCEDIMENTO")

    def declaracao_variavel(self):
        self.consumir("DECLARACAO_VARIAVEL")
        self.tipo()
        self.consumir("ID")
        self.consumir("PONTO_VIRGULA")

    def tipo(self):
        msg = ""
        for token_type, valor in PR.TOKEN_TIPO:
            if self.tokenAtual.token_type == token_type:
                self.consumir(token_type)
                return
            else:
                msg += token_type + ", "
        self.erro(msg)

    def declaracao_funcao(self):
        self.consumir("DECLARACAO_FUNCAO")
        self.tipo()
        self.cabecalho()
        self.corpo_funcao()

    def declaracao_procedimento(self):
        self.consumir("DECLARACAO_PROCEDIMENTO")
        self.cabecalho()
        self.corpo_funcao()

    def cabecalho(self):
        self.consumir("ID")
        self.consumir("PARENT_ESQ")
        if self.tokenAtual.token_type != "PARENT_DIR":
            self.parametros()
        self.consumir("PARENT_DIR")

    def corpo(self):
        self.consumir("CHAVE_ESQ")
        self.instrucoes()
        self.consumir("CHAVE_DIR")

    def corpo_funcao(self):
        self.consumir("CHAVE_ESQ")
        if self.tokenAtual.token_type != "RETORNO":
            self.instrucoes()
        if self.tokenAtual.token_type == "RETORNO":
            self.retorno()
        self.consumir("CHAVE_DIR")

    def parametros(self):
        self.tipo()
        self.consumir("ID")
        if self.tokenAtual.token_type == "VIRGULA":
            self.consumir("VIRGULA")
            self.parametros()

    def instrucoes(self):
        if self.tokenAtual.token_type == "DECLARACAO_VARIAVEL":
            self.declaracao_variavel()
        elif self.tokenAtual.token_type == "ID":
            self.id()
        elif self.tokenAtual.token_type == "SE":
            self.se()
        elif self.tokenAtual.token_type == "ENQUANTO":
            self.enquanto()
        elif self.tokenAtual.token_type == "IMPRIMIR":
            self.imprimir()
        else:
            self.erro("DECLARACAO_VARIAVEL, DECLARACAO_FUNCAO, DECLARACAO_PROCEDIMENTO,CHAMADA_FUNCAO, "
                      "CHAMADA_PROCEDIMENTO")
        if self.tokenAtual.token_type != "CHAVE_DIR" and self.tokenAtual.token_type != "RETORNO":
            self.instrucoes()

    def chamada_func_proc(self):
        self.consumir("ID")
        self.consumir("PARENT_ESQ")
        while self.tokenAtual.token_type != "PARENT_DIR":
            if self.tokenAtual.token_type == "ID":
                self.consumir(self.tokenAtual.token_type)
            else:
                for token_type, valor in PR.VALOR_LITERAL:
                    if self.tokenAtual.token_type == token_type:
                        self.consumir(token_type)
            if self.tokenAtual.token_type == "VIRGULA":
                self.consumir("VIRGULA")
        self.consumir("PARENT_DIR")
        self.consumir("PONTO_VIRGULA")

    def atribuicao(self):
        self.consumir("ATRIBUICAO")
        if self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "PONTO_VIRGULA":
            self.consumir("ID")
            self.consumir("PONTO_VIRGULA")
        elif self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "PARENT_ESQ":
            self.chamada_func_proc()
        elif self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "OP_BOOLEANO":
            self.expressoes()
            self.consumir("PONTO_VIRGULA")
        elif self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "OP_ARITIMETICO":
            self.expressoes()
            self.consumir("PONTO_VIRGULA")
        else:
            msg = "ID, PONTO_VIRGULA, "
            for token_type, valor in PR.VALOR_LITERAL:
                if self.tokenAtual.token_type == token_type:
                    self.expressoes()
                    self.consumir("PONTO_VIRGULA")
                    return
                else:
                    msg += token_type + ", "
            self.erro(msg)

    def se(self):
        self.consumir("SE")
        self.consumir("PARENT_ESQ")
        self.expressao_bool()
        self.consumir("PARENT_DIR")
        self.corpo()
        if self.tokenAtual.token_type == "SENAO":
            self.consumir("SENAO")
            self.corpo()

    def enquanto(self):
        self.consumir("ENQUANTO")
        self.consumir("PARENT_ESQ")
        self.expressao_bool()
        self.consumir("PARENT_DIR")
        self.corpo()

    def expressoes(self):

        msg = ""
        for token_type, valor in PR.VALOR_LITERAL:
            if self.tokenAtual.token_type == token_type or self.tokenAtual.token_type == "ID" and\
                    self.listaTokens.lookAHead() == "PONTO_VIRGULA":
                self.consumir(self.tokenAtual.token_type)
                return
            elif self.tokenAtual.token_type == token_type or self.tokenAtual.token_type == "ID" and\
                    self.listaTokens.lookAHead() == "OP_BOOLEANO":
                self.expressao_bool()
                return
            elif self.tokenAtual.token_type == token_type or self.tokenAtual.token_type == "ID" and\
                     self.listaTokens.lookAHead() == "OP_ARITIMETICO":
                self.expressao_aritimetica()
                return
            else:
                msg += token_type + ", "
        self.erro(msg)

    def expressao_bool(self):
        self.termo_bool()
        self.consumir("OP_BOOLEANO")
        self.termo_bool()

    def termo_bool(self):
        if self.tokenAtual.token_type == "ID":
            self.consumir("ID")
        elif self.tokenAtual.token_type == "TIPO_BOOL":
            self.consumir("TIPO_BOOL")
        elif self.tokenAtual.token_type == "TIPO_INT":
            self.consumir("TIPO_INT")
        else:
            self.erro("ID, TIPO_BOOL ou TIPO_INT")

    def expressao_aritimetica(self):
        self.termo_aritimatico()
        self.consumir("OP_ARITIMETICO")
        self.termo_aritimatico()

    def termo_aritimatico(self):
        if self.tokenAtual.token_type == "ID":
            self.consumir("ID")
        elif self.tokenAtual.token_type == "TIPO_INT":
            self.consumir("TIPO_INT")
        else:
            self.erro("ID ou TIPO_INT")

    def imprimir(self):
        self.consumir("IMPRIMIR")
        self.consumir("PARENT_ESQ")
        if self.tokenAtual.token_type == "ID":
            self.consumir("ID")
        elif self.tokenAtual.token_type == "TIPO_BOOL":
            self.consumir("TIPO_BOOL")
        elif self.tokenAtual.token_type == "TIPO_INT":
            self.consumir("TIPO_INT")
        else:
            self.erro("ID, TIPO_BOOL ou TIPO_INT")

        self.consumir("PARENT_DIR")
        self.consumir("PONTO_VIRGULA")

    #REVISAR
    def retorno(self):
        self.consumir("RETORNO")
        if self.tokenAtual.token_type == "ID" and self.listaTokens.lookAHead() == "PARENT_ESQ":
            self.chamada_func_proc()
        else:
            self.expressoes();

        self.consumir("PONTO_VIRGULA")
