import pygame
import random
import sys
import math
import os

# Inicializar o Pygame
pygame.init()

# Configurações da janela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Cão Vingador: A Caçada ao Hambúrguer")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
verde = (0, 255, 0)
roxo = (100, 0, 100)

# Fonte para texto
fonte_texto = pygame.font.Font(None, 40)

# Arquivo de ranking
arquivo_ranking = "ranking.txt"

# Função para carregar imagens
def carregar_imagem(caminho, tamanho):
    try:
        imagem = pygame.image.load(caminho)
        return pygame.transform.scale(imagem, tamanho)
    except pygame.error:
        imagem_placeholder = pygame.Surface(tamanho)
        imagem_placeholder.fill(preto)
        return imagem_placeholder

# Carregar imagens
image_cachorro = carregar_imagem("assets/cachorro.png", (50, 50))
imagem_hamburguer = carregar_imagem("assets/hamburguer.png", (50, 50))
image_vilao = carregar_imagem("assets/vilao.png", (50, 50))
imagem_fundo = carregar_imagem("assets/fundo.png", (largura, altura))

# Função para salvar a pontuação no ranking
def salvar_ranking(nome, pontuacao):
    with open(arquivo_ranking, "a") as arquivo:
        arquivo.write(f"{nome} {pontuacao}\n")

# Função para carregar o ranking
def carregar_ranking():
    if not os.path.exists(arquivo_ranking):
        return []
    with open(arquivo_ranking, "r") as arquivo:
        ranking = []
        for linha in arquivo:
            dados = linha.strip().rsplit(None, 1)
            if len(dados) != 2:
                continue
            nome, pontos = dados
            try:
                ranking.append((nome, int(pontos)))
            except ValueError:
                continue
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:5]

# Função para exibir o ranking
def exibir_ranking():
    tela.fill(branco)
    titulo = fonte_texto.render("Ranking - Top 5", True, preto)
    tela.blit(titulo, (largura // 3, altura // 6))

    ranking = carregar_ranking()
    for i, (nome, pontuacao) in enumerate(ranking):
        texto = fonte_texto.render(f"{i + 1}. {nome} - {pontuacao} pontos", True, preto)
        tela.blit(texto, (largura // 4, altura // 3 + i * 40))

    pygame.display.flip()
    pygame.time.delay(5000)

# Função para exibir a tela inicial
def tela_inicial():
    nome_digitado = ''
    rodando = True
    while rodando:
        tela.fill(branco)
        tela.blit(imagem_fundo, (0, 0))

        titulo = fonte_texto.render("Cão Vingador: A Caçada ao Hambúrguer", True, roxo)
        tela.blit(titulo, (largura // 4, altura // 6))

        texto_nome = fonte_texto.render("Digite seu nome:", True, preto)
        tela.blit(texto_nome, (largura // 4, altura // 3))

        nome_surface = fonte_texto.render(nome_digitado, True, preto)
        tela.blit(nome_surface, (largura // 4, altura // 2))

        botao_iniciar = pygame.Rect(largura // 3, altura // 1.5, 150, 50)
        pygame.draw.rect(tela, azul, botao_iniciar)
        texto_botao = fonte_texto.render("Iniciar", True, branco)
        tela.blit(texto_botao, (largura // 3 + 40, altura // 1.5 + 10))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome_digitado != '':
                    return nome_digitado
                elif evento.key == pygame.K_BACKSPACE:
                    nome_digitado = nome_digitado[:-1]
                else:
                    nome_digitado += evento.unicode
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    if nome_digitado != '':
                        return nome_digitado

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

# Função para mostrar a tela de Game Over
def mostrar_game_over(nome, pontuacao):
    salvar_ranking(nome, pontuacao)
    texto = fonte_texto.render(f"Game Over! Pontos: {pontuacao}", True, vermelho)
    tela.blit(texto, (largura // 4, altura // 3))
    pygame.display.flip()
    pygame.time.delay(2000)
    exibir_ranking()
    return menu_fim_de_jogo()

# Menu exibido depois do fim da partida
def menu_fim_de_jogo():
    while True:
        tela.fill(branco)
        titulo = fonte_texto.render("Fim de jogo", True, vermelho)
        jogar_novamente = fonte_texto.render("Pressione ENTER para jogar novamente", True, preto)
        sair = fonte_texto.render("Pressione ESC para sair", True, preto)

        tela.blit(titulo, (largura // 3, altura // 4))
        tela.blit(jogar_novamente, (largura // 6, altura // 2))
        tela.blit(sair, (largura // 4, altura // 2 + 50))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (
                evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return True

# Função para movimentar o vilão
def mover_vilao(vilao, jogador_x, jogador_y):
    distancia_x = jogador_x - vilao["x"]
    distancia_y = jogador_y - vilao["y"]
    distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)

    if distancia > 0:
        vilao["x"] += (distancia_x / distancia) * vilao["velocidade"]
        vilao["y"] += (distancia_y / distancia) * vilao["velocidade"]

# Loop principal do jogo
def jogo(nome):
    jogador_x, jogador_y = largura // 2, altura // 2
    tamanho_jogador = 50
    velocidade_jogador = 7
    pontuacao = 0
    fase = 1

    clock = pygame.time.Clock()
    hamburguer_x, hamburguer_y = random.randint(0, largura - 50), random.randint(0, altura - 50)

    viloes = [
        {"x": random.randint(0, largura - 50), "y": random.randint(0, altura - 50), "velocidade": 1}
    ]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()

        jogador_x += (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * velocidade_jogador
        jogador_y += (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * velocidade_jogador

        jogador_x = max(0, min(jogador_x, largura - tamanho_jogador))
        jogador_y = max(0, min(jogador_y, altura - tamanho_jogador))

        if pygame.Rect(jogador_x, jogador_y, tamanho_jogador, tamanho_jogador).colliderect(
            pygame.Rect(hamburguer_x, hamburguer_y, 50, 50)):
            pontuacao += 1
            hamburguer_x, hamburguer_y = random.randint(0, largura - 50), random.randint(0, altura - 50)

        for vilao in viloes:
            mover_vilao(vilao, jogador_x, jogador_y)
            if pygame.Rect(jogador_x, jogador_y, tamanho_jogador, tamanho_jogador).colliderect(
                pygame.Rect(vilao["x"], vilao["y"], 50, 50)):
                return mostrar_game_over(nome, pontuacao)

        if pontuacao >= 10 * fase:
            fase += 1
            if fase == 2:
                viloes.append({
                    "x": random.randint(0, largura - 50),
                    "y": random.randint(0, altura - 50),
                    "velocidade": 1 + fase
                })
            for vilao in viloes:
                vilao["velocidade"] += 0.5

        tela.fill(branco)
        tela.blit(imagem_fundo, (0, 0))
        tela.blit(image_cachorro, (jogador_x, jogador_y))
        tela.blit(imagem_hamburguer, (hamburguer_x, hamburguer_y))
        for vilao in viloes:
            tela.blit(image_vilao, (vilao["x"], vilao["y"]))

        texto = fonte_texto.render(f"Nome: {nome} Pontos: {pontuacao} Fase: {fase}", True, preto)
        tela.blit(texto, (10, 10))

        pygame.display.flip()
        clock.tick(60)

# Função principal
def main():
    while True:
        nome = tela_inicial()
        if not nome or not jogo(nome):
            break

if __name__ == "__main__":
    main()
# C extensions