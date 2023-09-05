# Palavras reservadas que compõe a linguagem

DEL_ESCOPO = " | "  # Delimitador de escopo

TOKEN_TIPO = [
    ("INT", r"int"),
    ("BOOL", r"bool"),

]

VALOR_NUMERICO = [
    ("TIPO_INT", r"[0-9]+"),
]

VALOR_BOOL = [
    ("TIPO_BOOL", r"true|false"),
]

TOKEN_OPERADORES = [
    ("OP_BOOLEANO", r"==|!=|>|>=|<|<="),
    ("OP_ARITIMETICO", r"\+|\-|\*|\/"),
]

TOKEN_DELIMITADOR = [
    ("PONTO_VIRGULA", r";"),
    ("VIRGULA", r","),
    ("PARENT_ESQ", r"\("),
    ("PARENT_DIR", r"\)"),
    ("CHAVE_ESQ", r"\{"),
    ("CHAVE_DIR", r"\}"),
    ("ATRIBUICAO", r"="),

]

TOKEN_IGNORADOS = [
    ("QUEBRA_LINHA", r"\n"),
    ("ESPACO_BRANCO", r"\s"),

]

TOKEN_PALAVRA = [

    ("RETORNO", r"retorno"),
    ("SENAO", r"senao"),
    ("SE", r"se"),
    ("ENQUANTO", r"enquanto"),
    ("IMPRIMIR", r"imprimir"),
    ("PARAR", r"parar"),
    ("CONTINUE", r"continue"),
    ("DECLARACAO_FUNCAO", r"func"),
    ("DECLARACAO_PROCEDIMENTO", r"proc"),
    ("DECLARACAO_VARIAVEL", r"var"),
    ("EOF", r"$"),
    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
]
VALOR_LITERAL = VALOR_BOOL + VALOR_NUMERICO
TOKENS_GRAMATICA = TOKEN_IGNORADOS + TOKEN_TIPO + VALOR_LITERAL + TOKEN_OPERADORES + TOKEN_DELIMITADOR + TOKEN_PALAVRA

def getOperadores():
    operadores = []
    for token_type, valor in TOKEN_OPERADORES:
        operadores.append(token_type)
    return operadores