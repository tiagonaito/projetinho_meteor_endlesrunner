import pygame
import random

# --- INICIALIZAÇÃO ---
pygame.init()

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
    imagem_moto = pygame.image.load("moto_com_piloto.png")
    imagem_moto = pygame.transform.scale(imagem_moto, (200, 120))
    imagem_moto = pygame.transform.rotate(imagem_moto, 90)
    
# Carrega a Kombi original (Horizontal)
    imagem_kombi_orig = pygame.image.load("kombi.png")
    
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

# --- LOOP PRINCIPAL ---
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # 1. MOVIMENTAÇÃO DA MOTO
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and moto_x > MARGEM_ESQUERDA: 
        moto_x -= velocidade_moto
    # Limite Direito: Fim da pista menos a largura da moto (100px)
    if teclas[pygame.K_RIGHT] and moto_x < LIMITE_DIREITO_PISTA - 100: 
        moto_x += velocidade_moto
    if teclas[pygame.K_UP] and moto_y > 50: moto_y -= velocidade_moto
    if teclas[pygame.K_DOWN] and moto_y < ALTURA - 200: moto_y += velocidade_moto

    # 2. MOVIMENTAÇÃO DA ESTRADA
    pista_y1 += velocidade_pista
    pista_y2 += velocidade_pista
    # A cada frame, ganhamos um pouco de pontuação (simulando distância)
    pontuacao += 0.1
    if pista_y1 >= ALTURA: pista_y1 = pista_y2 - ALTURA
    if pista_y2 >= ALTURA: pista_y2 = pista_y1 - ALTURA

    # 3. Lógica do Obstáculo (Kombi)
    obs_y += obs_velocidade + velocidade_pista 
    
    if obs_y > ALTURA:
        obs_y = -500
        # Sorteia o X entre o início da pista e o fim dela (menos a largura da Kombi)
        # 150 a 450 é uma boa faixa de segurança
        obs_x = random.randint(MARGEM_ESQUERDA + 20, LIMITE_DIREITO_PISTA - 220)

    # 4. DETECÇÃO DE COLISÃO
    # Pegamos o retângulo real da imagem desenhada
    rect_moto_visual = imagem_moto.get_rect(topleft=(moto_x, moto_y))
    rect_obs_visual = imagem_kombi.get_rect(topleft=(obs_x, obs_y))

    # Criamos o "Hitbox" (a área que realmente mata)
    # .inflate(-largura, -altura) encolhe o retângulo para dentro
    hitbox_moto = rect_moto_visual.inflate(-60, -40) # Tira 30px de cada lado e 20px de cima/baixo
    hitbox_obs = rect_obs_visual.inflate(-50, -60)   # Encolhe a Kombi para ignorar os espelhos/bordas

    # A verificação agora é entre os Hitboxes, não as imagens
    if hitbox_moto.colliderect(hitbox_obs):
        vidas -= 1
        obs_y = -500 # Reseta a Kombi
        moto_x, moto_y = MARGEM_ESQUERDA + (LARGURA_PISTA // 2) - 50, ALTURA - 300
        
        if vidas <= 0:
            print("GAME OVER! Sua Meteor foi para a oficina.")
            rodando = False # Encerra o jogo se as vidas acabarem

    # 5. DESENHO (A ORDEM IMPORTA!)
    tela.fill(PRETO) # Limpa tudo

    # A. Grama (Esquerda)
    pygame.draw.rect(tela, VERDE_GRAMA, [0, 0, MARGEM_ESQUERDA, ALTURA])

    # B. Asfalto (Pista deslocada)
    pygame.draw.rect(tela, CINZA_ASFALTO, [MARGEM_ESQUERDA, pista_y1, LARGURA_PISTA, ALTURA])
    pygame.draw.rect(tela, CINZA_ASFALTO, [MARGEM_ESQUERDA, pista_y2, LARGURA_PISTA, ALTURA])

    # C. Faixas Brancas (CORRETO: Centralizadas na nova pista)
    x_faixa = MARGEM_ESQUERDA + (LARGURA_PISTA // 2) - 2 
    for i in range(25):
        pygame.draw.rect(tela, BRANCO, [x_faixa, pista_y1 + i * 100, 5, 50])
        pygame.draw.rect(tela, BRANCO, [x_faixa, pista_y2 + i * 100, 5, 50])

    # D. Barreira de Proteção (Guardi-Rail)
    pygame.draw.rect(tela, PRATA_BARREIRA, [LIMITE_DIREITO_PISTA, 0, 15, ALTURA])

    # E. Painel de Informações (Direita)
    pygame.draw.rect(tela, AZUL_PAINEL, [LIMITE_DIREITO_PISTA + 15, 0, LARGURA - LIMITE_DIREITO_PISTA - 15, ALTURA])

    # F. Desenha os Sprites (Kombi e Moto)
    tela.blit(imagem_kombi, (obs_x, obs_y))
    tela.blit(imagem_moto, (moto_x, moto_y))
    
    # G. PAINEL DE INFORMAÇÕES (TEXTOS)
    x_texto = LIMITE_DIREITO_PISTA + 40
    
    # Renderiza os textos (Texto, Antialias, Cor)
    texto_km_label = fonte_label.render("DISTÂNCIA:", True, BRANCO)
    texto_pontos = fonte_placar.render(f"{int(pontuacao)} km", True, AMARELO_RE)
    
    texto_vidas_label = fonte_label.render("PILOTO:", True, BRANCO)
    texto_vidas = fonte_placar.render("♥ " * vidas, True, (255, 50, 50))

    # Desenha os textos no painel azul
    tela.blit(texto_km_label, (x_texto, 50))
    tela.blit(texto_pontos, (x_texto, 85))
    
    tela.blit(texto_vidas_label, (x_texto, 200))
    tela.blit(texto_vidas, (x_texto, 235))
    
    # G. DEBUG (As linhas verdes de colisão)
    pygame.draw.rect(tela, (0, 255, 0), hitbox_moto, 2)
    pygame.draw.rect(tela, (0, 255, 0), hitbox_obs, 2)

    # Finaliza o frame
    pygame.display.flip()
    
    # DESENHO DE DEBUG (Remova depois!)
    # Desenha linhas verdes ao redor de onde o código "acha" que você está
    pygame.draw.rect(tela, (0, 255, 0), hitbox_moto, 2)
    pygame.draw.rect(tela, (0, 255, 0), hitbox_obs, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()