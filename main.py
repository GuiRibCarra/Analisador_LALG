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
i_lexemas = 0


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

def ler_comentario(texto,posicao):
    i = posicao+1
    tamanho = len(texto) - 1
    palavra = ''
    if texto[i-1] == '{':
        while texto[i] != '}':
            if i == tamanho:
                return palavra,i,'NÃO_FECHOU_COMENTARIO'
            else:
                palavra = palavra + texto[i]
                i = i + 1
    else:
        i = i+1
        while texto[i] != '\n':
            if i == tamanho:
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
        if i == tamanho:
            break
        else:
            palavra = palavra + texto[i]
            i = i+1
    if palavra in reservadas:
        tipo = 'PALAVRA RESERVADA '+palavra.upper()
        lexemas.append(tipo)
        return palavra,i,tipo
    elif len(palavra) > limite:
        tipo = 'IDENTIFICADOR FORA DO LIMITE'
        lexemas.append('IDENTIFICADOR')
        return palavra,i,tipo
    else:
        tipo = 'IDENTIFICADOR'
        lexemas.append(tipo)
        return palavra, i, tipo

def numeros_I_R(texto,posicao):
  tamanho = len(texto)-1
  if posicao == tamanho:
      numero = texto[posicao]
      tipo = 'NUMERO_INTEIRO'
      lexemas.append(tipo)
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
        if j == tamanho:
          numero = numero + texto[j]
          break
      if texto[j] == '.':
        numero = numero + texto[j]
        k = j+1
        while texto[k] in numeros:
          numero = numero + texto[k]
          k = k+1
          tamanho_c = tamanho_c + 1
        if tamanho_c > tamanho_max or tamanho_n > tamanho_max:
            tipo = 'NUMERO MAIOR QUE O LIMITE'
            lexemas.append('Numero')
            return numero, k, tipo
        tipo = 'NUMERO_REAL'
        lexemas.append(tipo)
        return numero,k,tipo
      if tamanho_n > tamanho_max:
          tipo = 'NUMERO MAIOR QUE O LIMITE'
          lexemas.append('Numero')
          return numero, j, tipo
      tipo = 'NUMERO_INTEIRO'
      lexemas.append(tipo)
      return numero,j,tipo

def especiais(texto,posicao):
  tamanho = len(texto)
  for i in range(posicao,tamanho):
    if texto[i] in simbolos:
      if texto[i] == ':':
          if texto[i+1]+texto[i+2] == ':=':
              tipo = '2P_2P_IGUAL'
              especi = '::='
              lexemas.append(tipo)
              return especi, i+1, tipo
          elif texto[i+1] == '=':
              tipo = '2P_IGUAL'
              especi = ':='
              lexemas.append(tipo)
              return especi, i+1, tipo
          else:
              tipo = '2PONTOS'
              especi = ':'
              lexemas.append(tipo)
              return especi, i, tipo
      if texto[i] == '<':
          if texto[i+1] == '=':
              tipo = 'MENOR_IGUAL'
              especi = '<='
              lexemas.append(tipo)
              return especi, i+1, tipo
          elif texto[i+1] == '>':
              tipo = 'MENOR_MAIOR'
              especi = '<>'
              lexemas.append(tipo)
              return especi, i+1, tipo
          else:
              tipo = 'MENOR'
              especi = '<'
              lexemas.append(tipo)
              return especi, i, tipo
      if texto[i] == '>':
          if texto[i+1] == '=':
              tipo = 'MAIOR_IGUAL'
              especi = '>='
              lexemas.append(tipo)
              return especi, i+1, tipo
          else:
              tipo = 'MAIOR'
              especi = '>'
              lexemas.append(tipo)
              return especi, i, tipo
      if texto[i] == '(':
        tipo = 'ABRE_PARENTESES'
        especi = '('
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == ')':
        tipo = 'FECHA_PARENTESES'
        especi = ')'
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == '[':
        tipo = 'ABRE_COLCHETES'
        especi = '['
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == ']':
        tipo = 'FECHA_COLCHETES'
        especi = ']'
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == '{':
        tipo = 'ABRE_CHAVES'
        especi = '{'
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == '}':
        tipo = 'FECHA_CHAVES'
        especi = '}'
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == '+':
        tipo = 'OP_SOMA'
        especi = '+'
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == '-':
        tipo = 'OP_SUBTRACAO'
        especi = '-'
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == '*':
        tipo = 'OP_MULTIPLICACAO'
        especi = '*'
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == '=':
        tipo = 'OP_IGUAL'
        especi = '='
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == '.':
        tipo = 'OP_PONTO'
        especi = '.'
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == ';':
        tipo = 'OP_PONTO_VIRGULA'
        especi = ';'
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == ',':
        tipo = 'OP_VIRGULA'
        especi = ','
        lexemas.append(tipo)
        return especi,i,tipo
      if texto[i] == '/':
        tipo = 'OP_BARRA'
        especi = '/'
        lexemas.append(tipo)
        return especi,i,tipo
  return None, None, None

def limpar_sintatico():
    sintatico.delete(0,END)

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
    while terminou == False:
        if i == len(texto):
            terminou = True
            break
        if texto[i] == ' ':
            i = i + 1
        elif texto[i] == '\t':
            i = i + 1
        elif texto[i] == '\n':
            i = i + 1
            linha = linha + 1
        elif texto[i] in alfabeto or texto[i] in alfabeto_m or texto[i] == '_':
            elem,k,tipo = ler_texto(texto,i)
            if tipo == 'IDENTIFICADOR FORA DO LIMITE':
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

        elif texto[i] == ',' and texto[i-1] in numeros and texto[i+1] in numeros:
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
            if tipo == 'NUMERO MAIOR QUE O LIMITE':
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
            if numero == '{':
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

            elif numero == '/' and texto[i+1] == '/':
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
    lexemas.append('$')
    for i in range(len(lexemas)):
        print(lexemas[i])
    index = 0
    program(index)
    lexemas.clear()

def atualiza_linha(event):
    texto = bloco.get('0.0',END)
    numeros_l.config(state='normal')
    numeros_l.delete('0.0',END)
    n = 2
    numeros_l.insert(END,str(1))
    for i in range(len(texto)-1):
        if(texto[i] == "\n"):
            numeros_l.insert(END, '\n'+ str(n))
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

def obter_token(i):
    texto = lexemas[i]
    index = i + 1
    print(texto,i)
    return texto,index

def program(index):
    token,i_lexemas = obter_token(index)
    if token == 'PALAVRA RESERVADA PROGRAM':
        token,i_lexemas = obter_token(i_lexemas)
        if token == 'IDENTIFICADOR':
            token,i_lexemas = obter_token(i_lexemas)
            if token == 'OP_PONTO_VIRGULA':
                bloco_(i_lexemas)
            else:
                sintatico.insert(END,'Falta o ;')
                bloco_(i_lexemas-1)
        else:
            sintatico.insert(END,'Falta o Identificador')
            bloco_(i_lexemas)
    else:
        sintatico.insert(END,'Falta o "program" ')
        bloco_(i_lexemas+1)

def bloco_(index):
    token,i_lexemas = obter_token(index)
    if token == 'PALAVRA RESERVADA INT' or token == 'PALAVRA RESERVADA BOOLEAN':
        i_lexemas = parte_declaracao_variaveis(i_lexemas-1)
    if token == 'PALAVRA RESERVADA PROCEDURE':
        i_lexemas = parte_de_declaracao_de_subrotina(i_lexemas - 1)
    i_lexemas = comando_composto(i_lexemas)
    return i_lexemas



def lista_de_identificadores(index):
    token,i_lexemas = obter_token(index)
    if token == 'IDENTIFICADOR':
        token,i_lexemas = obter_token(i_lexemas)
        if token == 'OP_VIRGULA' or token == 'IDENTIFICADOR':
            while True:
                if token == 'OP_VIRGULA':
                    token,i_lexemas = obter_token(i_lexemas)
                    if token == 'IDENTIFICADOR':
                        token,i_lexemas = obter_token(i_lexemas)
                        if token != 'OP_VIRGULA' and token != 'IDENTIFICADOR':
                            break
                    elif token == 'OP_VIRGULA':
                        sintatico.insert(END,'Falta um Identificador entre as virgulas')
                        token,i_lexemas = obter_token(i_lexemas)
                    else:
                        sintatico.insert(END,'Nao terminou com um identificador')
                        break
                elif token == 'IDENTIFICADOR':
                    token2,i_lexemas2 = obter_token(i_lexemas-2)
                    if token2 == 'OP_VIRGULA':
                        token, i_lexemas = obter_token(i_lexemas)
                    else:
                        sintatico.insert(END,'Falta uma virgula entre os identificadores')
                        token,i_lexemas = obter_token(i_lexemas)

                    if token != 'OP_VIRGULA' and token != 'IDENTIFICADOR':
                        break
    return i_lexemas

def declaracao_variaveis(index):
    token,i_lexemas = obter_token(index)
    if token == 'PALAVRA RESERVADA INT' or token == 'PALAVRA RESERVADA BOOLEAN':
        i_lexemas = lista_de_identificadores(i_lexemas)
    else:
        sintatico.insert(END,'tipo nao suportado')
    return i_lexemas

def parte_declaracao_variaveis(index):
    i_lexemas = declaracao_variaveis(index)
    token,i_lexemas = obter_token(i_lexemas-1)
    while True:
        if token == 'OP_PONTO_VIRGULA':
            i_lexemas = declaracao_variaveis(i_lexemas)
            token,i_lexemas = obter_token(i_lexemas-1)
            token2,i_lexemas2 = obter_token(i_lexemas)
            if token2 != 'PALAVRA RESERVADA INT' and token != 'PALAVRA RESERVADA BOOLEAN':
                break
    return i_lexemas
                
def secao_de_parametros_formais(index):
    token, i_lexemas = obter_token(index)
    if token == 'PALAVRA RESERVADA VAR':
        i_lexemas = lista_de_identificadores(i_lexemas)
        token, i_lexemas = obter_token(i_lexemas)
        if token == '2PONTOS':
            token, i_lexemas = obter_token(i_lexemas)
            if token == "IDENTIFICADOR":
                return i_lexemas
            else:
                sintatico.insert(END, 'Falta o identificador final')
        else:
            sintatico.insert(END, 'Falta o ":" ')
            return i_lexemas+1
    else:
        i_lexemas = lista_de_identificadores(i_lexemas-1)
        token, i_lexemas = obter_token(i_lexemas)
        if token == '2PONTOS':
            token, i_lexemas = obter_token(i_lexemas)
            if token == "IDENTIFICADOR":
                return i_lexemas

    return i_lexemas


def parametros_formais(index):
    token, i_lexemas = obter_token(index)
    if token == 'ABRE_PARENTESES':
        i_lexemas = secao_de_parametros_formais(i_lexemas)
        token, i_lexemas = obter_token(i_lexemas)
        while True:
            if token == 'OP_PONTO_VIRGULA':
                i_lexemas = secao_de_parametros_formais(i_lexemas)
                token, i_lexemas = obter_token(i_lexemas)
                if token != 'FECHA_PARENTESES':
                    break
            else:
                sintatico.insert(END, 'Falta o ";" ')
        if token == 'FECHA_PARENTESES':
            return i_lexemas
        else:
            sintatico.insert(END, 'Falta o ")" ')
    else:
        sintatico.insert(END, 'Falta o "(" ')
    return i_lexemas

def declaracao_de_procedimento(index):
    token, i_lexemas = obter_token(index)
    if token == 'PALAVRA RESERVADA PROCEDURE':
        token, i_lexemas = obter_token(i_lexemas)
        if token == 'IDENTIFICADOR':
            token, i_lexemas = obter_token(i_lexemas)
            if token == 'ABRE_PARENTESES':
                i_lexemas = parametros_formais(i_lexemas-1)
                token, i_lexemas = obter_token(i_lexemas)
                if token == 'OP_PONTO_VIRGULA':
                    i_lexemas = bloco_(i_lexemas)
                else:
                    sintatico.insert(END, 'Falta o ";" ')
            elif token == 'OP_PONTO_VIRGULA':
                i_lexemas = bloco_(i_lexemas)
            else:
                sintatico.insert(END, 'Falta o ";" ')
        else:
            sintatico.insert(END, 'Falta o identificador ')

    return i_lexemas

def parte_de_declaracao_de_subrotina(index):
    token, i_lexemas = obter_token(index)
    if token != 'PALAVRA RESERVADA PROCEDURE':
        return i_lexemas-1
    else:
        while True:
            if token == 'PALAVRA RESERVADA PROCEDURE':
                i_lexemas = declaracao_de_procedimento(i_lexemas-1)
                token, i_lexemas = obter_token(i_lexemas)
                if token == 'OP_PONTO_VIRGULA':
                    token2, i_lexemas2 = obter_token(i_lexemas)
                    if token2 != 'PALAVRA RESERVADA PROCEDURE':
                        break
                    else:
                        token, i_lexemas = obter_token(i_lexemas)
        return i_lexemas

def relacao(index):
    token, i_lexemas = obter_token(index)
    if token == 'MENOR_IGUAL':
        return i_lexemas
    elif token == 'MENOR_MAIOR':
        return i_lexemas
    elif token == 'MENOR':
        return i_lexemas
    elif token == 'MAIOR_IGUAL':
        return i_lexemas
    elif token == 'MAIOR':
        return i_lexemas
    elif token == 'OP_IGUAL':
        return i_lexemas
    else:
        sintatico.insert(END, 'Falta o operando de relação ')
        return i_lexemas

def variavel(index):
    token, i_lexemas = obter_token(index)
    if token == 'IDENTIFICADOR':
        token, i_lexemas = obter_token(i_lexemas)
        if token == 'ABRE_COLCHETES':
            i_lexemas = expressao(i_lexemas)
            if token == 'FECHA_COLCHETES':
                return i_lexemas
            else:
                sintatico.insert(END, 'Falta o "]" ')
        else:
            return i_lexemas
    else:
        sintatico.insert(END, 'Falta o identificador ')
    return i_lexemas

def fator(index):
    token, i_lexemas = obter_token(index)
    if token == "IDENTIFICADOR":
        variavel(index)
        return i_lexemas
    elif token == 'NUMERO':
        return i_lexemas
    elif token == 'ABRE_PARENTESES':
        i_lexemas = expressao(i_lexemas)
        token, i_lexemas = obter_token(i_lexemas)
        if token == 'FECHA_PARENTESES':
            return i_lexemas
        else:
            sintatico.insert(END, 'Falta o ")" ')
    elif token == 'PALAVRA RESERVADA NOT':
        fator(i_lexemas)
        return i_lexemas
    else:
        sintatico.insert(END, 'Falta o fator corretamente ')
    return i_lexemas

def termo(index):
    i_lexemas = fator(index)
    token, i_lexemas = obter_token(i_lexemas)
    while True:
        if token == 'OP_MULTIPLICACAO' or token == 'PALAVRA RESERVADA DIV' or token == 'PALAVRA RESERVADA AND':
            i_lexemas = fator(index)
            token, i_lexemas = obter_token(i_lexemas)
        else:
            break
    return i_lexemas

def expressao_simples(index):
    token, i_lexemas = obter_token(index)
    if token == "OP_SOMA" or token == 'OP_SUBTRACAO':
        i_lexemas = termo(i_lexemas)
        token, i_lexemas = obter_token(i_lexemas)
        while True:
            if token == 'OP_SOMA' or token == 'OP_SUBTRACAO' or token == 'PALAVRA RESERVADA OR':
                i_lexemas = termo(index)
                token, i_lexemas = obter_token(i_lexemas)
            else:
                break
        return i_lexemas
    else:
        i_lexemas = termo(index)
        token, i_lexemas = obter_token(i_lexemas)
        while True:
            if token == 'OP_SOMA' or token == 'OP_SUBTRACAO' or token == 'PALAVRA RESERVADA OR':
                i_lexemas = termo(index)
                token, i_lexemas = obter_token(i_lexemas)
            else:
                break
        return i_lexemas

def expressao(index):
    i_lexemas = expressao_simples(index)
    token, i_lexemas = obter_token(i_lexemas)
    if token in 'MENOR' or token in 'MAIOR' or token in 'IGUAL':
        i_lexemas = relacao(i_lexemas-1)
        i_lexemas = expressao_simples(i_lexemas)

    return i_lexemas

def lista_expressao(index):
    i_lexemas = expressao(index)
    token,i_lexemas = obter_token(i_lexemas)
    while True:
        if token == 'OP_VIRGULA':
            i_lexemas = expressao(i_lexemas)
            token, i_lexemas = obter_token(i_lexemas)
        else:
            break
    return i_lexemas

def atribuicao(index):
    i_lexemas = variavel(index)
    token,i_lexemas = obter_token(i_lexemas)
    if token == '2P_IGUAL':
        i_lexemas = expressao(i_lexemas)
        return i_lexemas
    else:
        sintatico.insert(END, 'Falta o := ')
        i_lexemas = expressao(i_lexemas+1)
        return i_lexemas

def chamada_de_procedimento(index):
    token, i_lexemas = obter_token(index)
    if token == "IDENTIFICADOR":
        token, i_lexemas = obter_token(i_lexemas)
        if token == 'ABRE_PARENTESES':
            i_lexemas = lista_expressao(i_lexemas)
            token, i_lexemas = obter_token(i_lexemas)
            if token == 'FECHA_PARENTESES':
                return i_lexemas
            else:
                sintatico.insert(END, 'Falta fechar o parenteses')
                return i_lexemas
    else:
        sintatico.insert(END, 'Esta faltando o identificador')
        token, i_lexemas = obter_token(i_lexemas)
        if token == 'ABRE_PARENTESES':
            i_lexemas = lista_expressao(i_lexemas)
            token, i_lexemas = obter_token(i_lexemas)
            if token == 'FECHA_PARENTESES':
                return i_lexemas
            else:
                sintatico.insert(END, 'Falta fechar o parenteses')
        return i_lexemas

def IF(index):
    token, i_lexemas = obter_token(index)
    if token == 'PALAVRA RESERVADA IF':
        i_lexemas = expressao(i_lexemas)
        token,i_lexemas = obter_token(i_lexemas)
        if token == 'PALAVRA RESERVADA THEN':
            i_lexemas = comando(i_lexemas)
            token, i_lexemas = obter_token(i_lexemas)
            if token == 'PALAVRA RESERVADA ELSE':
                i_lexemas = comando(i_lexemas)
            return i_lexemas
        else:
            sintatico.insert(END, 'Falta o THEN')
            i_lexemas = comando(i_lexemas)
            token, i_lexemas = obter_token(i_lexemas)
            if token == 'PALAVRA RESERVADA ELSE':
                i_lexemas = comando(i_lexemas)
            return i_lexemas
    else:
        sintatico.insert(END, 'Falta o IF')

    return i_lexemas

def WHILE(index):
    token, i_lexemas = obter_token(index)
    if token == 'PALAVRA RESERVADA WHILE':
        i_lexemas = expressao(i_lexemas)
        token, i_lexemas = obter_token(i_lexemas)
        if token == 'PALAVRA RESERVADA DO':
            i_lexemas = comando(i_lexemas)
        else:
            sintatico.insert(END, 'Falta o DO')
    else:
        sintatico.insert(END, 'Falta o While')

def comando(index):
    token,i_lexemas = obter_token(index)
    if token == 'IDENTIFICADOR':
        token2,i_lexemas2 = obter_token(i_lexemas)
        if token2 == '2P_IGUAL':
            i_lexemas = atribuicao(index)
        else:
            i_lexemas = chamada_de_procedimento(i_lexemas)
    elif token == 'PALAVRA RESERVADA BEGIN':
        i_lexemas = comando_composto(i_lexemas)
    elif token == 'PALAVRA RESERVADA IF':
        i_lexemas = IF(i_lexemas)
    elif token == 'PALAVRA RESERVADA WHILE':
        i_lexemas = WHILE(i_lexemas)
    return i_lexemas

def comando_composto(index):
    token, i_lexemas = obter_token(index)
    if token == 'PALAVRA RESERVADA BEGIN':
        i_lexemas = comando(i_lexemas)
        while True:
            token, i_lexemas = obter_token(i_lexemas)
            if token == 'OP_PONTO_VIRGULA':
                i_lexemas = comando(i_lexemas)
            else:
                break
        token, i_lexemas = obter_token(i_lexemas)
        if token == 'PALAVRA RESERVADA END':
            return i_lexemas
        else:
            sintatico.insert(END, 'Falta o END')
            return i_lexemas

def sinc(index,tipo):
    if tipo == 'PROGRAM':
        token, i_lexemas = obter_token(index)
        while True:
            if token == 'PALAVRA RESERVADA INT' or token == 'PALAVRA RESERVADA BOOLEAN':
                bloco_(i_lexemas)
                break
            elif token == 'PALAVRA RESERVADA PROCEDURE':
                bloco_(i_lexemas)
                break
            elif token == 'PALAVRA RESERVADA BEGIN':
                bloco_(i_lexemas)
                break
            else:
                token, i_lexemas = obter_token(i_lexemas)

    elif tipo == 'PARTE DECLARAÇÃO VARIAVEIS':
        token, i_lexemas = obter_token(index)
        while True:
            if token == 'PALAVRA RESERVADA PROCEDURE':
                parte_de_declaracao_de_subrotina(i_lexemas)
                break
            elif token == 'PALAVRA RESERVADA BEGIN':
                comando_composto(i_lexemas)
                break
            elif token == 'OP_PONTO':
                break
            else:
                token, i_lexemas = obter_token(i_lexemas)

    elif tipo == 'PARTE DECLARAÇÃO ROTINAS':
        token, i_lexemas = obter_token(index)
        while True:
            if token == 'PALAVRA RESERVADA BEGIN':
                comando_composto(i_lexemas)
                break
            elif token == 'OP_PONTO':
                break
            else:
                token, i_lexemas = obter_token(i_lexemas)

    elif tipo == 'DECLARAÇÃO DE VARIAVEIS':
        token, i_lexemas = obter_token(index)
        while True:
            if token == 'OP_PONTO_VIRGULA':
                token2, i_lexemas2 = obter_token(i_lexemas+1)
                if token == 'PALAVRA RESERVADA INT' or token == 'PALAVRA RESERVADA BOOLEAN':
                    declaracao_variaveis(i_lexemas)
                elif token == 'PALAVRA RESERVADA PROCEDURE':
                    parte_de_declaracao_de_subrotina(i_lexemas)
                    break
                elif token == 'PALAVRA RESERVADA BEGIN':
                    comando_composto(i_lexemas)
                    break
            elif token == 'OP_PONTO':
                break
            else:
                token, i_lexemas = obter_token(i_lexemas)

    elif tipo == 'LISTA IDENTIFICADORES':
        token, i_lexemas = obter_token(index)
        while True:
            if token == 'OP_VIRGULA':
                lista_de_identificadores(i_lexemas)
                break
            if token == 'OP_PONTO_VIRGULA':
                token2, i_lexemas2 = obter_token(i_lexemas+1)
                if token2 == 'PALAVRA RESERVADA INT' or token2 == 'PALAVRA RESERVADA BOOLEAN':
                    declaracao_variaveis(i_lexemas)
                elif token2 == 'PALAVRA RESERVADA PROCEDURE':
                    parte_de_declaracao_de_subrotina(i_lexemas)
                    break
                elif token2 == 'PALAVRA RESERVADA BEGIN':
                    comando_composto(i_lexemas)
                    break
            else:
                token, i_lexemas = obter_token(i_lexemas)

    elif tipo == 'DECLARAÇÃO DE PROCEDIMENTO':
        token, i_lexemas = obter_token(index)
        while True:
            if token == 'OP_PONTO_VIRGULA':
                parte_de_declaracao_de_subrotina(i_lexemas)
                break
            elif token == 'PALAVRA RESERVADA BEGIN':
                comando_composto(i_lexemas)
                break
            else:
                token, i_lexemas = obter_token(i_lexemas)

    elif tipo == 'PARAMETROS FORMAIS':
        token, i_lexemas = obter_token(index)
        while True:
            if token == 'OP_PONTO_VIRGULA':
                token2,i_lexemas2 = obter_token(i_lexemas)
                if token2 == 'PALAVRA RESERVADA INT' or token2 == 'PALAVRA RESERVADA BOOLEAN' or token2 == 'PALAVRA RESERVADA PROCEDURE':
                    i_lexemas = bloco_(i_lexemas)
                else:
                    i_lexemas = secao_de_parametros_formais(i_lexemas)
            else:
                token, i_lexemas = obter_token(i_lexemas)

    elif tipo == 'SECAO DE PARAMETROS FORMAIS':
        token, i_lexemas = obter_token(index)
        while True:
            if token == 'OP_PONTO_VIRGULA':
                i_lexemas = secao_de_parametros_formais(i_lexemas)
            elif token == 'FECHA_PARENTESES':
                i_lexemas = bloco_(i_lexemas+1)
            else:
                token, i_lexemas = obter_token(i_lexemas)

    elif tipo == 'COMANDO COMPOSTO':
        token, i_lexemas = obter_token(index)
        while True:
            if token == 'OP_PONTO_VIRGULA':
                token2, i_lexemas2 = obter_token(i_lexemas)
                if token2 == 'PALAVRA RESERVADA PROCEDURE':
                    i_lexemas = parte_de_declaracao_de_subrotina(i_lexemas)
                else:
                    i_lexemas = comando(i_lexemas)
            elif token == 'OP_PONTO':
                i_lexemas = len(lexemas)

    elif tipo == 'COMANDO':
        token, i_lexemas = obter_token(index)

    elif tipo == 'ATRIBUIÇÃO':
        token, i_lexemas = obter_token(index)

    elif tipo == 'CHAMADA DE PROCEDIMENTO':
        token, i_lexemas = obter_token(index)

    elif tipo == 'IF':
        token, i_lexemas = obter_token(index)

    elif tipo == 'WHILE':
        token, i_lexemas = obter_token(index)

    elif tipo == 'EXPRESSAO':
        token, i_lexemas = obter_token(index)

    elif tipo == 'EXPRESSAO SIMPLES':
        token, i_lexemas = obter_token(index)

    elif tipo == 'TERMO':
        token, i_lexemas = obter_token(index)

    elif tipo == 'FATOR':
        token, i_lexemas = obter_token(index)

    elif tipo == 'VARIAVEL':
        token, i_lexemas = obter_token(index)




#------------------------------------------ INTERFACE ------------------------------------------------------------------

janela = Tk()
janela.title("Analisador Lexico")
janela.geometry("1000x450")
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

menu = Menu(janela)
menu_arq = Menu(menu)
menu_arq.add_command(label='Abrir .txt',command=abrir_arq)
menu_arq.add_command(label='Salvar .txt',command=salvar_arq)
menu.add_cascade(label='Arquivo',menu=menu_arq)

janela.config(menu = menu)
inicia_tab()
janela.mainloop()