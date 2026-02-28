import pygame
import random

# --- INICIALIZAÇÃO ---
pygame.init()
pygame.mixer.init()

# Carrega as músicas
try:
    pygame.mixer.music.load("music/music2.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("Música não encontrada.")

# Configurações da Janela
LARGURA, ALTURA = 1080, 1300
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meteor 350 - Estrada Infinita")

# Cores
PRETO, BRANCO, CINZA_ASFALTO = (0, 0, 0), (255, 255, 255), (40, 40, 40)
AMARELO_RE = (255, 204, 0) 
VERDE_GRAMA, PRATA_BARREIRA, AZUL_PAINEL = (34, 139, 34), (192, 192, 192), (20, 20, 60)

# --- CONFIGURAÇÕES DE LAYOUT ---
MARGEM_ESQUERDA = 50
LARGURA_PISTA = 600
LIMITE_DIREITO_PISTA = MARGEM_ESQUERDA + LARGURA_PISTA
LARGURA_PAINEL = LARGURA - LIMITE_DIREITO_PISTA - 15

# --- CARREGAMENTO DE ASSETS ---
def carregar_e_girar(caminho, escala):
    try:
        img = pygame.image.load(caminho)
        img = pygame.transform.scale(img, escala)
        return pygame.transform.rotate(img, 90)
    except:
        surf = pygame.Surface(escala)
        surf.fill((200, 0, 0))
        return surf

imagem_moto = carregar_e_girar("assets/moto_com_piloto.png", (200, 120))

# Tipos de Obstáculos
tipos_obstaculos = [
    {"nome": "kombi", "img": carregar_e_girar("assets/kombi.png", (350, 200)), "vel": 5},
    {"nome": "fusca", "img": carregar_e_girar("assets/fusca.png", (280, 180)), "vel": 7},
    {"nome": "caminhao", "img": carregar_e_girar("assets/truck.png", (600, 230)), "vel": 6},
    {"nome": "sport", "img": carregar_e_girar("assets/sport.png", (180, 100)), "vel": 0}
]

# --- VARIÁVEIS INICIAIS ---
velocidade_pista = 10
pista_y1, pista_y2 = 0, -ALTURA 
moto_x, moto_y = MARGEM_ESQUERDA + 250, ALTURA - 300     
velocidade_moto = 8
pontuacao, vidas = 0, 3
game_over = False

# Obstáculo atual
obstaculo_atual = random.choice(tipos_obstaculos)
obs_x = random.randint(MARGEM_ESQUERDA + 50, LIMITE_DIREITO_PISTA - 250)
obs_y = -700

clock = pygame.time.Clock()
pygame.font.init()
fonte_placar = pygame.font.SysFont("Arial", 40, bold=True)
fonte_label = pygame.font.SysFont("Arial", 25)

# --- FUNÇÕES DE DESENHO ---
def desenhar_estrada(p1, p2):
    pygame.draw.rect(tela, VERDE_GRAMA, [0, 0, MARGEM_ESQUERDA, ALTURA])
    pygame.draw.rect(tela, CINZA_ASFALTO, [MARGEM_ESQUERDA, p1, LARGURA_PISTA, ALTURA])
    pygame.draw.rect(tela, CINZA_ASFALTO, [MARGEM_ESQUERDA, p2, LARGURA_PISTA, ALTURA])
    x_faixa = MARGEM_ESQUERDA + (LARGURA_PISTA // 2) - 2
    for i in range(25):
        pygame.draw.rect(tela, BRANCO, [x_faixa, p1 + i * 100, 5, 50])
        pygame.draw.rect(tela, BRANCO, [x_faixa, p2 + i * 100, 5, 50])
    pygame.draw.rect(tela, PRATA_BARREIRA, [LIMITE_DIREITO_PISTA, 0, 15, ALTURA])

def desenhar_painel(pontos, v):
    pygame.draw.rect(tela, AZUL_PAINEL, [LIMITE_DIREITO_PISTA + 15, 0, LARGURA_PAINEL, ALTURA])
    x_t = LIMITE_DIREITO_PISTA + 40
    tela.blit(fonte_label.render("DISTÂNCIA:", True, BRANCO), (x_t, 50))
    tela.blit(fonte_placar.render(f"{int(pontos)} km", True, AMARELO_RE), (x_t, 85))
    tela.blit(fonte_label.render("PILOTO:", True, BRANCO), (x_t, 200))
    tela.blit(fonte_placar.render("♥ " * v, True, (255, 50, 50)), (x_t, 235))

def exibir_game_over(pts):
    overlay = pygame.Surface((LARGURA, ALTURA))
    overlay.set_alpha(180); overlay.fill(PRETO)
    tela.blit(overlay, (0, 0))
    t1 = fonte_placar.render("GAME OVER", True, (255, 50, 50))
    t2 = fonte_label.render(f"Sua Meteor 350 rodou {int(pts)} km!", True, BRANCO)
    t3 = fonte_label.render("Pressione 'R' para Reiniciar", True, AMARELO_RE)
    tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, ALTURA // 2 - 100))
    tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, ALTURA // 2))
    tela.blit(t3, (LARGURA // 2 - t3.get_width() // 2, ALTURA // 2 + 100))

# --- LOOP PRINCIPAL ---
rodando = True
while rodando:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: rodando = False
        if game_over and ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_r:
                vidas, pontuacao, velocidade_pista, game_over = 3, 0, 10, False
                obs_y = -700
                moto_x, moto_y = MARGEM_ESQUERDA + 250, ALTURA - 300
            if ev.key == pygame.K_ESCAPE: rodando = False

    if not game_over:
        # Movimentação da Meteor 350
        # 1. Movimentação da Meteor 350 (Teclas)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and moto_x > MARGEM_ESQUERDA: 
            moto_x -= velocidade_moto
        if teclas[pygame.K_RIGHT] and moto_x < LIMITE_DIREITO_PISTA - 100: 
            moto_x += velocidade_moto
        if teclas[pygame.K_UP] and moto_y > 50: 
            moto_y -= velocidade_moto
        if teclas[pygame.K_DOWN] and moto_y < ALTURA - 200: 
            moto_y += velocidade_moto

        # 2. MOVIMENTAÇÃO DA PISTA (A CORREÇÃO ESTÁ AQUI)
        pista_y1 += velocidade_pista
        pista_y2 += velocidade_pista

        # Lógica de "loop" da estrada infinita
        if pista_y1 >= ALTURA: 
            pista_y1 = pista_y2 - ALTURA
        if pista_y2 >= ALTURA: 
            pista_y2 = pista_y1 - ALTURA
        
        # 3. Pontuação e Dificuldade
        pontuacao += 0.1
        velocidade_pista = 10 + (int(pontuacao) // 100)

        # 4. Lógica do Obstáculo
        if obstaculo_atual["nome"] == "sport":
            # Ela sempre sobe a 5 pixels por frame MAIS RÁPIDO que a pista
            # Independente se a pista está a 10 ou a 50
            obs_y -= 5 
        else:
            # Os outros (Kombi, Fusca, Caminhão) descem com a pista + sua lentidão
            obs_y += obstaculo_atual["vel"] + velocidade_pista 

        # Condição de Reset (Sumiu por cima ou por baixo)
        if obs_y > ALTURA + 200 or obs_y < -900:
            # 1. Sorteia o novo veículo
            obstaculo_atual = random.choice(tipos_obstaculos)
            larg_v = obstaculo_atual["img"].get_width()
            obs_x = random.randint(MARGEM_ESQUERDA + 20, LIMITE_DIREITO_PISTA - larg_v - 20)
            
            # 2. DEFINE O PONTO DE PARTIDA (Crucial!)
            if obstaculo_atual["nome"] == "sport":
                # A moto sport nasce ABAIXO da tela para subir
                obs_y = ALTURA + 100 
            else:
                # Os outros nascem ACIMA da tela para descer
                obs_y = -800
                
        # 4. Lógica de Movimento (Acontece todo frame)
        if obstaculo_atual["nome"] == "sport":
            # A sport ignora a pista e "sobe" 15 pixels fixos
            obs_y -= 15 
        else:
            # Eles descem acompanhando a pista, mas com um "freio" (vel)
            # Se a pista é 10 e a 'vel' do caminhão é 2, ele desce a 8 (mais lento que a pista)
            # Se a 'vel' for 5, ele desce a 5 (ainda mais lento)
            velocidade_final_obstaculo = velocidade_pista - obstaculo_atual["vel"]
            
            # Garantimos que ele nunca suba (mínimo 1 pixel de descida)
            if velocidade_final_obstaculo < 1: velocidade_final_obstaculo = 1
            
            obs_y += velocidade_final_obstaculo 

        # Se for um veículo normal e sumiu por baixo OU se for a moto sport e sumiu por cima
        if (obstaculo_atual["vel"] > 0 and obs_y > ALTURA) or (obstaculo_atual["vel"] < 0 and obs_y < -500):
            
            # Sorteia o próximo veículo
            obstaculo_atual = random.choice(tipos_obstaculos)
            larg_v = obstaculo_atual["img"].get_width()
            obs_x = random.randint(MARGEM_ESQUERDA + 20, LIMITE_DIREITO_PISTA - larg_v - 20)

            # Posicionamento inicial:
            if obstaculo_atual["vel"] < 0:
                # Se for a moto sport, nasce embaixo para ultrapassar
                obs_y = ALTURA + 200
            else:
                # Se forem os outros, nascem em cima
                obs_y = -800

        # Colisão
        rect_moto = imagem_moto.get_rect(topleft=(moto_x, moto_y)).inflate(-60, -40)
        rect_obs = obstaculo_atual["img"].get_rect(topleft=(obs_x, obs_y))
        hitbox_obs = rect_obs.inflate(-40, -60) if obstaculo_atual["nome"] != "caminhao" else rect_obs.inflate(-30, -100)

        if rect_moto.colliderect(hitbox_obs):
            vidas -= 1
            obs_y = -800
            if vidas <= 0: game_over = True

        # Desenho
        desenhar_estrada(pista_y1, pista_y2)
        tela.blit(obstaculo_atual["img"], (obs_x, obs_y))
        tela.blit(imagem_moto, (moto_x, moto_y))
        desenhar_painel(pontuacao, vidas)
    else:
        exibir_game_over(pontuacao)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()