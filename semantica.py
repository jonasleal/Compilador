from tabelaSimbolos import TabelaSimbolos
from estruturasDados import *


class Semantica:

    def __init__(self):
        self.tabelaSimbolos = TabelaSimbolos()
        self.listaErros = []

    def iniciar(self, ast):
        self.analizar(ast)
        for erro in self.listaErros:
            print(f"Erro {erro}")
        if len(self.listaErros) > 0:
            raise Exception(f"Foram encontrados {len(self.listaErros)} erro(s).")

    def analizar(self, ast: list[AST], escopo=None):
        if escopo is None:
            escopo = [""]

        for no in ast:
            local = escopo.copy()
            if isinstance(no, NoImprimir):
                self.imprimir(no, escopo)
            elif isinstance(no.tipo, NoDeclaracaoVariavel):
                self.declaracaoVariavel(no.tipo, escopo)
            elif isinstance(no.tipo, NoDeclaracaoFuncao):
                self.declaracaoFuncao(no.tipo)
                local.append(no.tipo.__str__())
                self.analizar(no.filhos, local)
                if not (no.tipo.retorno is None):
                    if isinstance(no.tipo.retorno, NoTipo):
                        declaracao = self.tabelaSimbolos.getSimbolo(no.tipo.retorno.valor, local)
                        if not (declaracao is None):
                            no.tipo.retorno.escopo = declaracao.escopo
                        else:
                            self.listaErros.append(
                                f"linha: {no.tipo.retorno.linha}, variavel '{no.tipo.retorno.valor}' não declarada.")

                    elif isinstance(no.tipo.retorno, NoExpressaoAritimetica):
                        self.expressaoAritimetica(no.tipo.retorno, local)
                    elif isinstance(no.tipo.retorno, NoExpressaoBool):
                        self.expressaoBooleana(no.tipo.retorno, local)

            elif isinstance(no.tipo, NoDeclaracaoProcedimento):
                self.declaracaoProcedimento(no.tipo)
                local.append(no.tipo.__str__())
                self.analizar(no.filhos, local)
            elif isinstance(no.tipo, NoChamadaFuncProc):
                self.chamadaFuncProc(no.tipo)
            elif isinstance(no, NoAtribuicao):
                self.atribuicao(no, escopo)
            elif isinstance(no.tipo, NoEnquanto):
                self.enquanto(no.tipo, no.filhos, escopo)
                local.append(no.tipo.__str__())
                self.analizar(no.filhos, local)
            elif isinstance(no.tipo, NoSe):
                self.se(no.tipo, no.filhos, escopo)
                local.append(no.tipo.__str__())
                self.analizar(no.filhos, local)
                if not (no.tipo.casoContrario is None):
                    self.seNao(no.tipo.casoContrario, escopo)

    # 1 - Analizar escopo - OK; 2 - Verificar declaração duplicada - OK;
    def declaracaoVariavel(self, variavel: NoDeclaracaoVariavel, escopo: list[str]):
        if self.tabelaSimbolos.getSimbolo(variavel.id, escopo) is None:
            variavel.escopo = escopo
            variavel.tipo.escopo = escopo
            variavel.tipo.valor = variavel.id
            self.tabelaSimbolos.addSimbolo(variavel.id, variavel, escopo)
        else:
            self.listaErros.append(f"linha: {variavel.linha}, variavel '{variavel.id}' ja declarada.")

    def verificarTipos(self, tipoA: NoTipo, tipoB: NoTipo, escopo: list[str]):
        eIgual = False
        tipoAfim = None
        tipoBfim = None
        if isinstance(tipoA, NoTipoId):
            declaracao = self.tabelaSimbolos.getSimbolo(tipoA.valor, escopo)
            if declaracao is None:
                self.listaErros.append(f"linha: {tipoA.linha}, variavel '{tipoA.valor}' não declarada.")
            else:
                tipoAfim = declaracao.tipo
                tipoA.escopo = declaracao.escopo
                tipoA.tipo = tipoAfim
        else:
            tipoAfim = tipoA

        if isinstance(tipoB, NoTipoId):
            declaracao = self.tabelaSimbolos.getSimbolo(tipoB.valor, escopo)
            if declaracao is None:
                self.listaErros.append(f"linha: {tipoB.linha}, variavel '{tipoB.valor}' não declarada.")
            else:
                tipoBfim = declaracao.tipo
                tipoB.escopo = declaracao.escopo
                tipoB.tipo = tipoBfim
        else:
            tipoBfim = tipoB

        if type(tipoAfim) == type(tipoBfim):
                eIgual = True

        return eIgual

    # 1 - Analizar escopo - OK; 2 - Verificar tipos; 3 - Verificar variavel não declarada - OK;
    def atribuicao(self, varAtribuicao: NoAtribuicao, escopo):
        # 1 - Analizar escopo
        declaracao = self.tabelaSimbolos.getSimbolo(varAtribuicao.id, escopo)
        # 3 - Verificar variavel não declarada
        if declaracao is None:

            self.listaErros.append(f"linha: {varAtribuicao.linha}, variavel '{varAtribuicao.id}' não declarada.")
            return
        declaracao.tipo.escopo = declaracao.escopo
        varAtribuicao.tipo = declaracao.tipo

        # 2 - Verificar tipos
        if isinstance(varAtribuicao.valor, NoExpressaoAritimetica):
            eIgual = self.expressaoAritimetica(varAtribuicao.valor, escopo)
            print(f"Expressao '{varAtribuicao.valor}' na linha {varAtribuicao.linha} esta correta: {eIgual}")
        elif isinstance(varAtribuicao.valor, NoExpressaoBool):
            eIgual = self.expressaoBooleana(varAtribuicao.valor, escopo)
            print(f"Expressao '{varAtribuicao.valor}' na linha {varAtribuicao.linha} esta correta: {eIgual}")
        elif isinstance(varAtribuicao.valor, NoChamadaFuncProc):
            self.chamadaFuncProc(varAtribuicao.valor)
            eIgual = self.verificarTipos(varAtribuicao.tipo, varAtribuicao.valor.retorno.tipo, escopo)
            print(f"A atribuição '{varAtribuicao.valor}' na linha {varAtribuicao.linha} esta correta: {eIgual}")

        else:
            eIgual = self.verificarTipos(varAtribuicao.tipo, varAtribuicao.valor, escopo)
            print(f"A atribuição '{varAtribuicao.valor}' na linha {varAtribuicao.linha} esta correta: {eIgual}")

        if not eIgual:
            self.listaErros.append(f"linha: {varAtribuicao.linha}, variavel '{varAtribuicao.id}' incompativel com "
                                   f"'{varAtribuicao.valor}'")

    # 1 - Analizar escopo - OK; 2 - Verificar tipos; 4 - Verificar declaração duplicada - OK;
    def declaracaoFuncao(self, funcao: NoDeclaracaoFuncao):
        # 4 - Verificar declaração duplicada
        escopo = ['']
        assinatura = f"{funcao.__str__()}"
        if self.tabelaSimbolos.getSimbolo(funcao.id, escopo) is None:
            self.tabelaSimbolos.addSimbolo(assinatura, funcao, escopo)
            escopo.append(assinatura)
            for parametro in funcao.parametros:
                self.declaracaoVariavel(parametro, escopo)

        else:
            self.listaErros.append(f"linha: {funcao.linha}, função ou procedimento com id '{assinatura}' ja declarado.")

    def declaracaoProcedimento(self, proc: NoDeclaracaoProcedimento):
        # 4 - Verificar declaração duplicada
        escopo = ['']
        assinatura = f"{proc.__str__()}"
        if self.tabelaSimbolos.getSimbolo(proc.id, escopo) is None:

            self.tabelaSimbolos.addSimbolo(assinatura, proc, escopo)
            escopo.append(assinatura)
            for parametro in proc.parametros:
                self.declaracaoVariavel(parametro, escopo)
        else:
            self.listaErros.append(
                f"linha: {proc.linha}, função ou procedimento com assinatura '{assinatura}' ja declarado.")

    def chamadaFuncProc(self, funcao: NoChamadaFuncProc) -> NoTipo:
        # 4 - Verificar se foi declarada a função ou procedimento
        assinatura = f"{funcao.__str__()}"
        declaracaoFunc = self.tabelaSimbolos.getSimbolo(assinatura, [''])

        if declaracaoFunc is None:
            self.listaErros.append(
                f"linha: {funcao.linha}, função ou procedimento com id '{assinatura}' não foi declarado.")
        declaracaoVarRet = self.tabelaSimbolos.getSimbolo(declaracaoFunc.retorno.valor, declaracaoFunc.retorno.escopo)
        funcao.retorno = declaracaoVarRet
        return funcao.retorno

    def imprimir(self, saida: NoImprimir, escopo):
        saidaValida = False
        # 2 - Verificar tipos
        if isinstance(saida.tipo, NoTipoBool) or isinstance(saida.tipo, NoTipoInt):
            saidaValida = True
        elif isinstance(saida.tipo, NoExpressaoAritimetica):
            saidaValida = self.expressaoAritimetica(saida.tipo, escopo)
        elif isinstance(saida.tipo, NoExpressaoBool):
            saidaValida = self.expressaoBooleana(saida.tipo, escopo)
        elif isinstance(saida.tipo, NoChamadaFuncProc):
            saidaValida = self.chamadaFuncProc(saida.tipo)
        elif isinstance(saida.tipo, NoTipoId):
            declaracao = self.tabelaSimbolos.getSimbolo(saida.tipo.valor, escopo)
            # 3 - Verificar variavel não declarada
            if declaracao is None:
                self.listaErros.append(f"linha: {saida.linha}, variavel '{saida.tipo.valor}' não declarada.")
                return
            saida.tipo = declaracao.tipo
        else:
            self.listaErros.append(f"linha: {saida.linha}, impossivel imprimir '{saida.tipo.__str__()}'")

        if saidaValida:
            print(f"linha: {saida.linha}, imprimir '{saida.tipo.__str__()}'")

    def enquanto(self, enquanto: NoEnquanto, filhos, escopo: list[str]):
        if isinstance(enquanto.condicao, NoExpressaoBool):
            eIgual = self.expressaoBooleana(enquanto.condicao, escopo)
            print(
                f"Expressao '{enquanto.condicao}' na condição do loop 'ENQUANTO' na linha {enquanto.linha} esta correta: {eIgual}")
        if isinstance(filhos, list) and (len(filhos) < 1):
            self.listaErros.append(f"linha: {enquanto.linha}, deve conter ao menos uma instrução no corpo.")

    def se(self, se: NoSe, filhos, escopo: list[str]):
        if isinstance(se.condicao, NoExpressaoBool):
            eIgual = self.expressaoBooleana(se.condicao, escopo)
            print(
                f"Expressao '{se.condicao}' na condição da condicional 'SE' na linha {se.linha} esta correta: {eIgual}")
        if isinstance(filhos, list) and (len(filhos) < 1):
            self.listaErros.append(f"linha: {se.linha}, deve conter ao menos uma instrução no corpo.")

    def seNao(self, seN: NoSeNao, filhos):
        if isinstance(filhos, list) and (len(filhos) < 1):
            self.listaErros.append(f"linha: {seN.linha}, deve conter ao menos uma instrução no corpo.")

    def expressaoAritimetica(self, expressao: NoExpressaoAritimetica, escopo: list[str]) -> bool:
        if not (isinstance(expressao.termoA, NoTipoBool) and isinstance(expressao.termoB, NoTipoBool)) and \
                self.verificarTipos(expressao.termoA, expressao.termoB, escopo):
            return True
        return False

    def expressaoBooleana(self, expressao: NoExpressaoBool, escopo: list[str]) -> bool:
        if self.verificarTipos(expressao.termoA, expressao.termoB, escopo):
            return True
        return False
