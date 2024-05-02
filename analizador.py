# Definir los tokens y palabras reservadas
tokens = {
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
    'tkn_exclamacion': '!'
}

# Palabras reservadas en minúsculas
palabras_reservadas = {
    'range', 'object', 'False', 'None', 'True', 'and', 'or','not', 'as', 'assert', 'async', 'await', 'break',
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global',
    'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'pass', 'raise', 'return',
    'try', 'self', 'while', 'with', 'yield', 'init','->','>=','<=','==','!=','+=','-=', '*=', '/=','//','%=', '<<', '>>','=',
    '/','+','-','*','%','>','<','@','&','?','~','_','!'
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
    if cadena in tokens.values():
        return False
    if cadena in palabras_reservadas:
        return True
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
        blanco = 0
        comentario = False
        palabra = ''
        tokensLinea = []

        while columna < len(linea):
            char = linea[columna]
            columna += 1

            if(blanco == 4):
                tokensLinea.append(["tkn_tab",fila,columna - 4])
                blanco = 0

            if comentario:  # Estado (comentario)
                continue

            if dentro_cadena:
                blanco = 0
                palabra += char

                if char == '"' or char == "'":
                    tokensLinea.append(["tkn_cadena",fila,(columna-len(palabra))+1])
                    print(f"<tkn_cadena, {palabra}, {fila}, {(columna-len(palabra))+1}>")
                    palabra = ''
                    dentro_cadena = False
                continue

            if char == '#':
                blanco = 0
                comentario = True
                continue

            # Verificar si el carácter es un símbolo definido
            if char not in tokens.values() and char not in palabras_reservadas and not char.isalnum() and char != '_' and char!=' ' and char!='"':
                print(f">>>Error léxico: Símbolo no definido '{char}' en la fila {fila}, columna {columna}")
                return

            if char.isdigit():
                blanco = 0
                inicio_numero = columna - 1
                while columna < len(linea) and (linea[columna].isdigit()):
                    columna += 1
                    
                tokensLinea.append(["tk_entero",fila,inicio_numero + 1])
                print(f"<tk_entero, {linea[inicio_numero:columna]}, {fila}, {inicio_numero + 1}>")
                palabra = ''
                continue

            if es_identificador(char):
                blanco = 0
                inicio_numero = columna - 1
                while columna < len(linea) and (es_identificador(linea[columna])): #Identificar longitud cadena
                    columna += 1
                if linea[inicio_numero:columna] in palabras_reservadas: #palabra reservada
                    tokensLinea.append([linea[inicio_numero:columna],fila,inicio_numero + 1])
                    print(f"<{linea[inicio_numero:columna]}, {fila}, {inicio_numero + 1}>")

                elif linea[inicio_numero:columna] in tipos_datos: 
                    tokensLinea.append(["tipo_dato",fila,inicio_numero + 1])
                    print(f"<tipo_dato, {linea[inicio_numero:columna]}, {fila}, {inicio_numero + 1}>")
                else:
                    tokensLinea.append(["id",fila,inicio_numero + 1])
                    print(f"<id, {linea[inicio_numero:columna]}, {fila}, {inicio_numero + 1}>")
                palabra = ''
                continue

            if char.isspace() or char in tokens.values():
                #Condicional :(
                if palabra:
                    blanco = 0
                    if palabra in palabras_reservadas:
                        tokensLinea.append([palabra,fila,columna - len(palabra)])
                        print(f"<{palabra}, {fila}, {columna - len(palabra)}>")

                    elif palabra in tipos_datos:
                        tokensLinea.append(["tipo_dato",fila,columna - len(palabra)])
                        print(f"<tipo_dato, {palabra}, {fila}, {columna - len(palabra)}>")
                        
                    elif es_identificador(palabra):
                        tokensLinea.append(["id",fila,columna - len(palabra)])
                        print(f"<id, {palabra}, {fila}, {columna - len(palabra)}>")

                    else:
                        try:
                            # Intentamos convertir la palabra en un número entero
                            numero_entero = int(palabra)
                            tokensLinea.append(["numero_entero",fila,columna - len(palabra)])
                            print(f"<numero_entero, {palabra}, {fila}, {columna - len(palabra)}>")
                        except ValueError:
                            print(f">>>Error léxico(Fila:{fila},Columna:{columna - len(palabra)})")
                            return
                    palabra = ''
                else:
                    blanco += 1

                if char in tokens.values():
                    for token, value in tokens.items():
                        if columna >= len(value) and linea[columna-len(value):columna] == value:
                            tokensLinea.append([token,fila,columna-len(value)+1])
                            
                            print(f"<{token}, {fila}, {columna-len(value)+1}>")
                            palabra = ''
                            break

            elif char == '"' or char == "'":
                palabra += char
                dentro_cadena = True

            else:
                palabra += char
        tokensIdentificados.append(tokensLinea)

# Analizador sintactico
def esFuncion(linea):
    structure = ['def','id','tkn_par_izq','id','tkn_coma','tkn_par_der', 'tkn_dos_puntos']
    token = linea[0]
    tkn_name = token[0]
    if(tkn_name == structure[0]): #def
        token = linea[1]
        tkn_name = token[0]
        if(tkn_name == structure[1]): #id
            token = linea[2]
            tkn_name = token[0]
            if(tkn_name == structure[2]): #(
                n = 3
                while linea[n][0] != structure[5]: #recorrer parametros hasta encontrar ')'
                    if linea[n][0] == structure[4] and linea[n+1][0] == structure[3]: #debe ser un id seguido de una coma
                        token = linea[n]
                        tkn_name = token[0]
                    elif  linea[n+1][0] == structure[5]: #el siguiente token ya es ')'
                        n += 1
                        continue                        
                    elif linea[n][0] == structure[3] and linea[n+1][0] == structure[4]: #debe ser una coma seguida de un id
                        token = linea[n]
                        tkn_name = token[0]
                    else:
                        print(f'<{linea[n][1]},{linea[n][2]}>Error sintactico: se encontro "{linea[n+1][0]}" se esperaba {"," if linea[n][0] == structure[3] else "parameter name or )"}')
                        return False
                    n += 1
                # n = 6 posicion de ')'
                if ((n - 3) % 2) != 0: #impar
                    token = linea[n + 1]
                    tkn_name = token[0]
                    if tkn_name == structure[6]: #:
                        return True
    return False

#Condicional IF-----------------------------------------------------------------------------

def operacionesCondiciones(linea):
    condicionalOperator = ['in','and','or','is','>=','<=','==','!=','tkn_and','tkn_or','tkn_not']
    factors = ['id','tk_entero']
    operators = ['tkn_div','tkn_suma','tkn_resta','tkn_mult','tkn_modulo']
    expression = [factors,operators,factors]
    
    structureOperacionesCondiciones = ['if',expression,condicionalOperator,expression,'tkn_dos_puntos'] #plantilla
    structureCondiciones = ['if',factors,condicionalOperator,factors,'tkn_dos_puntos'] #plantilla
    
    
    n=0
    if linea[n][0] == structureOperacionesCondiciones[0]: #if
        n+=1
        if linea[n][0] in structureOperacionesCondiciones[1][0]: # ES ID o ENTERO
            n+=1
            if linea[n][0] in structureOperacionesCondiciones[1][1]: # ES OPERADOR
                n+=1
                if linea[n][0] in structureOperacionesCondiciones[1][2]: # ES ID o ENTERO
                    n+=1
                    if linea[n][0] in structureOperacionesCondiciones[2]: # es condicional operator
                        n+=1
                        if linea[n][0] in structureOperacionesCondiciones[1][0]: # ES ID o ENTERO
                            n+=1
                            if linea[n][0] in structureOperacionesCondiciones[1][1]: # ES OPERADOR
                                n+=1
                                if linea[n][0] in structureOperacionesCondiciones[1][2]: # ES ID o ENTERO
                                    n+=1
                                    if linea[n][0] == structureOperacionesCondiciones[4]: # ES ':'
                                        #si es el final de la linea
                                        if n == len(linea) - 1:
                                            return True
                            else:
                                if linea[n][0] == structureOperacionesCondiciones[4]: # ES ':'
                                    if n == len(linea) - 1:
                                        return True
            else: #structureCondiciones
                if linea[n][0] in structureOperacionesCondiciones[2]:# es condicional operator
                    n+=1
                    if linea[n][0] in structureOperacionesCondiciones[1][0]: # ES ID o Entero
                        n+=1
                        if linea[n][0] == structureOperacionesCondiciones[4]: # ES ':'
                            if n == len(linea) - 1:
                                return True
                else: # condicional con solo una variable.
                    
                    if linea[n][0] == structureOperacionesCondiciones[4]: # ES ':'
                        if n == len(linea) - 1:
                            return True
                    
    print(f'<{linea[n][1]},{linea[n][2]}>Error sintactico: se encontro un simbolo inesperado: "{linea[n][0]}"')
    return False

def basicStructure(linea):
    palabras_reservadas_aceptadas = ['True','False','None']
    
    basicStructure = ['if',palabras_reservadas_aceptadas,'tkn_dos_puntos']
    
    n = 0
    if linea[n][0] == basicStructure[0]: #if
        n+=1
        if linea[n][0] in basicStructure[1]: # palabras reservas
            n+=1
            if linea[n][0] == basicStructure[2]:
                if n == len(linea) - 1:
                    return True
    print(f'<{linea[n][1]},{linea[n][2]}>Error sintactico: se encontro un simbolo inesperado: "{linea[n][0]}"')
    return False

def negationStructure(linea):
    negationStructure = ['if','not','id','tkn_dos_puntos']
    n=0
    if linea[n][0] == negationStructure[0]: #if
        n+=1
        if linea[n][0] == negationStructure[1]: #not
            n+=1
            if linea[n][0] == negationStructure[2]: #id
                n+=1
                if linea[n][0] == negationStructure[3]:
                    if n == len(linea) - 1:
                        return True
    print(f'<{linea[n][1]},{linea[n][2]}>Error sintactico: se encontro un simbolo inesperado: "{linea[n][0]}"')
    return False

condicionales ={
    'id': operacionesCondiciones,
    'tk_entero': operacionesCondiciones,
    'True': basicStructure,
    'False': basicStructure,
    'None': basicStructure,
    'not': negationStructure
    
}

def esCondicional(linea):    
    if condicionales[linea[1][0]]: 
        func = condicionales[linea[1][0]]
        return func(linea) # ejecutar la función que corresponda
    return False

def esId(linea):
    n=0
    if linea[n][0] == 'id':
        n+=1
        if linea[n][0] == '=': #Asignación
            n+=1
            if linea[n][0] == 'id' or linea[n][0] == 'tk_entero' or linea[n][0] == 'tkn_cadena':
                if n == len(linea) - 1:
                    return True
        else:
            if linea[n][0] == 'tkn_par_izq':
                n+=1
                while linea[n][0] != 'tkn_par_der':
                    if linea[n][0] == 'id' or linea[n][0] == 'tk_entero' or linea[n][0] == 'tkn_cadena':
                        n+=1
                        if linea[n][0] == 'tkn_coma':
                            n+=1
                        elif linea[n][0] == 'tkn_par_der':
                            if n == len(linea) - 1:
                                return True
                        else:
                            print(f'<{linea[n][1]},{linea[n][2]}>Error sintactico: se encontro un simbolo inesperado: "{linea[n][0]}"')
                            return False
                    else:
                        print(f'<{linea[n][1]},{linea[n][2]}>Error sintactico: se encontro un simbolo inesperado: "{linea[n][0]}"')
                        return False
        if n == len(linea) - 1:
            return True
    print(f'<{linea[n+1][1]},{linea[n+1][2]}>Error sintactico: se encontro un simbolo inesperado: "{linea[n+1][0]}"')
    return False

grammar ={
    'def': esFuncion,
    'if' : esCondicional,
    'id' : esId
    'import': esImport,
}

def identificar_estructura(linea):
    if grammar[linea[0][0]]: #comprobar si el primer tkn es una estructura definina en grammar
        func = grammar[linea[0][0]]
        return func(linea) # ejecutar la función que corresponda
        

def analizadorSintactico():
    for filas in tokensIdentificados:
        filas = [token for token in filas if token[0] != 'tkn_tab'] #eliminar tkn_tab!!!!!!!!
        print(filas)
        if not identificar_estructura(filas):
            print("Error en el analisis sintactico.")
            return
    print("El analisis sintactico ha finalizado exitosamente.")


# Cargar el código desde un archivo
with open('codigo.py', 'r', encoding='utf-8') as file:
    input_text = file.read()

# Realizar el análisis léxico
print('Análisis léxico 🚩')
analizar_lexico(input_text)
print('Análisis léxico completado.\n')

print('Análisis Sintactico 🚩')
# print(tokensIdentificados)
analizadorSintactico()