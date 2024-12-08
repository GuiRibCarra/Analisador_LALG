import tkinter.filedialog
import tkinter.messagebox
from tkinter import *

#------------------------------------------ARRAYS ELEMENTOS-------------------------------------------------------------
alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_']
alfabeto_m = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
numeros=['0','1','2','3','4','5','6','7','8','9']
reservadas= ['program','procedure','var','int','float','boolean','read','write','true','false','begin','end','if','then','else','while','do','or','div','and','not']
simbolos = ['::=',':=',':','=','<','>','<=','>=',',','<>','+','-','*','[',']','{','}',';','.','_','(',')','/']
lexemas = []
identificadores = []
expressoes = []
i_lexemas = 0
token = ''
token2 = ''
#------------------------------------------------ FUNCOES -------------------------------------------------------------
def inicia_tab():
    tabela.insert(END,'ELEMENTO')
    tabela.itemconfig(END, {'bg': '#EE82EE'})
    tabela2.insert(END, 'TIPO')
    tabela2.itemconfig(END, {'bg': '#EE82EE'})
    tabela3.insert(END, 'LINHA')
    tabela3.itemconfig(END, {'bg': '#EE82EE'})
    sintatico.insert(END,'ERROS SINTATICOS')
    sintatico.itemconfig(END, {'bg': '#EE82EE'})
    semantico.insert(END, 'ERROS SEMANTICOS')
    semantico.itemconfig(END, {'bg': '#EE82EE'})

def ler_comentario(texto,posicao):
    i = posicao+1
    tamanho = len(texto) - 1
    palavra = ''
    if texto[i-1]  ==  '{':
        while texto[i] != '}':
            if i  ==  tamanho:
                return palavra,i,'NÃO_FECHOU_COMENTARIO'
            else:
                palavra = palavra + texto[i]
                i = i + 1
    else:
        i = i+1
        while texto[i] != '\n':
            if i  ==  tamanho:
                break
            else:
                palavra = palavra + texto[i]
                i = i + 1
    return palavra,i,'COMENTARIO'

def abrir_arq():
    bloco.delete('0.0',END)
    tabela.delete(0,END)
    tabela2.delete(0, END)
    tabela3.delete(0, END)
    sintatico.delete(0, END)
    semantico.delete(0, END)
    inicia_tab()
    arq = tkinter.filedialog.askopenfilename()

    if('.txt' in arq):
        arq_a = open(arq,'r')
        conteudo = arq_a.read()
        bloco.insert(END,conteudo)
    else:
        tkinter.messagebox.showerror(title="ERROR",message="Tipo de Arquivo selecinado não é .txt, selecione novamente")
        print('erro')

def salvar_arq():
    tabela.delete(0, END)
    tipo = [('.txt', '*.txt')]
    arq = tkinter.filedialog.asksaveasfile(mode='w',filetypes=tipo,defaultextension=".txt")
    arq.write(bloco.get('0.0',END))

def ler_texto(texto,posicao):
    i = posicao
    tamanho = len(texto)-1
    limite = 15
    palavra = ''
    while texto[i] in alfabeto or texto[i] in alfabeto_m or texto[i] in numeros:
        if i  ==  tamanho:
            break
        else:
            palavra = palavra + texto[i]
            i = i+1
    if palavra in reservadas:
        tipo = 'PALAVRA RESERVADA '+palavra.upper()
        lexemas.append([tipo,palavra])
        return palavra,i,tipo
    elif len(palavra) > limite:
        tipo = 'IDENTIFICADOR FORA DO LIMITE'
        lexemas.append(['IDENTIFICADOR',palavra])
        identificadores.append([palavra,'NULL'])
        return palavra,i,tipo
    else:
        tipo = 'IDENTIFICADOR'
        lexemas.append([tipo,palavra])
        identificadores.append([palavra, 'NULL'])
        return palavra, i, tipo

def numeros_I_R(texto,posicao):
  tamanho = len(texto)-1
  if posicao  ==  tamanho:
      numero = texto[posicao]
      tipo = 'NUMERO_INTEIRO'
      lexemas.append([tipo,numero])
      return numero,posicao,tipo

  tamanho_max = 15
  tamanho_n = 1
  tamanho_c = 1
  for i in range(posicao,tamanho):
    if texto[i] in numeros:
      numero = texto[i]
      j = i+1
      while texto[j] in numeros:
        numero = numero + texto[j]
        j = j+1
        tamanho_n = tamanho_n + 1
        if j  ==  tamanho:
          numero = numero + texto[j]
          break
      if texto[j]  ==  '.':
        numero = numero + texto[j]
        k = j+1
        while texto[k] in numeros:
          numero = numero + texto[k]
          k = k+1
          tamanho_c = tamanho_c + 1
        if tamanho_c > tamanho_max or tamanho_n > tamanho_max:
            tipo = 'NUMERO MAIOR QUE O LIMITE'
            lexemas.append(['NUMERO',numero])
            return numero, k, tipo
        tipo = 'NUMERO_REAL'
        lexemas.append([tipo,numero])
        return numero,k,tipo
      if tamanho_n > tamanho_max:
          tipo = 'NUMERO MAIOR QUE O LIMITE'
          lexemas.append(['NUMERO',numero])
          return numero, j, tipo
      tipo = 'NUMERO_INTEIRO'
      lexemas.append([tipo,numero])
      return numero,j,tipo

def especiais(texto,posicao):
  tamanho = len(texto)
  for i in range(posicao,tamanho):
    if texto[i] in simbolos:
      if texto[i]  ==  ':':
          if texto[i+1]+texto[i+2]  ==  ':=':
              tipo = '2P_2P_IGUAL'
              especi = '::='
              lexemas.append([tipo,especi])
              return especi, i+1, tipo
          elif texto[i+1]  ==  '=':
              tipo = '2P_IGUAL'
              especi = ':='
              lexemas.append([tipo,especi])
              return especi, i+1, tipo
          else:
              tipo = '2PONTOS'
              especi = ':'
              lexemas.append([tipo,especi])
              return especi, i, tipo
      if texto[i]  ==  '<':
          if texto[i+1]  ==  '=':
              tipo = 'MENOR_IGUAL'
              especi = '<='
              lexemas.append([tipo,especi])
              return especi, i+1, tipo
          elif texto[i+1]  ==  '>':
              tipo = 'MENOR_MAIOR'
              especi = '<>'
              lexemas.append([tipo,especi])
              return especi, i+1, tipo
          else:
              tipo = 'MENOR'
              especi = '<'
              lexemas.append([tipo,especi])
              return especi, i, tipo
      if texto[i]  ==  '>':
          if texto[i+1]  ==  '=':
              tipo = 'MAIOR_IGUAL'
              especi = '>='
              lexemas.append([tipo,especi])
              return especi, i+1, tipo
          else:
              tipo = 'MAIOR'
              especi = '>'
              lexemas.append([tipo,especi])
              return especi, i, tipo
      if texto[i]  ==  '(':
        tipo = 'ABRE_PARENTESES'
        especi = '('
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  ')':
        tipo = 'FECHA_PARENTESES'
        especi = ')'
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  '[':
        tipo = 'ABRE_COLCHETES'
        especi = '['
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  ']':
        tipo = 'FECHA_COLCHETES'
        especi = ']'
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  '{':
        tipo = 'ABRE_CHAVES'
        especi = '{'
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  '}':
        tipo = 'FECHA_CHAVES'
        especi = '}'
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  '+':
        tipo = 'OP_SOMA'
        especi = '+'
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  '-':
        tipo = 'OP_SUBTRACAO'
        especi = '-'
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  '*':
        tipo = 'OP_MULTIPLICACAO'
        especi = '*'
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  '=':
        tipo = 'OP_IGUAL'
        especi = '='
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  '.':
        tipo = 'OP_PONTO'
        especi = '.'
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  ';':
        tipo = 'OP_PONTO_VIRGULA'
        especi = ';'
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  ',':
        tipo = 'OP_VIRGULA'
        especi = ','
        lexemas.append([tipo,especi])
        return especi,i,tipo
      if texto[i]  ==  '/':
        tipo = 'OP_BARRA'
        especi = '/'
        lexemas.append([tipo,especi])
        return especi,i,tipo
  return None, None, None

def limpar_sintatico():
    sintatico.delete(0,END)
    semantico.delete(0, END)

def imprimirAnalise():
    tabela.delete(0,END)
    tabela2.delete(0, END)
    tabela3.delete(0, END)
    limpar_sintatico()
    inicia_tab()
    texto = bloco.get('1.0',END)
    terminou = False
    i = 0
    linha = 1
    while terminou  ==  False:
        if i  ==  len(texto):
            terminou = True
            break
        if texto[i]  ==  ' ':
            i = i + 1
        elif texto[i]  ==  '\t':
            i = i + 1
        elif texto[i]  ==  '\n':
            i = i + 1
            linha = linha + 1
        elif texto[i] in alfabeto or texto[i] in alfabeto_m or texto[i]  ==  '_':
            elem,k,tipo = ler_texto(texto,i)
            if tipo  ==  'IDENTIFICADOR FORA DO LIMITE':
                i = k
                tabela.insert(END, elem)
                tabela2.insert(END, tipo)
                tabela3.insert(END, linha)
                tabela.itemconfig(END, {'bg': 'yellow'})
                tabela2.itemconfig(END, {'bg': 'yellow'})
                tabela3.itemconfig(END, {'bg': 'yellow'})
            else:
                i = k
                tabela.insert(END, elem)
                tabela2.insert(END, tipo)
                tabela3.insert(END, linha)
                tabela.itemconfig(END, {'bg': '#00FF7F'})
                tabela2.itemconfig(END, {'bg': '#00FF7F'})
                tabela3.itemconfig(END, {'bg': '#00FF7F'})

        elif texto[i]  ==  ',' and texto[i-1] in numeros and texto[i+1] in numeros:
            tabela.insert(END, texto[i-1]+texto[i]+texto[i+1])
            tabela2.insert(END, 'Utilize o "." ao invés da "virgula "')
            tabela3.insert(END, linha)
            tabela.itemconfig(END, {'bg': 'yellow'})
            tabela2.itemconfig(END, {'bg': 'yellow'})
            tabela3.itemconfig(END, {'bg': 'yellow'})
            i = i + 1
        elif texto[i] not in numeros and texto[i] not in simbolos:
            tabela.insert(END, texto[i])
            tabela2.insert(END, 'NÃO PERTENCE AO ALFABETO')
            tabela3.insert(END, linha)
            tabela.itemconfig(END, {'bg': 'red'})
            tabela2.itemconfig(END, {'bg': 'red'})
            tabela3.itemconfig(END, {'bg': 'red'})
            i = i + 1
        elif texto[i] in numeros:
            numero, j, tipo = numeros_I_R(texto, i)
            tabela.insert(END, numero)
            tabela2.insert(END, tipo)
            tabela3.insert(END, linha)
            if tipo  ==  'NUMERO MAIOR QUE O LIMITE':
                tabela.itemconfig(END, {'bg': 'yellow'})
                tabela2.itemconfig(END, {'bg': 'yellow'})
                tabela3.itemconfig(END, {'bg': 'yellow'})
            else:
                tabela.itemconfig(END, {'bg': '#00FF7F'})
                tabela2.itemconfig(END, {'bg': '#00FF7F'})
                tabela3.itemconfig(END, {'bg': '#00FF7F'})
            i = j
        elif texto[i] in simbolos:
            numero, k, tipo = especiais(texto, i)
            if numero  ==  '{':
                comentario,p,tipo_com = ler_comentario(texto,k)
                if 'NÃO' in tipo_com:
                    tabela.insert(END, comentario)
                    tabela2.insert(END, tipo_com)
                    tabela3.insert(END, linha)
                    tabela.itemconfig(END, {'bg': 'red'})
                    tabela2.itemconfig(END, {'bg': 'red'})
                    tabela3.itemconfig(END, {'bg': 'red'})
                    i = p
                else:
                    i = p
                    tabela.insert(END, numero)
                    tabela2.insert(END, tipo)
                    tabela3.insert(END, linha)
                    tabela.itemconfig(END, {'bg': '#00FF7F'})
                    tabela2.itemconfig(END, {'bg': '#00FF7F'})
                    tabela3.itemconfig(END, {'bg': '#00FF7F'})
                    tabela.insert(END, comentario)
                    tabela2.insert(END, tipo_com)
                    tabela3.insert(END, linha)
                    tabela.itemconfig(END, {'bg': '#00FF7F'})
                    tabela2.itemconfig(END, {'bg': '#00FF7F'})
                    tabela3.itemconfig(END, {'bg': '#00FF7F'})

            elif numero  ==  '/' and texto[i+1]  ==  '/':
                comentario, p, tipo_com = ler_comentario(texto, k)
                i = p + 1
                tabela.insert(END, numero)
                tabela2.insert(END, tipo)
                tabela3.insert(END, linha)
                tabela.itemconfig(END, {'bg': '#00FF7F'})
                tabela2.itemconfig(END, {'bg': '#00FF7F'})
                tabela3.itemconfig(END, {'bg': '#00FF7F'})
                tabela.insert(END, numero)
                tabela2.insert(END, tipo)
                tabela3.insert(END, linha)
                tabela.itemconfig(END, {'bg': '#00FF7F'})
                tabela2.itemconfig(END, {'bg': '#00FF7F'})
                tabela3.itemconfig(END, {'bg': '#00FF7F'})
                tabela.insert(END, comentario)
                tabela2.insert(END, tipo_com)
                tabela3.insert(END, linha)
                tabela.itemconfig(END, {'bg': '#00FF7F'})
                tabela2.itemconfig(END, {'bg': '#00FF7F'})
                tabela3.itemconfig(END, {'bg': '#00FF7F'})
            else:
                i = k + 1
                tabela.insert(END, numero)
                tabela2.insert(END, tipo)
                tabela3.insert(END, linha)
                tabela.itemconfig(END, {'bg': '#00FF7F'})
                tabela2.itemconfig(END, {'bg': '#00FF7F'})
                tabela3.itemconfig(END, {'bg': '#00FF7F'})
    global lexemas,identificadores
    for i in range(len(lexemas)):
        if lexemas[i][0]  ==  'PALAVRA RESERVADA INT' or lexemas[i][0]  ==  'PALAVRA RESERVADA BOOLEAN':
            j = i + 1
            while lexemas[j][0] != 'OP_PONTO_VIRGULA':
                if lexemas[j][0]  ==  'IDENTIFICADOR':
                    for k in range(len(identificadores)):
                        if identificadores[k][0]  ==  lexemas[j][1]:
                            if identificadores[k][1]  ==  lexemas[i][0][18:]:
                                print(f'possui 2 variaveis com o mesmo nome "{identificadores[k][0]}"')
                                break
                            else:
                                identificadores[k][1] = lexemas[i][0][18:]
                                break
                j += 1
            if lexemas[i-1][0]  ==  '2PONTOS':
                j = i-2
                while lexemas[j][0] != 'PALAVRA RESERVADA VAR':
                    if lexemas[j][0]  ==  'IDENTIFICADOR':
                        for k in range(len(identificadores)):
                            if identificadores[k][0]  ==  lexemas[j][1]:
                                if identificadores[k][1]  ==  lexemas[i][0][18:]:
                                    print(f'possui 2 variaveis com o mesmo nome "{identificadores[k][0]}"')
                                    break
                                else:
                                    identificadores[k][1] = lexemas[i][0][18:]
                                    break
                    j -= 1
        elif lexemas[i][0] == 'IDENTIFICADOR' and lexemas[i+1][0] == '2P_IGUAL':
            j = i + 1
            aux = []
            while lexemas[j][0] != 'OP_PONTO_VIRGULA':
                if (lexemas[j][0] == 'IDENTIFICADOR' or lexemas[j][0] == 'NUMERO_INTEIRO' or
                        lexemas[j][0] == 'PALAVRA RESERVADA FALSE' or lexemas[j][0] == 'PALAVRA RESERVADA TRUE'):
                    aux.append(lexemas[j][1])
                j += 1
            expressoes.append([lexemas[i][1], aux])
    pops = []
    for i in range(len(identificadores)):
        if identificadores[i][1] == 'NULL':
            pops.append(i)
    identificadores = [x for i,x in enumerate(identificadores) if i not in pops]
    print(expressoes)
    print(identificadores)
    print(lexemas)
    analise_semantica()
    #program()
    lexemas.clear()

def analise_semantica():
    for i in range(len(expressoes)):
        tipos = []
        for j in range(len(identificadores)):
            if expressoes[i][0] == identificadores[j][0]:
                for k in range(len(expressoes[i][1])):
                    if expressoes[i][1][k].isdigit():
                        tipos.append('INT')
                    elif expressoes[i][1][k] == 'true' or expressoes[i][1][k] == 'false':
                        tipos.append('BOOLEAN')
                    else:
                        for aux in range(len(identificadores)):
                            if identificadores[aux][0] == expressoes[i][1][k]:
                                tipos.append(identificadores[aux][1])

                todos_iguais = all(x == identificadores[j][1] for x in tipos)
                if not todos_iguais:
                    semantico.insert(END,f"Erro na expressao {expressoes[i][0]}:={expressoes[i][1]}")


def atualiza_linha(event):
    texto = bloco.get('0.0',END)
    numeros_l.config(state='normal')
    numeros_l.delete('0.0',END)
    n = 2
    numeros_l.insert(END,str(1))
    for i in range(len(texto)-1):
        if texto[i] == "\n":
            numeros_l.insert(END, '\n' + str(n))
            n = n + 1
    numeros_l.yview_moveto(bloco.yview()[0])
    numeros_l.config(state='disabled')

def multiple_yview(*args):
    tabela.yview(*args)
    tabela2.yview(*args)
    tabela3.yview(*args)
    sintatico.yview(*args)

def multiple_yview_l(*args):
    bloco.yview(*args)
    numeros_l.yview(*args)

def scrollwheel(event):
    return 'break'

def obter_token():
    global i_lexemas, token
    token = lexemas[i_lexemas]
    i_lexemas += 1


def obter_token2():
    global i_lexemas, token2
    token2 = lexemas[i_lexemas+1]

def program():
    global token
    print('passei program')
    obter_token()
    if token[0]  ==  'PALAVRA RESERVADA PROGRAM':
        obter_token()
        if token[0]  ==  'IDENTIFICADOR':
            obter_token()
            if token[0]!= 'OP_PONTO_VIRGULA':
                sintatico.insert(END, 'Falta o ;')
            else:
                obter_token()
                while token[0]in ('PALAVRA RESERVADA INT', 'PALAVRA RESERVADA BOOLEAN', 'PALAVRA RESERVADA PROCEDURE',
                                'PALAVRA RESERVADA BEGIN'):
                    if token[0] ==  'PALAVRA RESERVADA INT' or token[0] ==  'PALAVRA RESERVADA BOOLEAN':
                        variable_declaring()
                        obter_token()
                    elif token[0] ==  'PALAVRA RESERVADA PROCEDURE':
                        procedure_declaration()
                        obter_token()
                    elif token[0] ==  'PALAVRA RESERVADA BEGIN':
                        execucao()
                        break
                obter_token()
                if token[0] ==  'PALAVRA RESERVADA END':
                    obter_token()
                    if token[0]!= 'OP_PONTO' or token[0]!= 'OP_PONTO_VIRGULA':
                        sintatico.insert(END, ' Falta o "." ou o ";" depois do END')
                else:
                    sintatico.insert(END, ' Falta o END, para finalizar o programa')
        else:
            sintatico.insert(END,'Falta o Identificador')
    else:
        sintatico.insert(END,'Falta o "program" ')

def execucao():
    global token
    obter_token()
    if token[0] ==  'PALAVRA RESERVADA BEGIN':
        obter_token()
        while token[0]!= 'PALAVRA RESERVADA END':
            comando()
            obter_token()
        obter_token()
        if token[0]!= 'OP_PONTO_VIRGULA':
            sintatico.insert(END, 'Falta o ";" ')

def comando():
    global token
    obter_token()
    if token[0] ==  'PALAVRA RESERVADA INT' or token[0] ==  'PALAVRA RESERVADA BOOLEAN':
        variable_declaring()
    elif token[0] ==  'PALAVRA RESERVADA IF':
        conditional_statement()
    elif token[0] ==  'IDENTIFIER':
        obter_token2()
        if token2[0]  ==  '2P_IGUAL':
            variable_assignment()
        elif token2[0]  ==  'ABRE_PARENTESES':
            procedure_call()
        else:
            sintatico.insert(END, 'Apos o Identificador necessita ser ":=" ou "(" ')
    else:
        sintatico.insert(END, 'Necessita ter "int", "boolean", "if" ou "Identificador" ')

def variable_declaring():
    global token
    variaveis = []
    while True:
        obter_token()
        if token[0] ==  'IDENTIFICADOR':
            variaveis.append(['IDENTIFICADOR',i_lexemas])
        else:
            sintatico.insert(END, 'Falta o Identificador ')
        obter_token()
        if token[0]!= 'OP_VIRGULA':
            break

    if token[0] ==  '2PONTOS':
        obter_token()
    else:
        sintatico.insert(END, 'Falta o ":"')

    if token[0]!= 'OP_VIRGULA':
        sintatico.insert(END, 'Falta o ";"')

def variable_assignment():
    global token
    obter_token()
    if token[0] ==  'IDENTIFICADOR':
        obter_token()
    else:
        sintatico.insert(END, 'Falta o identificador')
    if token[0]!= '2P_IGUAL':
        sintatico.insert(END, 'Falta o ":=" ')


    assigned_type = evaluate_expression()

    obter_token()
    if token[0] != 'OP_VIRGULA':
        sintatico.insert(END, 'Falta o ";"')


def evaluate_expression():
    global token
    # Começa avaliando o primeiro termo
    result_type = evaluate_term()
    obter_token()
    # Avalia operadores de soma/subtração
    while token[0]  ==  'OP_SOMA' or token[0]  ==  'OP_SUBTRACAO':
        term_type = evaluate_term()

        # Verifica a compatibilidade dos tipos
        if result_type != term_type:
            sintatico.insert(END,f"Type mismatch in operation: '{result_type}' and '{term_type}' are incompatible.")
        obter_token()

    return result_type

def evaluate_term():
    global token
    # Começa avaliando o primeiro fator
    result_type = evaluate_factor()

    # Avalia operadores de multiplicação/divisão
    while token[0] ==  'PALAVRA RESERVADA DIV' or token[0] ==  'OP_MULTIPLICACAO':
        factor_type = evaluate_factor()

        # Verifica a compatibilidade dos tipos
        if result_type != factor_type:
            sintatico.insert(END,f"Type mismatch in operation: '{result_type}' and '{factor_type}' are incompatible.")

    return result_type

def evaluate_factor():
    global token
    obter_token()
    if token[0] ==  'IDENTIFICADOR':
        # Busca o tipo da variável e consome o token
        for i in range(len(identificadores)):
            if token[1] == identificadores[0]:
                var_type = identificadores[1]
                return var_type

    elif token[0] ==  'PALAVRA RESERVADA INT':
        return 'PALAVRA RESERVADA INT'

    elif token[0] ==  'ABRE_PARENTESES':
        result_type = evaluate_expression()
        return result_type

    else:
        sintatico.insert(END,f"Unexpected token[0]in factor: {token}")

def procedure_call():
    global token
    obter_token()
    if token[0] ==  'IDENTIFICADOR':
        obter_token()
    else:
        sintatico.insert(END,'Falta o identificador')
    
    if token[0] ==  'ABRE_PARENTESES':
        obter_token()
    else:
        sintatico.insert(END, 'Falta o "(" ')
        
    while token[0]!= 'FECHA_PARENTESES':
        expression()
        if token[0] ==  'OP_VIRGULA':
            obter_token()

    if token[0] ==  'FECHA_PARENTESES':
        obter_token()
    else:
        sintatico.insert(END, 'Falta o ")" ')
    if token[0] ==  'OP_PONTO_VIRGULA':
        obter_token()
    else:
        sintatico.insert(END, 'Falta o ";" ')

def expression():
    global token
    if token[0]in ['IDENTIFICADOR','PALAVRA RESERVADA INT','PALAVRA RESERVADA TRUE', 'PALAVRA RESERVADA FALSE']:
        obter_token()
    else:
        sintatico.insert(END,f"Unexpected token[0]in expression: {token}")

def conditional_statement():
    global token
    obter_token()
    if token[0] ==  'PALAVRA RESERVADA IF':
        boolean_expression()
        obter_token()
        if token[0] ==  'PALAVRA RESERVADA THEN':
            comando()
        if token[0] ==  'PALAVRA RESERVADA ELSE':
            comando()

def boolean_expression():
    global token
    term()
    while token[0]in ['MENOR', 'MAIOR','MENOR_IGUAL', 'MAIOR_IGUAL']:
        obter_token()
        term()

def term():
    global token
    factor()
    while token[0] ==  'OP_SOMA' or token[0] ==  'OP_SUBTRACAO':
        obter_token()
        factor()

def factor():
    global token
    if token[0]in ['IDENTIFICADOR', 'PALAVRA RESERVADA INT']:
        obter_token()
    elif token[0] ==  'ABRE_PARENTESES':
        obter_token()
        boolean_expression()
        if token[0] ==  'FECHA_PARENTESES':
            obter_token()
        else:
            sintatico.insert(END,'Faltou o ")" ')
    else:
        sintatico.insert(END,f'token[0]nao esperado em fator {token}')

def procedure_declaration():
    global token
    if token[0] ==  'PALAVRA RESERVADA PROCEDURE':
        obter_token()
        procedure_name = token[1]
        if token[0] ==  'IDENTIFICADOR':
            obter_token()
        else:
            sintatico.insert(END, 'Faltou o identificador ')

        if token[0] ==  'ABRE_PARENTESES':
            obter_token()
        else:
            sintatico.insert(END, 'Faltou o "(" ')
        param_list = []

        while token[0]!= 'FECHA_PARENTESES':
            obter_token()
            if token[0] ==  'IDENTIFICADOR':
                obter_token()
            else:
                sintatico.insert(END, 'Faltou o identificador ')
            if token[0] ==  '2PONTOS':
                obter_token()
            else:
                sintatico.insert(END, 'Faltou o ":" ')

            param_type = ''

            for i in range(len(identificadores)):
                if token[1] == identificadores[0]:
                    param_type = identificadores[1]

            if param_type not in ['PALAVRA RESERVADA INT','PALAVRA RESERVADA BOOLEAN']:
                sintatico.insert(END,
                    f"Invalid parameter type '{param_type}' for procedure '{procedure_name}'.")

            obter_token()
            if token[0] ==  'IDENTIFICADOR':
                obter_token()
            else:
                sintatico.insert(END, 'Faltou o identificador ')

            if token[0] ==  'OP_VIRGULA':
                obter_token()
        obter_token()
        if token[0] ==  'OP_PONTO_VIRGULA':
            obter_token()
    else:
        sintatico.insert(END,f"Expected 'PROCEDURE' keyword, found {token[0]}")


#------------------------------------------ INTERFACE ------------------------------------------------------------------

janela = Tk()
janela.title("Analisador Lexico")
janela.geometry("1000x550")
janela.config(background='#BA55D3')

scrollbar_l = Scrollbar(janela,orient='vertical')
scrollbar_l.grid(column=0,row=0,padx=0,pady=0,sticky=N+S)
bloco = Text(janela, width=60, height=20,yscrollcommand = scrollbar_l.set)
bloco.grid(column=2,row=0,padx=5,pady=0)
bloco.bind("<KeyRelease>", atualiza_linha)
bloco.bind("<KeyPress>", atualiza_linha)
bloco.bind('<MouseWheel>', scrollwheel)
bloco.bind('<Enter>', atualiza_linha)
bloco.bind('<Leave>', atualiza_linha)

numeros_l = Text(janela,wrap='none', width=4, height=20,background='lightgrey',state='disabled',yscrollcommand = scrollbar_l.set)
numeros_l.grid(column=1,row=0,padx=2,pady=0)
numeros_l.config(state='normal')
numeros_l.insert('1.0', '1')
numeros_l.config(state='disabled')
numeros_l.bind('<MouseWheel>', scrollwheel)

scrollbar_l.config(command=multiple_yview_l)
scrollbar = Scrollbar(janela,orient='vertical')
scrollbar.grid(column=6,row=0,padx=0,pady=0,sticky=N+S)
tabela = Listbox(janela,height=20,width=20,borderwidth=2,yscrollcommand = scrollbar.set)
tabela.grid(column=3,row=0,ipadx=0,pady=0,stick=E)
tabela2 = Listbox(janela,height=20,width=30,borderwidth=2,yscrollcommand = scrollbar.set)
tabela2.grid(column=4,row=0,padx=0,pady=0)
tabela3 = Listbox(janela,height=20,width=10,borderwidth=2,yscrollcommand = scrollbar.set)
tabela3.grid(column=5,row=0,padx=0,pady=0)


scrollbar.config( command = multiple_yview )
botao = Button(janela, text="Analisar", command = imprimirAnalise)
botao.grid(column=3, row=1, padx=0, pady=5)

sintatico = Listbox(janela,height=5,width=80,borderwidth=2,yscrollcommand = scrollbar.set)
sintatico.grid(column=2,row=1,padx=0,pady=5)

semantico = Listbox(janela,height=5,width=80,borderwidth=2,yscrollcommand = scrollbar.set)
semantico.grid(column=2,row=2,padx=0,pady=5)

menu = Menu(janela)
menu_arq = Menu(menu)
menu_arq.add_command(label='Abrir .txt',command=abrir_arq)
menu_arq.add_command(label='Salvar .txt',command=salvar_arq)
menu.add_cascade(label='Arquivo',menu=menu_arq)

janela.config(menu = menu)
inicia_tab()
janela.mainloop()