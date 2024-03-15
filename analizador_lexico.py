token = {
    'tk_num': '0123456789',
    'tk_letra': 'abcdefghijklmnopqrstuvwxyz',
}

simbolos = {'+': 'concatenacion_cadenas', '-': 'resta', '*': 'repeticion_cadenas', '/': 'division', '%': 'modulo', '**': 'exponenciacion', '==': 'igualdad', '!=': 'desigualdad', '>': 'mayor_que', '<': 'menor_que', '>=': 'mayor_igual_que', '<=': 'menor_igual_que', '->': 'ejecuta', 'and': 'y_logico', 'or': 'o_logico', 'not': 'no_logico', '=': 'asignacion', '+=': 'incremento', '-=': 'decremento', '*=': 'multiplicacion_asignacion', '/=': 'division_asignacion', '%=': 'modulo_asignacion', '**=': 'exponenciacion_asignacion', '(': 'parentesis_abierto', ')': 'parentesis_cerrado', '{': 'llave_abierta', '}': 'llave_cerrada', '[': 'corchete_abierto', ']': 'corchete_cerrado', ',': 'coma', '.': 'punto', ':': 'dos_puntos', ';': 'punto_y_coma', '@': 'aroba_invertida', '#': 'comentario', '$': 'dolar', '&': 'ampersand', '?': 'interrogacion', '!': 'exclamacion', '~': 'tilde', 'is': 'is', 'is not': 'is_not', 'in': 'in', 'not in': 'not_in', "'": 'comilla_simple', '"': 'comilla_doble', '`': 'acento_grave', '\\': 'barra_invertida'}

palabras_reservadas = {'False': 'False', 'None': 'None', 'True': 'True', 'and': 'and', 'as': 'as', 'assert': 'assert', 'async': 'async', 'await': 'await', 'bool':'bool', 'break': 'break', 'class': 'class', 'continue': 'continue', 'def': 'def', 'del': 'del', 'elif': 'elif', 'else': 'else', 'except': 'except', 'finally': 'finally', 'for': 'for', 'from': 'from', 'global': 'global', 'if': 'if', 'import': 'import', 'in': 'in', 'is': 'is', 'lambda': 'lambda', 'nonlocal': 'nonlocal', 'not': 'not', 'or': 'or', 'pass': 'pass', 'print':'print', 'raise': 'raise', 'str':'str', '__init__':'__init__', 'return': 'return', 'try': 'try', 'self':'self', 'while': 'while', 'with': 'with', 'yield': 'yield'}

def buscar_palabras_en_diccionarios(cadena, diccionario1, diccionario2, token):
    fila = 1
    columna = 0
    recorrido = 0
    longitud_cadena = len(cadena)
    palabra = ''

    def es_simbolo(palabra):
        return simbolos.get(palabra)

    def es_palabra_reservada(palabra):
        return palabras_reservadas.get(palabra)

    def es_token(palabra):
        return palabra in token.values()
    
    for char in range(len(cadena)):
        recorrido += 1
        caracter_actual = cadena[char]

        if caracter_actual == ' ' or caracter_actual == '\n' or caracter_actual in simbolos.keys():
            if palabra:
                if es_simbolo(palabra):
                    print(f"< {es_simbolo(palabra)}, {fila}, {columna - len(palabra) + 1}>")
                elif es_palabra_reservada(palabra):
                    print(f"< {es_palabra_reservada(palabra)}, {fila}, {columna - len(palabra) + 1}>")
                elif es_token(palabra):
                    print(f"< {palabra}, {fila}, {columna - len(palabra) + 1}>")
                elif palabra not in palabras_reservadas and palabra not in token.values() and palabra not in simbolos.keys():
                    print(f"<id {palabra}, {fila}, {columna - len(palabra) + 1}>")
                else:
                    for simbolo in simbolos.keys():
                        if palabra.startswith(simbolo) or palabra.endswith(simbolo):
                            print(f"<{simbolo},{fila}, {columna - len(palabra) + 1}>")
            palabra = ''

            if caracter_actual == ' ' or caracter_actual == '\n':
                columna += 1
            else:
                print(f"<{caracter_actual}, {fila}, {columna + 1}>")
                columna += 1

        else:
            palabra += caracter_actual
            columna += 1

        if caracter_actual == '\n':
            fila += 1
            columna = 0

# Abre el archivo en modo lectura (r)
with open('prueba.py', 'r') as file:
    # Lee todas las líneas del archivo
    input = file.read()

buscar_palabras_en_diccionarios(input, simbolos, palabras_reservadas, token)
