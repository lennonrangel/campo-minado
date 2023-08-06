# Importando Bibliotecas
import tkinter
from tkinter import *
import tkinter as tk
import random
from datetime import datetime

# Cores
co0 = "#FFFFFF"     # branca
co1 = "#333333"     # preta pesado
co2 = "#fff873"     # amarela
co3 = "#fcc058"     # laranja
co4 = "#FF0000"     # vermelha
co5 = "#3297a8"     # azul
co6 = "#DBDBDB"     # cinza claro
co7 = "#14189C"     # azul escuro
co8 = "#22B14C"     # verde
co9 = "#7F7F7F"     # cinza escuro
fundo = "#3b3b3b"   # preta

# Criação da janela do jogo
janela = tk.Tk()
janela.title('')
janela.geometry('380x540')
janela.configure(bg=fundo)

# Dividindo a janela em 2 frames
frame_cima = Frame(janela, width=361, height=80, bg=co1, relief="raised")
frame_cima.grid(row=0, column=0, sticky=NW, padx=10, pady=10)

frame_meio = Frame(janela, width=361, height=391, bg=fundo, relief="raised")
frame_meio.grid(row=1, column=0, sticky=NW, padx=10, pady=2)

frame_baixo = Frame(janela, width=360, height=35, bg=co1, relief="raised")
frame_baixo.grid(row=2, column=0, sticky=NW, padx=10, pady=2)

# Configurando os frames
app_x = Label(frame_cima, text="Campo Minado", height=1, relief="flat", anchor="center",
              font=('Ivy 20 bold'), bg=co1, fg=co5)
app_x.place(x=77, y=7)
app_0 = Label(frame_meio, text="Como jogar\n \nAs regras do Campo Minado são simples:\n "
                                "\n1. Se você descobrir uma mina, o jogo acaba. "
                                "\n2. Se descobrir um quadrado vazio, o jogo continua. "
                                "\n3. Se aparecer um número, ele informará quantas minas "
                                "\nestão escondidas nos oito quadrados que o cercam. "
                                "\n4. Você usa essa informação para deduzir em que "
                                "\nquadrados próximos é seguro clicar.\n "
                                "\n\nPara marcar as bombas clique no botão direito do mouse",
              height=15, font=('Ivy 10'), bg=co1, fg=co0)
app_0.place(x=12, y=50)

# Variáveis para contar as bombas
total_bombas = 0
bombas_marcadas = 0

# Variáveis para o cronômetro
tempo_inicial = None
cronometro_atualizado = True

# Função para atualizar o cronômetro
def atualizar_cronometro():
    global tempo_inicial, cronometro_atualizado
    if cronometro_atualizado:
        tempo_atual = datetime.now() - tempo_inicial
        minutos = tempo_atual.seconds // 60
        segundos = tempo_atual.seconds % 60
        tempo_formatado = f"{minutos:02d}:{segundos:02d}"
        label_cronometro.config(text="Tempo: " + tempo_formatado)
        label_cronometro.after(100, atualizar_cronometro)

# Função para parar o cronômetro
def parar_cronometro():
    global cronometro_atualizado
    cronometro_atualizado = False

# Rótulo para exibir o cronômetro
label_cronometro = Label(frame_cima, height=1, font=('Ivy 10 bold'), bg=co1, fg=co0)
label_cronometro.place(x=25, y=49)

# Função para iniciar o jogo
def iniciar_jogo():

    # Remover o botão "Jogar" quando o jogo começar
    b_jogar.place_forget()

    # Configurações do jogo
    largura = 15
    altura = 15
    bombas = 40
    total_bombas = bombas
    bombas_marcadas = 0

    # Iniciar o cronômetro
    global tempo_inicial, cronometro_atualizado
    tempo_inicial = datetime.now()
    cronometro_atualizado = True
    atualizar_cronometro()

    # Criando o frame para o campo minado
    frame_tabuleiro = Frame(frame_meio, width=350, height=350, bg=fundo)
    frame_tabuleiro.pack()

    # Criação dos botões/células
    botoes = []
    for i in range(altura):
        linha_botoes = []
        for j in range(largura):
            botao = tk.Button(frame_tabuleiro, width=2)
            botao.grid(row=i, column=j)
            botao.config(command=lambda linha=i, coluna=j: revelar_bloco(linha, coluna))
            botao.bind("<Button-3>", lambda event, linha=i, coluna=j: marcar_bloco(linha, coluna))
            linha_botoes.append(botao)
        botoes.append(linha_botoes)

    # Inicialização do campo minado
    campo_minado = [[0] * largura for _ in range(altura)]
    blocos_adjacentes = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),  (1, 0),  (1, 1)]
    blocos_revelados = [[False] * largura for _ in range(altura)]
    blocos_marcados = [[False] * largura for _ in range(altura)]

    # Distribuir bombas aleatoriamente
    bombas = random.sample(range(largura * altura), bombas)
    for b in bombas:
        linha = b // largura
        coluna = b % largura
        campo_minado[linha][coluna] = -1

    # Calcular os números de bombas adjacentes
    for i in range(altura):
        for j in range(largura):
            if campo_minado[i][j] != -1:
                for x, y in blocos_adjacentes:
                    if 0 <= i + x < altura and 0 <= j + y < largura and campo_minado[i + x][j + y] == -1:
                        campo_minado[i][j] += 1

    # Função para revelar um bloco
    def revelar_bloco(linha, coluna):
        if 0 <= linha < altura and 0 <= coluna < largura and not blocos_revelados[linha][coluna]:
            blocos_revelados[linha][coluna] = True
            if campo_minado[linha][coluna] == -1:
                # Game over - jogador clicou em uma bomba
                botao = botoes[linha][coluna]
                botao.config(text="💣", bg=co4)
                mostrar_todos_blocos()
                return
            if campo_minado[linha][coluna] == 0:
                # Revelar blocos adjacentes vazios
                botao = botoes[linha][coluna]
                botao.config(text="", bg=co6, relief=tk.SUNKEN)
                for x, y in blocos_adjacentes:
                    revelar_bloco(linha + x, coluna + y)
            else:
                numero = campo_minado[linha][coluna]
                # Revelar o número de bombas adjacentes com cores
                botao = botoes[linha][coluna]
                botao.config(relief=tk.SUNKEN, text=numero, bg=co6)
                if numero == 1:
                    botao.config(fg=co5)
                elif numero == 2:
                    botao.config(fg=co8)
                elif numero == 3:
                    botao.config(fg=co4)
                elif numero == 4:
                    botao.config(fg=co7)
                elif numero == 5:
                    botao.config(fg=co3)
                elif numero == 6:
                    botao.config(fg=co0)
                elif numero == 7:
                    botao.config(fg=fundo)
                elif numero == 8:
                    botao.config(fg=co1)

            # Verificar se o jogador venceu
            if all(all(blocos_revelados[linha][coluna] or campo_minado[linha][coluna] == -1
                       for coluna in range(largura)) for linha in range(altura)):
                mostrar_vitoria()

    # Função para marcar ou desmarcar um bloco
    def marcar_bloco(linha, coluna):

        # Variável global
        global bombas_marcadas

        if 0 <= linha < altura and 0 <= coluna < largura and not blocos_revelados[linha][coluna]:
            botao = botoes[linha][coluna]
            if not blocos_marcados[linha][coluna]:
                botao.config(text="🏴", bg=co2)
                blocos_marcados[linha][coluna] = True
                bombas_marcadas += 1 # Incrementa o contador de bombas marcadas
            else:
                botao.config(text="")
                blocos_marcados[linha][coluna] = False
                bombas_marcadas -= 1 # Decrementa o contador de bombas marcadas

            # Atualiza o rótulo com o contador de bombas marcadas
            contador_bombas.config(text=f"Bombas: {bombas_marcadas}/{total_bombas}    ")

    # Criação do rótulo para exibir o contador de bombas marcadas
    contador_bombas = Label(frame_cima, text=f"Bombas: {bombas_marcadas}/{total_bombas}    ", height=1, font=('Ivy 10 bold'), bg=co1, fg=co0)
    contador_bombas.place(x=245, y=49)

    # Função para mostrar todos os blocos após o fim do jogo
    def mostrar_todos_blocos():
        for i in range(altura):
            for j in range(largura):
                botao = botoes[i][j]
                if campo_minado[i][j] == -1:
                    botao.config(text="💣", bg=co4)
                else:
                    campo_minado[i][j] > 0
                    botao.config(text=campo_minado[i][j])
        label_derrota = Label(frame_baixo, text=" Que pena! Você perdeu! ", height=1, font=('Ivy 15 bold'), bg=co4, fg=co0)
        label_derrota.place(x=56, y=2)
        parar_cronometro()

    def mostrar_vitoria():
        label_vitoria = Label(frame_baixo, text=" Parabéns! Você venceu! ", height=1, font=('Ivy 15 bold'), bg=co8, fg=co0)
        label_vitoria.place(x=56, y=2)
        parar_cronometro()

    def limpar_frame_baixo():
        for widget in frame_baixo.winfo_children():
            widget.destroy()

    # Função para reiniciar o jogo
    def reiniciar_jogo():
        # Destruir o frame atual
        frame_tabuleiro.destroy()

        # Limpar o conteúdo do frame_baixo
        limpar_frame_baixo()

        # Chamar a função iniciar_jogo para começar um novo jogo
        iniciar_jogo()

        global bombas_marcadas, total_bombas  # Adicionamos as variáveis globais aqui
        bombas_marcadas = 0
        total_bombas = 0

    # Botão reiniciar
    b_reiniciar = Button(frame_cima, command=reiniciar_jogo, text='Reiniciar', width=10, height=1,
                         font=('Ivy 10 bold'),overrelief=RIDGE, relief='raised', bg=fundo, fg=co0)
    b_reiniciar.place(x=135, y=47)

# Botão jogar
b_jogar = Button(frame_cima, command=iniciar_jogo, text='Jogar', width=10, height=1,
                 font=('Ivy 10 bold'), overrelief=RIDGE, relief='raised', bg=fundo, fg=co0)
b_jogar.place(x=135, y=47)

# Loop principal da interface gráfica
janela.mainloop()
