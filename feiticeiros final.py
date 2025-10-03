# Arquivo: jogo_batalha_pygame_final.py
import pygame
import random
import os

# --- Classes para Sprites ---

class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=pos)
        self.max_health = 100
        self.health = 100
        self.max_mana = 100
        self.mana = 100
        self.potions = 3
        self.is_defending = False
        self.initial_pos = self.rect.copy()

    def update(self):
        if self.mana < self.max_mana:
            self.mana += 0.2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=pos)
        self.max_health = 100
        self.health = 100
        self.initial_pos = self.rect.copy()

    def update(self):
        pass

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, pos, target, speed, damage, chance):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.target = target
        self.speed = speed
        self.damage = damage
        self.chance = chance
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2)**0.5)
        self.vel_x = (dx / dist) * self.speed
        self.vel_y = (dy / dist) * self.speed

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if not tela_rect.colliderect(self.rect): self.kill()

class DamageText(pygame.sprite.Sprite):
    def __init__(self, text, color, center_pos):
        super().__init__()
        self.image = fonte_dano.render(str(text), True, color)
        self.rect = self.image.get_rect(center=center_pos)
        self.life_timer = 0
        self.speed_y = -2

    def update(self):
        self.rect.y += self.speed_y
        self.life_timer += 1
        if self.life_timer > 60: self.kill()

class Effect(pygame.sprite.Sprite):
    def __init__(self, image, center_pos, life_time=60):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center_pos)
        self.life_timer = 0
        self.life_time = life_time
    def update(self):
        self.life_timer += 1
        if self.life_timer > self.life_time: self.kill()

# --- InicializaÃ§Ã£o do Pygame ---
pygame.init()
LARGURA, ALTURA = 1024, 768
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
tela_rect = tela.get_rect()
pygame.display.set_caption("Batalha MÃ¡gica!")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Consolas", 20, bold=True)
fonte_dano = pygame.font.SysFont("Impact", 30)
fonte_titulo = pygame.font.SysFont("Impact", 60)
fonte_log = pygame.font.SysFont("Consolas", 24)

# --- Cores ---
BRANCO=(255,255,255); PRETO=(0,0,0); VERDE=(0,255,0); VERMELHO=(255,0,0); AZUL=(0,180,255); CINZA=(50,50,50); AZUL_UI=(20,30,60)

# --- FunÃ§Ãµes de Carregamento de Imagem ---
def carregar_imagem_proporcional(filename, height):
    """Carrega e redimensiona uma imagem mantendo a proporÃ§Ã£o."""
    path = os.path.join(SPRITES_PATH, filename)
    image = pygame.image.load(path).convert_alpha()
    proporcao = image.get_width() / image.get_height()
    new_height = height
    new_width = int(new_height * proporcao)
    return pygame.transform.scale(image, (new_width, new_height))

# --- Carregando Assets ---
ASSETS_PATH = os.path.join("assets")
SPRITES_PATH = os.path.join(ASSETS_PATH, "sprites")

try:
    background_original = pygame.image.load(os.path.join(SPRITES_PATH, "background.png")).convert()
    background = pygame.transform.scale(background_original, (tela_rect.width, tela_rect.height))
    
    player_img = carregar_imagem_proporcional("mago_statico.png", 300)
    enemy_img = carregar_imagem_proporcional("inimigo_statico.png", 300)
    bola_fogo_img = carregar_imagem_proporcional("bola_de_fogo_statico.png", 60)
    raio_img = carregar_imagem_proporcional("raio_congelante_statico.png", 60)
    meteoro_img = carregar_imagem_proporcional("meteoro_statico.png", 60)
    cura_img = carregar_imagem_proporcional("efeito_cura_statico.png", 100)
    escudo_img = carregar_imagem_proporcional("escudo_statico.png", 100)
    trovao_img = carregar_imagem_proporcional("trovao_statico.png", 60)
    
except pygame.error as e:
    print(f"ERRO: Asset nÃ£o encontrado! ({e})")
    print("Certifique-se de que a estrutura de pastas e os nomes dos arquivos estÃ£o corretos.")
    exit()

# --- DicionÃ¡rio de FeitiÃ§os ---
FEITICOS_JOGADOR = {
    pygame.K_1: {"nome": "Bola de Fogo", "image": bola_fogo_img, "dano": 30, "chance": 60, "tipo": "ataque", "velocidade": 8},
    pygame.K_2: {"nome": "Raio Congelante", "image": raio_img, "dano": 20, "chance": 80, "tipo": "ataque", "velocidade": 12},
    pygame.K_3: {"nome": "Chuva de Meteoros", "image": meteoro_img, "dano": 50, "chance": 30, "tipo": "ataque", "velocidade": 6},
    pygame.K_4: {"nome": "Usar PoÃ§Ã£o de Cura", "image": cura_img, "cura": 20, "tipo": "suporte"},
    pygame.K_5: {"nome": "Defesa", "image": escudo_img, "tipo": "defesa"},
    pygame.K_6: {"nome": "TrovÃ£o de Zeus", "image": trovao_img, "dano": 1000, "chance": 10, "tipo": "ataque", "velocidade": 20},
}
FEITICOS_INIMIGO = {
    "padrao": {"nome": "FeitiÃ§o do Inimigo", "image": raio_img, "dano": 20, "chance": 75, "velocidade": 6}
}

# --- FunÃ§Ãµes de Jogo ---
def iniciar_jogo():
    global all_sprites, player_projectiles, enemy_projectiles, damage_texts, effects, player, enemy, turno, estado_jogo, screen_shake, event_log
    
    all_sprites.empty()
    player_projectiles.empty()
    enemy_projectiles.empty()
    damage_texts.empty()
    effects.empty()
    
    player = Player(player_img, (tela_rect.width * 0.25, tela_rect.height - 150))
    enemy = Enemy(enemy_img, (tela_rect.width * 0.75, tela_rect.height - 150))
    all_sprites.add(player, enemy)
    
    turno = "JOGADOR"
    estado_jogo = "BATALHA"
    screen_shake = 0
    event_log = "A batalha comeÃ§ou!"

def desenhar_barra(x, y, valor_atual, valor_max, cor):
    proporcao = max(0, valor_atual / valor_max)
    pygame.draw.rect(tela, CINZA, (x, y, 200, 20))
    pygame.draw.rect(tela, cor, (x, y, 200 * proporcao, 20))

def desenhar_botao(text, x, y, width, height, color, text_color):
    botao_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(tela, color, botao_rect, border_radius=10)
    
    texto_surf = fonte_dano.render(text, True, text_color)
    texto_rect = texto_surf.get_rect(center=botao_rect.center)
    tela.blit(texto_surf, texto_rect)
    return botao_rect

# --- Grupos de Sprites ---
all_sprites = pygame.sprite.Group()
player_projectiles = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()
damage_texts = pygame.sprite.Group()
effects = pygame.sprite.Group()

# --- VariÃ¡veis de Jogo ---
turno = "JOGADOR"
estado_jogo = "MENU"
screen_shake = 0
player = None
enemy = None
event_log = ""
turn_wait_timer = 0

# --- Loop Principal ---
rodando = True
while rodando:
    # --- Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_jogo == "MENU":
                start_button_rect = desenhar_botao("INICIAR", tela_rect.centerx - 100, tela_rect.centery + 50, 200, 50, AZUL_UI, BRANCO)
                if start_button_rect.collidepoint(evento.pos):
                    iniciar_jogo()
            elif estado_jogo in ["VITORIA", "DERROTA"]:
                restart_button_rect = desenhar_botao("JOGAR NOVAMENTE", tela_rect.centerx - 150, tela_rect.centery + 100, 300, 60, AZUL_UI, BRANCO)
                if restart_button_rect.collidepoint(evento.pos):
                    iniciar_jogo()

        if evento.type == pygame.KEYDOWN and turno == "JOGADOR" and estado_jogo == "BATALHA":
            player.is_defending = False
            if evento.key in FEITICOS_JOGADOR:
                feitico = FEITICOS_JOGADOR[evento.key]
                if feitico["tipo"] == "ataque":
                    proj = Projectile(feitico["image"], player.rect.center, enemy, feitico["velocidade"], feitico["dano"], feitico["chance"])
                    all_sprites.add(proj); player_projectiles.add(proj)
                    event_log = f"VocÃª lanÃ§ou {feitico['nome']}!"
                    turno = "ANIMACAO_JOGADOR"
                elif feitico["tipo"] == "suporte":
                    if player.potions > 0:
                        player.health = min(player.max_health, player.health + feitico["cura"])
                        player.potions -= 1
                        efeito = Effect(feitico["image"], player.rect.center)
                        all_sprites.add(efeito); effects.add(efeito)
                        dano_texto = DamageText(f'+{feitico["cura"]}', VERDE, player.rect.midtop)
                        all_sprites.add(dano_texto); damage_texts.add(dano_texto)
                        event_log = "VocÃª usou uma poÃ§Ã£o e se curou."
                        turno = "ESPERA_INIMIGO"
                    else:
                        event_log = "VocÃª nÃ£o tem poÃ§Ãµes!"
                elif feitico["tipo"] == "defesa":
                    player.is_defending = True
                    efeito = Effect(feitico["image"], player.rect.center, life_time=120)
                    all_sprites.add(efeito); effects.add(efeito)
                    event_log = "VocÃª se defendeu!"
                    turno = "ESPERA_INIMIGO"

    # --- AtualizaÃ§Ãµes ---
    if estado_jogo == "BATALHA":
        all_sprites.update()
        
        # LÃ³gica de colisÃ£o do jogador
        colisoes_inimigo = pygame.sprite.spritecollide(enemy, player_projectiles, True)
        if colisoes_inimigo:
            for colisao in colisoes_inimigo:
                if random.randint(0, 100) <= colisao.chance:
                    dano = colisao.damage + random.randint(-5, 5)
                    enemy.health -= dano
                    dano_texto = DamageText(dano, BRANCO, enemy.rect.midtop)
                    screen_shake = 20
                    event_log = f"VocÃª acertou o inimigo! Ele recebeu {dano} de dano."
                else:
                    dano_texto = DamageText("ERROU!", BRANCO, enemy.rect.midtop)
                    event_log = "Seu feitiÃ§o falhou!"
                all_sprites.add(dano_texto); damage_texts.add(dano_texto)
                if enemy.health <= 0: estado_jogo = "VITORIA"
                turno = "ESPERA_INIMIGO"

        # LÃ³gica de colisÃ£o do inimigo
        colisoes_jogador = pygame.sprite.spritecollide(player, enemy_projectiles, True)
        if colisoes_jogador:
            for colisao in colisoes_jogador:
                if random.randint(0, 100) <= colisao.chance:
                    dano_base = colisao.damage + random.randint(-5, 5)
                    dano_final = dano_base
                    if player.is_defending:
                        dano_final = dano_base * 0.5
                        event_log = f"Ataque inimigo bloqueado! VocÃª recebeu {int(dano_final)} de dano."
                    else:
                        event_log = f"VocÃª recebeu {int(dano_final)} de dano."
                    player.health -= dano_final
                    dano_texto = DamageText(int(dano_final), VERMELHO, player.rect.midtop)
                    screen_shake = 15
                else:
                    dano_texto = DamageText("ERROU!", VERMELHO, player.rect.midtop)
                    event_log = "O ataque do inimigo falhou!"
                all_sprites.add(dano_texto); damage_texts.add(dano_texto)
                if player.health <= 0: estado_jogo = "DERROTA"
                turno = "ESPERA_JOGADOR"

        # LÃ³gica de transiÃ§Ã£o de turnos
        if turno == "ANIMACAO_JOGADOR" and not player_projectiles and not effects:
            turno = "ESPERA_INIMIGO"
        
        if turno == "ESPERA_INIMIGO":
            turn_wait_timer += 1
            if turn_wait_timer >= 60: # Espera 1 segundo (60 frames)
                turn_wait_timer = 0
                if estado_jogo == "BATALHA":
                    turno = "INIMIGO"

        if turno == "ESPERA_JOGADOR":
            turn_wait_timer += 1
            if turn_wait_timer >= 60: # Espera 1 segundo (60 frames)
                turn_wait_timer = 0
                if estado_jogo == "BATALHA":
                    turno = "JOGADOR"
        
        if turno == "INIMIGO" and estado_jogo == "BATALHA":
            pygame.time.wait(500)
            feitico_inimigo = FEITICOS_INIMIGO["padrao"]
            proj_inimigo = Projectile(feitico_inimigo["image"], enemy.rect.center, player, feitico_inimigo["velocidade"], feitico_inimigo["dano"], feitico_inimigo["chance"])
            all_sprites.add(proj_inimigo); enemy_projectiles.add(proj_inimigo)
            event_log = "O inimigo estÃ¡ atacando!"
            turno = "ANIMACAO_INIMIGO"
        
        if turno == "ANIMACAO_INIMIGO" and not enemy_projectiles:
            turno = "ESPERA_JOGADOR"
    # --- Desenho ---
    tela.blit(background, (0, 0))
    offset = [0, 0]
    if screen_shake > 0:
        screen_shake -= 1
        offset[0] = random.randint(-5, 5)
        offset[1] = random.randint(-5, 5)

    if estado_jogo == "MENU":
        titulo_surf = fonte_titulo.render("Batalha MÃ¡gica!", True, BRANCO)
        titulo_rect = titulo_surf.get_rect(center=(tela_rect.centerx, tela_rect.centery - 50))
        tela.blit(titulo_surf, titulo_rect)
        desenhar_botao("INICIAR", tela_rect.centerx - 100, tela_rect.centery + 50, 200, 50, AZUL_UI, BRANCO)

    elif estado_jogo == "BATALHA":
        for sprite in all_sprites:
            tela.blit(sprite.image, (sprite.rect.x + offset[0], sprite.rect.y + offset[1]))
        
        desenhar_barra(player.initial_pos.centerx - 100, player.initial_pos.y - 40, player.health, player.max_health, VERDE)
        desenhar_barra(player.initial_pos.centerx - 100, player.initial_pos.y - 20, player.mana, player.max_mana, AZUL)
        desenhar_barra(enemy.initial_pos.centerx - 100, enemy.initial_pos.y - 40, enemy.health, enemy.max_health, VERMELHO)
        
        partes_msg = []
        for key_code, feitico in FEITICOS_JOGADOR.items():
            tecla_str = pygame.key.name(key_code).upper()
            if feitico["nome"] == "Usar PoÃ§Ã£o de Cura":
                partes_msg.append(f"[{tecla_str}] PoÃ§Ã£o({player.potions})")
            elif feitico["tipo"] == "defesa":
                partes_msg.append(f"[{tecla_str}] Defesa")
            else:
                partes_msg.append(f"[{tecla_str}] {feitico['nome']} ({feitico['chance']}%)")
        
        msg_linha1 = "  ".join(partes_msg[:3])
        msg_linha2 = "  ".join(partes_msg[3:])
        tela.blit(fonte.render(msg_linha1, True, BRANCO), (20, 20))
        tela.blit(fonte.render(msg_linha2, True, BRANCO), (20, 45))

        log_rect = pygame.Rect(10, tela_rect.height - 50, tela_rect.width - 20, 40)
        pygame.draw.rect(tela, AZUL_UI, log_rect, border_radius=10)
        log_text = fonte_log.render(event_log, True, BRANCO)
        log_text_rect = log_text.get_rect(center=log_rect.center)
        tela.blit(log_text, log_text_rect)

    elif estado_jogo in ["VITORIA", "DERROTA"]:
        msg = "VITORIA!" if estado_jogo == "VITORIA" else "DERROTA..."
        msg_surf = fonte_titulo.render(msg, True, VERDE if estado_jogo == "VITORIA" else VERMELHO)
        msg_rect = msg_surf.get_rect(center=(tela_rect.centerx, tela_rect.centery - 50))
        tela.blit(msg_surf, msg_rect)
        desenhar_botao("JOGAR NOVAMENTE", tela_rect.centerx - 150, tela_rect.centery + 100, 300, 60, AZUL_UI, BRANCO)
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()