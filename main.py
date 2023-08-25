
"""

nomeArq =  "teste.txt" #input('Digite o nome do arquivo que será compilado \n')
analiseLexica = lexica.Lexica(nomeArq)
analiseLexica.verificar()
"""
import re

# Token types
TOKEN_TYPE = [
    ("TIPO", r"int|bool"),
    ("NUM", r"[0-9]+"),
    ("TIPO_BOOL", r"true|false"),
    ("TIPO_INT", r"0|[1-9][0-9]*"),
    ("OP_ARITIMETICO", r"\+|\-|\*|\/"),
    ("OP_BOOLEANO", r"==|!=|>|>=|<|<="),
    ("PONTO_VIRGULA", r";"),
    ("VIRGULA", r","),
    ("PARENT_ESQ", r"\("),
    ("PARENT_DIR", r"\)"),
    ("CHAVE_ESQ", r"\{"),
    ("CHAVE_DIR", r"\}"),
    ("ATRIBUICAO", r"="),
    ("ESPACO_BRANCO", r"\s"),
    ("RETORNO", r"retorno"),
    ("SE", r"se"),
    ("SENAO", r"senao"),
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

def tokenize(input_text):
    tokens = []
    position = 0

    while position < len(input_text):
        match = None
        for token_type, pattern in TOKEN_TYPE:
            regex = re.compile(pattern)
            match = regex.match(input_text, position)
            if match:
                value = match.group(0)
                if token_type != "ESPACO_BRANCO":
                    tokens.append((token_type, value))
                break
        if not match:
            raise ValueError(f"Invalid character: {input_text[position]}")
        position = match.end()

    tokens.append(("EOF", ""))
    return tokens


with open("teste.txt", 'r') as arquivo:
    input_text = arquivo.read()
#input_text = "func "
tokens = tokenize(input_text)
for token_type, value in tokens:
    print(f"Token: {token_type}\tValue: {value}")
