import pygame
import random

# --- INICIALIZAÇÃO ---
pygame.init()
pygame.mixer.init()

# Carrega as músicas
pygame.mixer.music.load("music/music2.mp3")
pygame.mixer.music.set_volume(0.5)  # Ajusta o volume da música
pygame.mixer.music.play(-1)  # Toca a música em loop

# Configurações da Janela
LARGURA, ALTURA = 1080, 1300
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meteor 350 - Estrada Infinita")

# Cores
PRETO = (0, 0, 0)
AMARELO_RE = (255, 204, 0) 
CINZA_ASFALTO = (40, 40, 40)
BRANCO = (255, 255, 255)

# Cores novas
VERDE_GRAMA = (34, 139, 34)
PRATA_BARREIRA = (192, 192, 192)
AZUL_PAINEL = (20, 20, 60) # Um azul escuro para o fundo do placar

# --- CONFIGURAÇÕES DE LAYOUT ---
MARGEM_ESQUERDA = 50       # Espaço da grama/acostamento
LARGURA_PISTA = 600        # Largura do asfalto
LIMITE_DIREITO_PISTA = MARGEM_ESQUERDA + LARGURA_PISTA # Onde termina o asfalto (pixel 650)
LARGURA_PAINEL = LARGURA - LIMITE_DIREITO_PISTA - 15   # Espaço que sobra para o Score

# --- CARREGAMENTO DE ASSETS ---
try:
    imagem_moto = pygame.image.load("assets/moto_com_piloto.png")
    imagem_moto = pygame.transform.scale(imagem_moto, (200, 120))
    imagem_moto = pygame.transform.rotate(imagem_moto, 90)
    
# Carrega a Kombi original (Horizontal)
    imagem_kombi_orig = pygame.image.load("assets/kombi.png")
    
    # Rotaciona para ficar Vertical (Apontando para cima/frente)
    # Como a imagem original aponta para a direita (0° no Pygame), 
    # precisamos de 90° (anti-horário) para apontar para cima.
    imagem_kombi = pygame.transform.rotate(imagem_kombi_orig, 90)
    
    # Redimensiona para um tamanho adequado à pista e à moto (ex: 150 largura, 300 altura)
    imagem_kombi = pygame.transform.scale(imagem_kombi, (200,350))
    
except:
    print("Imagem não encontrada. Usando reserva.")
    imagem_moto = pygame.Surface((100, 200))
    imagem_moto.fill(AMARELO_RE)
    print("Imagem 'kombi.png' não encontrada. Usando reserva.")
    imagem_kombi = pygame.Surface((150, 300))
    imagem_kombi.fill((200, 0, 0)) # Carro vermelho de reserva

# --- CONFIGURAÇÕES DA PISTA ---
velocidade_pista = 10
pista_y1 = 0
pista_y2 = -ALTURA 

# --- VARIÁVEIS DA MOTO ---
moto_x = LARGURA // 2 - 50 
moto_y = ALTURA - 300     
velocidade_moto = 8


clock = pygame.time.Clock()

## --- CONFIGURAÇÕES DO OBSTÁCULO ---
obs_largura = 70
obs_altura = 120
obs_x = random.randint(300, 700) # Mantém o obstáculo mais centralizado na pista
obs_y = -200 
obs_velocidade = 5

# --- CONFIGURAÇÕES DE TEXTO ---
pygame.font.init() # Inicializa o sistema de fontes
fonte_placar = pygame.font.SysFont("Arial", 40, bold=True)
fonte_label = pygame.font.SysFont("Arial", 25)

# Variáveis do Jogo
pontuacao = 0
vidas = 3

def desenhar_estrada(pista_y1, pista_y2):
    # Grama
    pygame.draw.rect(tela, VERDE_GRAMA, [0, 0, MARGEM_ESQUERDA, ALTURA])
    # Asfalto
    pygame.draw.rect(tela, CINZA_ASFALTO, [MARGEM_ESQUERDA, pista_y1, LARGURA_PISTA, ALTURA])
    pygame.draw.rect(tela, CINZA_ASFALTO, [MARGEM_ESQUERDA, pista_y2, LARGURA_PISTA, ALTURA])
    
    # Faixas Brancas
    x_faixa = MARGEM_ESQUERDA + (LARGURA_PISTA // 2) - 2
    for i in range(25):
        pygame.draw.rect(tela, BRANCO, [x_faixa, pista_y1 + i * 100, 5, 50])
        pygame.draw.rect(tela, BRANCO, [x_faixa, pista_y2 + i * 100, 5, 50])
    
    # Guardi-Rail
    pygame.draw.rect(tela, PRATA_BARREIRA, [LIMITE_DIREITO_PISTA, 0, 15, ALTURA])

def desenhar_painel(pontos, vidas_atuais):
    # Fundo do Painel
    pygame.draw.rect(tela, AZUL_PAINEL, [LIMITE_DIREITO_PISTA + 15, 0, LARGURA_PAINEL, ALTURA])
    
    x_texto = LIMITE_DIREITO_PISTA + 40
    # Textos
    tela.blit(fonte_label.render("DISTÂNCIA:", True, BRANCO), (x_texto, 50))
    tela.blit(fonte_placar.render(f"{int(pontos)} km", True, AMARELO_RE), (x_texto, 85))
    
    tela.blit(fonte_label.render("PILOTO:", True, BRANCO), (x_texto, 200))
    cor_vida = (255, 50, 50) if vidas_atuais > 1 else (255, 255, 0)
    tela.blit(fonte_placar.render("♥ " * vidas_atuais, True, cor_vida), (x_texto, 235))

def reset_posicao():
    return MARGEM_ESQUERDA + (LARGURA_PISTA // 2) - 50, ALTURA - 300

def exibir_tela_game_over(pontuacao_final):
    # Escurece um pouco a tela de fundo
    overlay = pygame.Surface((LARGURA, ALTURA))
    overlay.set_alpha(180) # Transparência
    overlay.fill((0, 0, 0))
    tela.blit(overlay, (0, 0))

    # Textos da tela final
    texto_titulo = fonte_placar.render("GAME OVER", True, (255, 50, 50))
    texto_score = fonte_label.render(f"Você rodou {int(pontuacao_final)} km com sua Meteor!", True, BRANCO)
    texto_instrucao = fonte_label.render("Pressione 'R' para Reiniciar ou 'ESC' para Sair", True, AMARELO_RE)

    # Posicionamento centralizado
    tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, ALTURA // 2 - 100))
    tela.blit(texto_score, (LARGURA // 2 - texto_score.get_width() // 2, ALTURA // 2))
    tela.blit(texto_instrucao, (LARGURA // 2 - texto_instrucao.get_width() // 2, ALTURA // 2 + 100))
    
    pygame.display.flip()

# --- VARIÁVEIS DE ESTADO ---
rodando = True
game_over = False

while rodando:
    # 1. GERENCIAMENTO DE EVENTOS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Se estiver em Game Over e apertar uma tecla
        if game_over and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r: # Reiniciar
                # Reseta todas as variáveis para o padrão inicial
                vidas = 3
                pontuacao = 0
                velocidade_pista = 10
                moto_x, moto_y = reset_posicao()
                obs_y = -500
                game_over = False
            if evento.key == pygame.K_ESCAPE: # Sair
                rodando = False
    
    if not game_over:

        # B. LÓGICA DE MOVIMENTAÇÃO E PONTUAÇÃO
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and moto_x > MARGEM_ESQUERDA: moto_x -= velocidade_moto
        if teclas[pygame.K_RIGHT] and moto_x < LIMITE_DIREITO_PISTA - 100: moto_x += velocidade_moto
        if teclas[pygame.K_UP] and moto_y > 50: moto_y -= velocidade_moto
        if teclas[pygame.K_DOWN] and moto_y < ALTURA - 200: moto_y += velocidade_moto

        # Rolagem da pista e aumento de dificuldade
        pista_y1 += velocidade_pista
        pista_y2 += velocidade_pista
        if pista_y1 >= ALTURA: pista_y1 = pista_y2 - ALTURA
        if pista_y2 >= ALTURA: pista_y2 = pista_y1 - ALTURA
        
        pontuacao += 0.1
        # DIFICULDADE: A cada 100km, a pista acelera um pouco
        velocidade_pista = 10 + (int(pontuacao) // 100)

        # C. LÓGICA DO OBSTÁCULO (KOMBI)
        obs_y += obs_velocidade + velocidade_pista
        if obs_y > ALTURA:
            obs_y = -500
            obs_x = random.randint(MARGEM_ESQUERDA + 20, LIMITE_DIREITO_PISTA - 220)

        # D. COLISÃO
        rect_moto = imagem_moto.get_rect(topleft=(moto_x, moto_y)).inflate(-60, -40)
        rect_obs = imagem_kombi.get_rect(topleft=(obs_x, obs_y)).inflate(-50, -60)

        if rect_moto.colliderect(rect_obs):
            vidas -= 1
            obs_y = -500
            moto_x, moto_y = reset_posicao()
            if vidas <= 0:
                game_over = True
        # Se a vida chegar a zero, ativa o Game Over
        if vidas <= 0:
            game_over = True
            
        # E. RENDERIZAÇÃO (Onde a mágica acontece)
        tela.fill(PRETO)
        
        desenhar_estrada(pista_y1, pista_y2) # Chama a função da estrada
        
        tela.blit(imagem_kombi, (obs_x, obs_y))
        tela.blit(imagem_moto, (moto_x, moto_y))
        
        desenhar_painel(pontuacao, vidas) # Chama a função do painel
        
    else:
        # Se game_over for True, apenas exibe a tela final
        exibir_tela_game_over(pontuacao)
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()