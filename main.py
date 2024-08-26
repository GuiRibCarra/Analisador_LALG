import tkinter.filedialog
import tkinter.messagebox
from tkinter import *
#------------------------------------------------ FUNCOES -------------------------------------------------------------
def inicia_tab():
    tabela.insert(END,'ELEMENTO')
    tabela.itemconfig(END, {'bg': '#EE82EE'})
    tabela2.insert(END, 'TIPO')
    tabela2.itemconfig(END, {'bg': '#EE82EE'})
    tabela3.insert(END, 'LINHA')
    tabela3.itemconfig(END, {'bg': '#EE82EE'})

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
        return palavra,i,tipo
    elif len(palavra) > limite:
        tipo = 'IDENTIFICADOR FORA DO LIMITE'
        return palavra,i,tipo
    else:
        tipo = 'IDENTIFICADOR'
        return palavra, i, tipo

def numeros_I_R(texto,posicao):
  tamanho = len(texto)-1
  if posicao == tamanho:
      numero = texto[posicao]
      tipo = 'NUMERO_INTEIRO'
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
            return numero, k, tipo
        tipo = 'NUMERO_REAL'
        return numero,k,tipo
      if tamanho_n > tamanho_max:
          tipo = 'NUMERO MAIOR QUE O LIMITE'
          return numero, j, tipo
      tipo = 'NUMERO_INTEIRO'
      return numero,j,tipo

def especiais(texto,posicao):
  tamanho = len(texto)
  for i in range(posicao,tamanho):
    if texto[i] in simbolos:
      if texto[i] == ':':
          if texto[i+1]+texto[i+2] == ':=':
              tipo = '2P_2P_IGUAL'
              especi = '<='
              return especi, i+1, tipo
          elif texto[i+1] == '=':
              tipo = '2P_IGUAL'
              especi = ':='
              return especi, i+1, tipo
          else:
              tipo = '2PONTOS'
              especi = ':'
              return especi, i, tipo
      if texto[i] == '<':
          if texto[i+1] == '=':
              tipo = 'MENOR_IGUAL'
              especi = '<='
              return especi, i+1, tipo
          elif texto[i+1] == '>':
              tipo = 'MENOR_MAIOR'
              especi = '<>'
              return especi, i+1, tipo
          else:
              tipo = 'MENOR'
              especi = '<'
              return especi, i, tipo
      if texto[i] == '>':
          if texto[i+1] == '=':
              tipo = 'MAIOR_IGUAL'
              especi = '>='
              return especi, i+1, tipo
          else:
              tipo = 'MAIOR'
              especi = '>'
              return especi, i, tipo
      if texto[i] == '(':
        tipo = 'ABRE_PARENTESES'
        especi = '('
        return especi,i,tipo
      if texto[i] == ')':
        tipo = 'FECHA_PARENTESES'
        especi = ')'
        return especi,i,tipo
      if texto[i] == '[':
        tipo = 'ABRE_COLCHETES'
        especi = '['
        return especi,i,tipo
      if texto[i] == ']':
        tipo = 'FECHA_COLCHETES'
        especi = ']'
        return especi,i,tipo
      if texto[i] == '{':
        tipo = 'ABRE_CHAVES'
        especi = '{'
        return especi,i,tipo
      if texto[i] == '}':
        tipo = 'FECHA_CHAVES'
        especi = '}'
        return especi,i,tipo
      if texto[i] == '+':
        tipo = 'OP_SOMA'
        especi = '+'
        return especi,i,tipo
      if texto[i] == '-':
        tipo = 'OP_SUBTRACAO'
        especi = '-'
        return especi,i,tipo
      if texto[i] == '*':
        tipo = 'OP_MULTIPLICACAO'
        especi = '*'
        return especi,i,tipo
      if texto[i] == '=':
        tipo = 'OP_IGUAL'
        especi = '='
        return especi,i,tipo
      if texto[i] == '.':
        tipo = 'OP_PONTO'
        especi = '.'
        return especi,i,tipo
      if texto[i] == ';':
        tipo = 'OP_PONTO_VIRGULA'
        especi = ';'
        return especi,i,tipo
      if texto[i] == ',':
        tipo = 'OP_VIRGULA'
        especi = ','
        return especi,i,tipo
      if texto[i] == '/':
        tipo = 'OP_BARRA'
        especi = '/'
        return especi,i,tipo
  return None, None, None

def imprimirAnalise():
    tabela.delete(0,END)
    tabela2.delete(0, END)
    tabela3.delete(0, END)
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

#------------------------------------------ARRAYS ELEMENTOS-------------------------------------------------------------

alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_']
alfabeto_m = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
numeros=['0','1','2','3','4','5','6','7','8','9']
reservadas= ['program','procedure','var','int','float','boolean','read','write','true','false','begin','end','if','then','else','while','do','or','div','and','not']
simbolos = ['::=',':=',':','=','<','>','<=','>=',',','<>','+','-','*','[',']','{','}',';','.','_','(',')','/']

#------------------------------------------ INTERFACE ------------------------------------------------------------------

janela = Tk()
janela.title("Analisador Lexico")
janela.geometry("1000x400")
janela.config(background='#BA55D3')
scrollbar_l = Scrollbar(janela,orient='vertical')
scrollbar_l.grid(column=0,row=0,padx=0,pady=0,sticky=N+S)
bloco = Text(janela, width=60, height=20,yscrollcommand = scrollbar_l.set)
bloco.grid(column=2,row=0,padx=5,pady=0)
numeros_l = Text(janela,wrap='none', width=4, height=20,background='lightgrey',state='disabled',yscrollcommand = scrollbar_l.set)
numeros_l.grid(column=1,row=0,padx=2,pady=0)
numeros_l.config(state='normal')
numeros_l.insert('1.0', '1')
numeros_l.config(state='disabled')
bloco.bind("<KeyRelease>", atualiza_linha)
bloco.bind("<KeyPress>", atualiza_linha)

def multiple_yview_l(*args):
    bloco.yview(*args)
    numeros_l.yview(*args)

scrollbar_l.config(command=multiple_yview_l)

scrollbar = Scrollbar(janela,orient='vertical')
scrollbar.grid(column=6,row=0,padx=0,pady=0,sticky=N+S)
tabela = Listbox(janela,height=20,width=20,borderwidth=2,yscrollcommand = scrollbar.set)
tabela.grid(column=3,row=0,ipadx=0,pady=0,stick=E)
tabela2 = Listbox(janela,height=20,width=30,borderwidth=2,yscrollcommand = scrollbar.set)
tabela2.grid(column=4,row=0,padx=0,pady=0)
tabela3 = Listbox(janela,height=20,width=10,borderwidth=2,yscrollcommand = scrollbar.set)
tabela3.grid(column=5,row=0,padx=0,pady=0)

def multiple_yview(*args):
    tabela.yview(*args)
    tabela2.yview(*args)
    tabela3.yview(*args)

scrollbar.config( command = multiple_yview )
botao = Button(janela, text="Analisar", command = imprimirAnalise)
botao.grid(column=3, row=1, padx=0, pady=5)

menu = Menu(janela)
menu_arq = Menu(menu)
menu_arq.add_command(label='Abrir .txt',command=abrir_arq)
menu_arq.add_command(label='Salvar .txt',command=salvar_arq)
menu.add_cascade(label='Arquivo',menu=menu_arq)

janela.config(menu = menu)
inicia_tab()
janela.mainloop()