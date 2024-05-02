# Definir los tokens y palabras reservadas
tokens = {
    'tkn_ejecuta': '->',
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
    'tkn_div_entera': '//',
    'tkn_mod_asig': '%=',
    'tkn_menor_menor': '<<',
    'tkn_mayor_mayor': '>>',
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
    'tkn_ampersand': '&',
    'tkn_interrogacion': '?',
    'tkn_tilde': '~',
    'tkn_barra_piso': '_',
    'tkn_exclamacion': '!'
}

# Palabras reservadas en minúsculas
palabras_reservadas = {
    'range', 'object', 'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global',
    'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'print', 'raise', 'return',
    'try', 'self', 'while', 'with', 'yield', 'init'
}

# Tipos de datos
tipos_datos = {
    'int': 'int',
    'float': 'float',
    'str': 'str',
    'bool': 'bool'
}

def es_identificador(cadena):
    if not cadena:
        return False  # La cadena no puede estar vacía
    if cadena[0].isdigit():
        return False  # El identificador no puede comenzar con un dígito
    for char in cadena:
        if not char.isalnum() and char != '_':
            return False  # Los caracteres permitidos son letras, números y guiones bajos
    return True

tokensIdentificados = []

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
        palabra = ''

        while columna < len(linea):
            tokensLinea = []
            char = linea[columna]
            if char == '\t':
                tokensIdentificados.append(["tkn_tab",fila,columna+1])
                columna += 4
            else:
                columna += 1

            if comentario:  # Estado (comentario)
                continue

            if dentro_cadena:
                palabra += char

                if char == '"' or char == "'":
                    tokensIdentificados.append(["tkn_cadena",fila,(columna-len(palabra))+1])
                    print(
                        f"<tkn_cadena, {palabra}, {fila}, {(columna-len(palabra))+1}>")
                    palabra = ''
                    dentro_cadena = False
                continue

            if char == '#':
                comentario = True
                continue

            # Verificar si el carácter es un símbolo definido
            if char not in tokens.values() and char not in palabras_reservadas and not char.isalnum() and char != '_' and char!=' ' and char!='"':
                print(f">>>Error léxico: Símbolo no definido '{char}' en la fila {fila}, columna {columna}")
                return
                continue

            if char.isdigit():
                inicio_numero = columna - 1
                while columna < len(linea) and (linea[columna].isdigit()):
                    columna += 1
                    
                tokensIdentificados.append(["tk_entero",fila,inicio_numero + 1])
                print(f"<tk_entero, {linea[inicio_numero:columna]}, {fila}, {inicio_numero + 1}>")
                palabra = ''
                continue

            if es_identificador(char):
                inicio_numero = columna - 1
                while columna < len(linea) and (es_identificador(linea[columna])): #Identificar longitud cadena
                    columna += 1
                if linea[inicio_numero:columna] in palabras_reservadas: #palabra reservada
                    tokensIdentificados.append([linea[inicio_numero:columna],fila,inicio_numero + 1])
                
                    print(f"<{linea[inicio_numero:columna]}, {fila}, {inicio_numero + 1}>")

                elif linea[inicio_numero:columna] in tipos_datos: 
                    tokensIdentificados.append(["tipo_dato",fila,inicio_numero + 1])

                    print(
                        f"<tipo_dato, {linea[inicio_numero:columna]}, {fila}, {inicio_numero + 1}>")
                else:
                    tokensIdentificados.append(["id",fila,inicio_numero + 1])
                    print(f"<id, {linea[inicio_numero:columna]}, {fila}, {inicio_numero + 1}>")
                palabra = ''
                continue

            if char.isspace() or char in tokens.values():
                #Condicional :(
                if palabra:
                    if palabra in palabras_reservadas:
                        tokensIdentificados.append([palabra,fila,columna - len(palabra)])
                        
                        print(f"<{palabra}, {fila}, {columna - len(palabra)}>")

                    elif palabra in tipos_datos:
                        tokensIdentificados.append(["tipo_dato",fila,columna - len(palabra)])
                        print(
                            f"<tipo_dato, {palabra}, {fila}, {columna - len(palabra)}>")
                    elif es_identificador(palabra):
                        tokensIdentificados.append(["id",fila,columna - len(palabra)])
                        
                        print(
                            f"<id, {palabra}, {fila}, {columna - len(palabra)}>")
                    else:
                        try:
                            # Intentamos convertir la palabra en un número entero
                            numero_entero = int(palabra)
                            tokensIdentificados.append(["numero_entero",fila,columna - len(palabra)])
                            
                            print(f"<numero_entero, {palabra}, {fila}, {columna - len(palabra)}>")
                        except ValueError:
                            print(
                                f">>>Error léxico(Fila:{fila},Columna:{columna - len(palabra)})")
                            return
                    palabra = ''
                if char in tokens.values():
                    for token, value in tokens.items():
                        if columna >= len(value) and linea[columna-len(value):columna] == value:
                            tokensIdentificados.append([token,fila,columna-len(value)+1])
                            
                            print(f"<{token}, {fila}, {columna-len(value)+1}>")
                            palabra = ''
                            break

            elif char == '"' or char == "'":
                palabra += char
                dentro_cadena = True

            else:
                palabra += char

            if columna == len(linea):
                tokensIdentificados.append(["tkn_salto",fila,columna+1])
    print(tokensIdentificados)
    
# Analizador sintactico
def esFuncion(linea):
    print(linea)
grammar ={
    'def': esFuncion,
}

def identificar_estructura(token,linea):
    func = grammar[token]
    if grammar[token]:
        func(linea)
        

def analizadorSintactico():
    for token in tokensIdentificados:
        identificar_estructura(token[0],token[1])


# Cargar el código desde un archivo
with open('codigo.py', 'r', encoding='utf-8') as file:
    input_text = file.read()

# Realizar el análisis léxico
analizar_lexico(input_text)