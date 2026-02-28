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

# --- LOOP PRINCIPAL ---
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # 1. MOVIMENTAÇÃO DA MOTO
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and moto_x > MARGEM_X: 
        moto_x -= velocidade_moto
    if teclas[pygame.K_RIGHT] and moto_x < (MARGEM_X + LARGURA_PISTA - 100): # 100 é a largura da moto
        moto_x += velocidade_moto
    if teclas[pygame.K_UP] and moto_y > 50: moto_y -= velocidade_moto
    if teclas[pygame.K_DOWN] and moto_y < ALTURA - 200: moto_y += velocidade_moto

    # 2. MOVIMENTAÇÃO DA ESTRADA
    pista_y1 += velocidade_pista
    pista_y2 += velocidade_pista
    
    if pista_y1 >= ALTURA: pista_y1 = pista_y2 - ALTURA
    if pista_y2 >= ALTURA: pista_y2 = pista_y1 - ALTURA

    # 3. LÓGICA DO OBSTÁCULO
    obs_y += obs_velocidade + velocidade_pista 
    if obs_y > ALTURA:
        obs_y = -500
        obs_x = random.randint(MARGEM_X + 20, MARGEM_X + LARGURA_PISTA - 160)

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
        print("POW! Bateu a Meteor!")
        moto_x, moto_y = LARGURA // 2 - 50, ALTURA - 300
        obs_y = -500 # Reseta a Kombi bem longe para não bater de novo na volta

    # 5. DESENHO (A ORDEM IMPORTA!)
    
    # A. Limpa a tela
    tela.fill(PRETO) 

    # B. Desenha o Asfalto (Ocupando a maior parte da tela)
    # Largura da pista desejada
    LARGURA_PISTA = 550 
    # Margem esquerda para centralizar: (1080 - 550) // 2 = 265
    MARGEM_X = 265
    #Desenha o Asfalto Centralizado
    pygame.draw.rect(tela, CINZA_ASFALTO, [MARGEM_X, pista_y1, LARGURA_PISTA, ALTURA])
    pygame.draw.rect(tela, CINZA_ASFALTO, [MARGEM_X, pista_y2, LARGURA_PISTA, ALTURA])

    # C. Desenha as Faixas Brancas (AGORA CORRETAMENTE)
    # i * 100 cria um espaçamento maior, range(20) cobre 2000px (mais que os 1300 da tela)
    for i in range(20):
        # Faixas da Pista 1
        pygame.draw.rect(tela, BRANCO, [LARGURA//2 - 5, pista_y1 + i * 100, 5, 50])
        # Faixas da Pista 2
        pygame.draw.rect(tela, BRANCO, [LARGURA//2 - 5, pista_y2 + i * 100, 5, 50])

    # D. Desenha o Obstáculo
    tela.blit(imagem_kombi, (obs_x, obs_y))

    # E. Desenha a Moto
    tela.blit(imagem_moto, (moto_x, moto_y))
    
    # DESENHO DE DEBUG (Remova depois!)
    # Desenha linhas verdes ao redor de onde o código "acha" que você está
    pygame.draw.rect(tela, (0, 255, 0), hitbox_moto, 2)
    pygame.draw.rect(tela, (0, 255, 0), hitbox_obs, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()