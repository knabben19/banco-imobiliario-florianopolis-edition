import random
import os
import time

# ==============================
# CONFIGURAÇÕES DO JOGO
# ==============================

DINHEIRO_INICIAL = 3000
VALOR_PASSOU_INICIO = 200

# ==============================
# CLASSE PROPRIEDADE
# ==============================

class Propriedade:
    def __init__(self, nome, preco, aluguel_base):
        self.nome = nome
        self.preco = preco
        self.aluguel_base = aluguel_base
        self.dono = None
        self.casas = 0
        self.hotel = False

    def calcular_aluguel(self):
        if self.hotel:
            return self.aluguel_base * 5
        return self.aluguel_base * (1 + self.casas)

# ==============================
# CLASSE JOGADOR
# ==============================

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.posicao = 0
        self.dinheiro = DINHEIRO_INICIAL
        self.propriedades = []
        self.falido = False

    def mover(self, casas):
        self.posicao += casas
        if self.posicao >= len(tabuleiro):
            self.posicao -= len(tabuleiro)
            self.dinheiro += VALOR_PASSOU_INICIO
            print(f"{self.nome} passou pelo Início e ganhou R${VALOR_PASSOU_INICIO}!")

# ==============================
# TABULEIRO (FLORIANÓPOLIS)
# ==============================

tabuleiro = [
    "Início",
    Propriedade("Centro", 400, 50),
    Propriedade("Trindade", 500, 60),
    "Imposto",
    Propriedade("Campeche", 600, 70),
    Propriedade("Ingleses", 700, 80),
    "Sorte",
    Propriedade("Lagoa da Conceição", 900, 100),
    Propriedade("Jurerê Internacional", 1200, 150),
    Propriedade("Canasvieiras", 800, 90),
    "Vá para o Centro",
]

# ==============================
# FUNÇÕES
# ==============================

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def rolar_dado():
    return random.randint(1, 6)

def turno(jogador):
    if jogador.falido:
        return

    input(f"\n{jogador.nome}, pressione ENTER para rolar o dado...")
    dado = rolar_dado()
    print(f"{jogador.nome} tirou {dado}!")

    jogador.mover(dado)
    casa = tabuleiro[jogador.posicao]

    print(f"{jogador.nome} caiu em {casa if isinstance(casa,str) else casa.nome}")

    if isinstance(casa, Propriedade):
        if casa.dono is None:
            if jogador.dinheiro >= casa.preco:
                comprar = input(f"Deseja comprar {casa.nome} por R${casa.preco}? (s/n): ")
                if comprar.lower() == "s":
                    jogador.dinheiro -= casa.preco
                    casa.dono = jogador
                    jogador.propriedades.append(casa)
                    print(f"{jogador.nome} comprou {casa.nome}!")
        elif casa.dono != jogador:
            aluguel = casa.calcular_aluguel()
            print(f"Você deve pagar R${aluguel} de aluguel para {casa.dono.nome}")
            jogador.dinheiro -= aluguel
            casa.dono.dinheiro += aluguel

            if jogador.dinheiro <= 0:
                jogador.falido = True
                print(f"{jogador.nome} faliu!")

        else:
            # Construir casas/hotel
            if not casa.hotel:
                opcao = input("Deseja construir casa (c) ou hotel (h)? ")
                if opcao.lower() == "c":
                    if jogador.dinheiro >= 200:
                        casa.casas += 1
                        jogador.dinheiro -= 200
                        print("Casa construída!")
                elif opcao.lower() == "h":
                    if jogador.dinheiro >= 500:
                        casa.hotel = True
                        jogador.dinheiro -= 500
                        print("Hotel construído!")

    elif casa == "Imposto":
        jogador.dinheiro -= 200
        print("Você pagou R$200 de imposto!")

    elif casa == "Sorte":
        premio = random.choice([200, -150, 300, -100])
        jogador.dinheiro += premio
        print(f"Carta sorte: você ganhou/perdeu R${premio}")

    elif casa == "Vá para o Centro":
        jogador.posicao = 1
        print("Você foi enviado para o Centro!")

    print(f"Saldo atual: R${jogador.dinheiro}")

# ==============================
# JOGO PRINCIPAL
# ==============================

def jogar():
    limpar()
    print("🏝️ BANCO IMOBILIÁRIO - FLORIANÓPOLIS EDITION 🏝️\n")

    num = int(input("Quantos jogadores? (2-4): "))
    jogadores = []

    for i in range(num):
        nome = input(f"Nome do jogador {i+1}: ")
        jogadores.append(Jogador(nome))

    while True:
        ativos = [j for j in jogadores if not j.falido]

        if len(ativos) == 1:
            print(f"\n🏆 {ativos[0].nome} venceu o jogo!")
            break

        for jogador in jogadores:
            turno(jogador)
            time.sleep(1)

if __name__ == "__main__":
    jogar()