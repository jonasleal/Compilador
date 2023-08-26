import re
import palavraReservada

class Lexica:

    def buscarTokens(input_text):
        tokens = []
        posicao = 0

        while posicao < len(input_text):
            encontrado = None
            for token_type, padrao in palavraReservada.TOKEN_TYPE:
                regex = re.compile(padrao)
                encontrado = regex.match(input_text, posicao)
                if encontrado:
                    value = encontrado.group(0)
                    if token_type != "ESPACO_BRANCO":
                        tokens.append((token_type, value))
                    break
            if not encontrado:
                raise ValueError(f"Invalid character: {input_text[posicao]}")
            posicao = encontrado.end()

        tokens.append(("EOF", ""))
        return tokens

