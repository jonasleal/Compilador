# Definição dos tokens
TOKENS = {
    'bool': 'TIPO',
    'true': 'TIPO_BOOL',
    'false': 'TIPO_BOOL',
    'int': 'TIPO',
    'var': 'VAR',
    'func': 'DECLARACAO_FUNCAO',
    'proc': "DECLARACAO_PROCEDIMENTO",
    'se': 'SE',
    'senao': 'SE_NAO',
    'enquanto': 'ENQUANTO',
    'imprimir': 'IMPRIMIR',
    'parar': 'PARAR',
    'continue': 'CONTINUE',
    'retorno': 'RETORNO',
    'id': 'ID'}

DELIMITADORES = {
    ';': 'PONTO_VIRGULA',
    '(': 'PARENT_ESQ',
    ')': 'PARENT_DIR',
    '{': 'CHAVE_ESQ',
    '}': 'CHAVE_DIR',
    ',': 'VIRGULA',
    '+': 'MAIS',
    '-': 'MENOS',
    '*': 'MULTIPLICAR',
    '/': 'DIVIDIR'

}

LOGICO = {
    '==': 'IGUAL',
    '!=': 'DIFERENTE',
    '>': 'MAIOR_QUE',
    '>=': 'MAIOR_IGUAL',
    '<': 'MENOR_QUE',
    '<=': 'MENOR_IGUAL',
    '!': 'NEGACAO'
}

ATRIBUICAO = {
    '=': 'ATRIBUICAO'
}