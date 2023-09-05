from estruturasDados import *


class label:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return f"{self.label}"


class tresEnderecos:
    def __init__(self):
        self.codigo = []
        self.contadorVarTemp = 0
        self.dicionarioVariavel = {}

    def novaVarTemp(self):
        temp = f"var{self.contadorVarTemp}"
        self.contadorVarTemp += 1
        return temp

    def getVarTemp(self, varOriginal) -> str:
        escopo = varOriginal.getEscopoSTR()
        return self.dicionarioVariavel[varOriginal.valor + escopo]

    def gerarCodigo(self, ast: list[AST]):
        for no in ast:

            if isinstance(no.tipo, label):                                  #LABEL
                self.codigo.append(no.tipo.__str__())
            elif isinstance(no, NoImprimir):                                #IMPRIMIR
                self.imprimir(no)
            elif isinstance(no.tipo, NoDeclaracaoVariavel):                 #DECLARACAO VARIAVEL
                self.declaracaoVariavel(no.tipo)
            elif isinstance(no.tipo, NoDeclaracaoFuncao):                   #DECLARACAO FUNCAO
                self.declaracaoFuncao(no.tipo)
                self.gerarCodigo(no.filhos)
                if isinstance(no.tipo.retorno, NoTipo):
                    retorno = self.getVarTemp(no.tipo.retorno)
                else:
                    temp = self.novaVarTemp()
                    self.codigo.append(f"{temp} = {self.expressao(no.tipo.retorno)}")
                    retorno = temp
                self.codigo.append(f"return {retorno}")
            elif isinstance(no.tipo, NoDeclaracaoProcedimento):             #DECLARACAO PROCEDIMENTO
                self.declaracaoProcedimento(no.tipo)
                self.gerarCodigo(no.filhos)
            elif isinstance(no.tipo, NoChamadaFuncProc):                    #CHAMADA DE PROCEDIMENTO
                self.chamadaFuncProc(no.tipo)
            elif isinstance(no, NoAtribuicao):                              #ATRIBUICAO
                self.atribuicao(no)
            elif isinstance(no.tipo, NoEnquanto):                           #ENQUANTO
                self.enquanto(no.tipo)
                no.filhos.append(AST(label(f"FIM_{no.tipo.__str__()}:")))
                self.gerarCodigo(no.filhos)
            elif isinstance(no.tipo, NoSe):                                 #SE
                self.se(no.tipo)
                if not (no.tipo.casoContrario is None):                     #SENAO ESCOPO
                    no.filhos.append(AST(label(f"goto FIM_{no.tipo.casoContrario.tipo.__str__()}")))
                    no.tipo.casoContrario.filhos.append(AST(label(f"FIM_{no.tipo.casoContrario.tipo.__str__()}:")))
                no.filhos.append(AST(label(f"FIM_{no.tipo.__str__()}:")))
                self.gerarCodigo(no.filhos)
                if isinstance(no.tipo.casoContrario, AST):
                    self.gerarCodigo(no.tipo.casoContrario.filhos)



    def getValorPadrao(self, variavel: NoTipo):
        valor = ""
        if isinstance(variavel, NoTipoInt):
            valor = 0
        elif isinstance(variavel, NoTipoBool):
            valor = "false"
        return valor

    def declaracaoVariavel(self, declaracao: NoDeclaracaoVariavel, valor=None):
        temp = self.novaVarTemp()
        escopo = declaracao.getEscopoSTR()
        self.dicionarioVariavel[declaracao.id + escopo] = temp

        if valor is None:
            valor = self.getValorPadrao(declaracao.tipo)

        linha = f"{temp} = {valor}"
        self.codigo.append(linha)

    #"""
    def declaracaoFuncao(self, declaracao: NoDeclaracaoFuncao):
        self.codigo.append(f"{declaracao.__str__()}:")
        index = 0
        for parametro in declaracao.parametros:
            self.declaracaoVariavel(parametro, f"param {index}")
            index += 1



    def declaracaoProcedimento(self, declaracao: NoDeclaracaoProcedimento):
        self.codigo.append(f"{declaracao.__str__()}:")
        index = 0
        for parametro in declaracao.parametros:
            self.declaracaoVariavel(parametro, f"param {index}")
            index += 1
    """
    def declaracaoFuncao(self, declaracao: NoDeclaracaoFuncao):
        linha = f"function {declaracao.id} ("
        index = 1
        for parametro in declaracao.parametros:
            linha += parametro.tipo.__str__()
            if index < len(declaracao.parametros):
                linha += ", "
        linha += f") -> {declaracao.retorno.__str__()};"


    def declaracaoProcedimento(self, declaracao: NoDeclaracaoProcedimento):
        linha = f"function {declaracao.id} ("
        index = 1
        for parametro in declaracao.parametros:
            linha += parametro.tipo.__str__()
            if index < len(declaracao.parametros):
                linha += ", "
        linha += f");"
    """

    def atribuicao(self, varAtribuicao: NoAtribuicao):
        linha = f"{self.getVarTemp(varAtribuicao.tipo)} = "

        if isinstance(varAtribuicao.valor, NoExpressaoAritimetica):
            linha += self.expressao(varAtribuicao.valor)
        elif isinstance(varAtribuicao.valor, NoExpressaoBool):
            linha += self.expressao(varAtribuicao.valor)
        elif isinstance(varAtribuicao.valor, NoChamadaFuncProc):
            linha += self.chamadaFuncProc(varAtribuicao.valor)
            # self.verificarTipos(varAtribuicao.tipo, varAtribuicao.valor.retorno)
        elif isinstance(varAtribuicao.valor, NoTipoId):
            linha += f"{self.getVarTemp(varAtribuicao.valor)}"
        elif isinstance(varAtribuicao.valor, NoTipo):
            linha += f"{varAtribuicao.valor.valor}"

        self.codigo.append(linha)

    def expressao(self, varExpressao: NoExpressao):
        linha = ""

        if isinstance(varExpressao.termoA, NoTipoId):
            temp = self.getVarTemp(varExpressao.termoA.tipo)
            linha += temp
        elif isinstance(varExpressao.termoA, NoTipo):
            linha += varExpressao.termoA.valor

        linha += " " + varExpressao.operador + " "

        if isinstance(varExpressao.termoB, NoTipoId):
            temp = self.getVarTemp(varExpressao.termoB.tipo)
            linha += temp
        elif isinstance(varExpressao.termoB, NoTipo):
            linha += varExpressao.termoB.valor

        return linha

    def enquanto(self, enquanto: NoEnquanto):
        temp = self.novaVarTemp()
        self.codigo.append(f"{temp} = {self.expressao(enquanto.condicao)}")
        self.codigo.append(f"if {temp} goto {enquanto.__str__()}")
        self.codigo.append(f"goto FIM_{enquanto.__str__()}")
        self.codigo.append(f"{enquanto.__str__()}:")

    def se(self, se: NoSe):
        temp = self.novaVarTemp()
        self.codigo.append(f"{temp} = {self.expressao(se.condicao)}")
        self.codigo.append(f"if {temp} goto {se.__str__()}")
        self.codigo.append(f"goto FIM_{se.__str__()}")
        self.codigo.append(f"{se.__str__()}:")

    def seNao(self, se: NoSeNao):

        self.codigo.append(f"goto FIM_{se.__str__()}")
        self.codigo.append(f"{se.__str__()}:")

    def imprimir(self, saida: NoImprimir):
        imprimir = ""
        if isinstance(saida.tipo, NoTipoId):
            imprimir = self.getVarTemp(saida.tipo)
        elif isinstance(saida.tipo, NoTipo):
            imprimir = saida.tipo.valor
        elif isinstance(saida.tipo, NoExpressao):
            imprimir = self.novaVarTemp()
            self.codigo.append(f"{imprimir} = {self.expressao(saida.tipo)}")
        elif isinstance(saida.tipo, NoChamadaFuncProc):
            imprimir = self.chamadaFuncProc(saida.tipo)
        self.codigo.append(f"param {imprimir}")
        self.codigo.append("call print")

    def chamadaFuncProc(self, chadamaFunc: NoChamadaFuncProc):
        temp = self.novaVarTemp()

        index = 0

        for parametro in chadamaFunc.parametros:
            if isinstance(parametro.tipo, NoTipoId):
                valor = self.getVarTemp(parametro.tipo)
            elif isinstance(parametro.tipo, NoTipo):
                valor = parametro.valor
            else:
                valor = self.expressao(parametro.tipo)
            self.codigo.append(f"param {index} = {valor}")
            index += 1


        self.codigo.append(f"call {chadamaFunc}, {temp}")
        return temp