import tkinter as tk
import random

class JogoMagia:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalha Mágica")

        self.modo_pvp = False  # padrão é jogar contra a máquina
        self.turno_jogador = 1

        self.vida_jogador1 = 100
        self.vida_jogador2 = 100
        self.pocoes_jogador1 = 3
        self.pocoes_jogador2 = 3

        self.create_widgets()

    def create_widgets(self):
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(pady=20)

        tk.Label(self.frame_menu, text="Escolha o modo de jogo:", font=("Arial", 12)).pack()

        tk.Button(self.frame_menu, text="Jogar contra a Máquina", width=25, command=self.iniciar_contra_maquina).pack(pady=5)
        tk.Button(self.frame_menu, text="Jogar com um Amigo", width=25, command=self.iniciar_pvp).pack(pady=5)

    def iniciar_contra_maquina(self):
        self.modo_pvp = False
        self.iniciar_jogo()

    def iniciar_pvp(self):
        self.modo_pvp = True
        self.iniciar_jogo()

    def iniciar_jogo(self):
        self.frame_menu.pack_forget()

        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(pady=10)

        self.label_status = tk.Label(self.frame_main, text="Clique em um feitiço para atacar!", font=("Arial", 12))
        self.label_status.pack(pady=10)

        self.label_vidas = tk.Label(self.frame_main, text=self.status_vidas(), font=("Arial", 14))
        self.label_vidas.pack(pady=10)

        self.label_pocoes = tk.Label(self.frame_main, text=self.status_pocoes(), font=("Arial", 12))
        self.label_pocoes.pack(pady=5)

        self.label_turno = tk.Label(self.frame_main, text="", font=("Arial", 12), fg="purple")
        self.label_turno.pack()

        self.frame_botoes = tk.Frame(self.frame_main)
        self.frame_botoes.pack(pady=10)

        # Feitiços disponíveis
        self.feiticos = [
            ("Bola de Fogo (30 dano, Acerto 60%)", lambda: self.jogada(30, 60)),
            ("Raio Congelante (20 dano, Acerto 80%)", lambda: self.jogada(20, 80)),
            ("Chuva de Meteoros (50 dano, 30%)", lambda: self.jogada(50, 30)),
            ("Usar Poção (+20 vida)", self.usar_pocao),
            ("Trovão de Zeus (1000 dano, Acerto 10%)", lambda: self.jogada(1000, 10))
        ]

        self.botoes_jogador = [[], []]  # [jogador1_buttons, jogador2_buttons]

        frame_j1 = tk.Frame(self.frame_botoes)
        frame_j1.pack(side=tk.LEFT, padx=20)
        tk.Label(frame_j1, text="Jogador 1", font=("Arial", 12, "bold")).pack()
        for texto, comando in self.feiticos:
            btn = tk.Button(frame_j1, text=texto, width=30, command=comando)
            btn.pack(pady=2)
            self.botoes_jogador[0].append(btn)

        frame_j2 = tk.Frame(self.frame_botoes)
        frame_j2.pack(side=tk.RIGHT, padx=20)
        tk.Label(frame_j2, text="Jogador 2", font=("Arial", 12, "bold")).pack()
        for texto, comando in self.feiticos:
            btn = tk.Button(frame_j2, text=texto, width=30, command=comando)
            btn.pack(pady=2)
            self.botoes_jogador[1].append(btn)

        self.label_resultado = tk.Label(self.frame_main, text="", font=("Arial", 12), fg="blue")
        self.label_resultado.pack(pady=10)

        self.botao_reiniciar = tk.Button(self.frame_main, text="Reiniciar Jogo", command=self.reiniciar, state=tk.DISABLED)
        self.botao_reiniciar.pack(pady=10)

        self.atualizar_interface()

    def status_vidas(self):
        return f"Jogador 1 Vida: {self.vida_jogador1} | Jogador 2 Vida: {self.vida_jogador2}"

    def status_pocoes(self):
        return f"Poções - Jogador 1: {self.pocoes_jogador1} | Jogador 2: {self.pocoes_jogador2}"

    def jogada(self, dano, chance):
        if self.vida_jogador1 <= 0 or self.vida_jogador2 <= 0:
            return

        resultado = ""

        atacante = self.turno_jogador
        defensor = 2 if atacante == 1 else 1

        if random.randint(1, 100) <= chance:
            if defensor == 2:
                self.vida_jogador2 -= dano
            else:
                self.vida_jogador1 -= dano
            resultado += f"Jogador {atacante} acertou e causou {dano} de dano!\n"
        else:
            resultado += f"Jogador {atacante} errou o feitiço!\n"

        if not self.modo_pvp and defensor == 2:
            resultado += self.ataque_inimigo()

        self.proximo_turno(resultado)

    def usar_pocao(self):
        resultado = ""
        jogador = self.turno_jogador

        if jogador == 1:
            if self.pocoes_jogador1 > 0:
                self.vida_jogador1 = min(100, self.vida_jogador1 + 20)
                self.pocoes_jogador1 -= 1
                resultado = "Jogador 1 usou uma poção e recuperou 20 de vida!\n"
            else:
                resultado = "Jogador 1 não tem mais poções!\n"
        else:
            if self.pocoes_jogador2 > 0:
                self.vida_jogador2 = min(100, self.vida_jogador2 + 20)
                self.pocoes_jogador2 -= 1
                resultado = "Jogador 2 usou uma poção e recuperou 20 de vida!\n"
            else:
                resultado = "Jogador 2 não tem mais poções!\n"

        if not self.modo_pvp and jogador == 1:
            resultado += self.ataque_inimigo()

        self.proximo_turno(resultado)

    def ataque_inimigo(self):
        dano, chance = random.choice([(30, 60), (20, 80), (50, 30)])
        if random.randint(1, 100) <= chance:
            self.vida_jogador1 -= dano
            return f"Inimigo atacou e causou {dano} de dano!"
        else:
            return "O inimigo errou o feitiço!"

    def proximo_turno(self, resultado):
        self.label_resultado.config(text=resultado)
        self.label_vidas.config(text=self.status_vidas())
        self.label_pocoes.config(text=self.status_pocoes())

        if self.vida_jogador1 <= 0 and self.vida_jogador2 <= 0:
            self.label_status.config(text="Empate! Ambos foram derrotados.")
            self.finalizar_jogo()
        elif self.vida_jogador1 <= 0:
            self.label_status.config(text="Jogador 2 venceu!")
            self.finalizar_jogo()
        elif self.vida_jogador2 <= 0:
            self.label_status.config(text="Jogador 1 venceu!")
            self.finalizar_jogo()
        else:
            if self.modo_pvp:
                self.turno_jogador = 2 if self.turno_jogador == 1 else 1
            self.atualizar_interface()

    def atualizar_interface(self):
        # Atualiza turno e habilita/desabilita botões
        if self.modo_pvp:
            self.label_turno.config(text=f"Vez do Jogador {self.turno_jogador}")
            for i in [0, 1]:
                estado = tk.NORMAL if self.turno_jogador == i + 1 else tk.DISABLED
                for btn in self.botoes_jogador[i]:
                    btn.config(state=estado)
        else:
            self.label_turno.config(text="")
            for btn in self.botoes_jogador[0]:
                btn.config(state=tk.NORMAL)
            for btn in self.botoes_jogador[1]:
                btn.config(state=tk.DISABLED)

    def finalizar_jogo(self):
        for grupo in self.botoes_jogador:
            for btn in grupo:
                btn.config(state=tk.DISABLED)
        self.botao_reiniciar.config(state=tk.NORMAL)

    def reiniciar(self):
        self.vida_jogador1 = 100
        self.vida_jogador2 = 100
        self.pocoes_jogador1 = 3
        self.pocoes_jogador2 = 3
        self.turno_jogador = 1
        self.label_resultado.config(text="")
        self.label_status.config(text="Novo jogo iniciado!")
        self.botao_reiniciar.config(state=tk.DISABLED)
        self.atualizar_interface()
        self.label_vidas.config(text=self.status_vidas())
        self.label_pocoes.config(text=self.status_pocoes())

# Execução do jogo
root = tk.Tk()
app = JogoMagia(root)
root.mainloop()
