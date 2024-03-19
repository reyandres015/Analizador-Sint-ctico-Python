# Definir los tokens y palabras reservadas
tokens = {

    'tkn_ejecuta': '->',

    'tkn_potencia': '**',

    'tkn_mayor_igual': '>=',

    'tkn_menor_igual': '<=',

    'tkn_igual': '==',

    'tkn_distinto': '!=',

    'tkn_and': 'and',

    'tkn_or': 'or',

    'tkn_not': 'not',

    'tkn_mas_asig': '+=',

    'tkn_menos_asig': '-=',

    'tkn_mult_asig': '*=',

    'tkn_div_asig': '/=',

    'tkn_mod_asig': '%=',

    'tkn_menor_menor': '<<',

    'tkn_mayor_mayor': '>>',

    'tkn_mas_mas': '++',

    'tkn_menos_menos': '--',

    'tkn_punto_y_coma': ';',

    'tkn_coma': ',',

    'tkn_par_izq': '(',

    'tkn_par_der': ')',

    'tkn_corchete_izq': '[',

    'tkn_corchete_der': ']',

    'tkn_llave_izq': '{',

    'tkn_llave_der': '}',

    'tkn_dos_puntos': ':',

    'tkn_punto': '.',

    'tkn_asig': '=',

    'tkn_div': '/',

    'tkn_suma': '+',

    'tkn_resta': '-',

    'tkn_mult': '*',

    'tkn_modulo': '%',

    'tkn_mayor': '>',

    'tkn_menor': '<',

    'tkn_arroba': '@',

    'tkn_comentario': '#',

    'tkn_dolar': '$',

    'tkn_ampersand': '&',

    'tkn_interrogacion': '?',

    'tkn_tilde': '~'

}
# Palabras reservadas en minúsculas

palabras_reservadas = {

    'object', 'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'bool', 'break',

    'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from','global',

    'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'print', 'raise','return',

    'try', 'self', 'while', 'with', 'yield', '_init_', 'str'
}

# Tipos de datos
tipos_datos = {
    'int': 'int',
    'float': 'float',
    'str': 'str',
    'bool': 'bool'
}

# Tabla de símbolos
tabla_simbolos = {}

# Contador de filas
fila = 1

def contiene_solo_letras(cadena):
    for char in cadena:
        if char.isalpha() or char.isalnum():
            return True
        else:
            return False

def analizar_lexico(codigo):
    fila = 0
    columna = 0
    palabra = ''
    comentario = False
    dentro_cadena = False
    ultima_columna = 0
    lineas = codigo.split('\n')

    for linea in lineas:
        fila += 1
        columna = 0
        comentario = False

        while columna < len(linea):
            char = linea[columna]
            if char == '\t':
                columna += 4
            else:
                columna += 1

            if comentario:
                continue

            if dentro_cadena:
                palabra += char

                if char == '"' or char =="'":
                    print(f"<tkn_cadena, {palabra}, {fila}, {(columna-len(palabra))+1}>")
                    palabra = ''
                    dentro_cadena = False
                continue

            if char == '#':
                comentario = True
                continue

            if char.isspace() or char in tokens.values():
                if palabra:
                    if palabra in palabras_reservadas:
                        print(f"<{palabra}, {fila}, {columna - len(palabra)}>")
                        # if palabra not in ['False', 'True', 'None']:

                    elif palabra in tipos_datos:
                        print(f"<tipo_dato, {palabra}, {fila}, {columna - len(palabra)}>")
                    else:
                        if contiene_solo_letras(palabra):
                            print(f"<id, {palabra}, {fila}, {columna - len(palabra)}>")
                        else:
                            print(f">>>Error lexico(Fila:{fila},Columna:{columna - len(palabra)})")
                    palabra = ''

                if char in tokens.values():
                    for token, value in tokens.items():
                        if columna >= len(value) and linea[columna-len(value):columna] == value:
                            print(f"<{token}, {fila}, {columna-len(value)+1}>")
                            palabra = ''
                            break


            elif char == '"' or char == "'":
                palabra += char
                dentro_cadena = True

            else:
                palabra += char

            if palabra in ['False', 'True', 'None']:
                ultima_columna = columna

        if palabra:
            if palabra in palabras_reservadas:
                print(f"<{palabra}, {fila}, {ultima_columna-len(palabra)}>")

            elif palabra in tipos_datos:
                print(f"<tipo_dato, {palabra}, {fila}, {ultima_columna}>")

            else:
                print(f"<id, {palabra}, {fila}, {ultima_columna}>")

# Cargar el código desde un archivo
with open('codigo.py', 'r', encoding='utf-8') as file:
    input_text = file.read()

# Realizar el análisis léxico
analizar_lexico(input_text)
