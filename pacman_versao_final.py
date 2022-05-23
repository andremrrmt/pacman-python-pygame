import pygame
from abc import ABCMeta, abstractmethod
import random

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)

fonte = pygame.font.SysFont("arial", 24, True, False)

amarelo = (255, 255, 0)
preto = (0, 0, 0)
branco = (255, 255, 255)
laranja = (255, 140, 0)
rosa = (255, 15, 192)
ciano = (0, 255, 255)
azul = (0,0, 255)
vermelho = (255, 0, 0)
velocidade = 1
acima = 1
abaixo = 2
direita = 3
esquerda = 4


class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass

class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass


class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac):
        self.pacman = pac
        self.moviveis = []
        self.pontos = 0
        # Estado possíveis: 0-Jogando 1-Pausado 2-GameOver 3-Vitoria
        self.estado = "Jogando"
        self.tamanho = tamanho
        self.vidas = 5
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)

    def pintar_score(self, tela):
        pontos_x = 30 * self.tamanho
        img_pontos = fonte.render("Pontuação: {}".format(self.pontos), True, amarelo)
        vida_img = fonte.render("Vidas: {}".format(self.vidas), True, amarelo)
        tela.blit(img_pontos, (pontos_x, 50))
        tela.blit(vida_img, (pontos_x, 100))

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = self.tamanho // 2
            cor = preto
            if coluna == 2:
                cor = azul
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, amarelo, (x + half, y + half), self.tamanho // 10, 0)

    def pintar(self, tela):
        if self.estado == "Jogando":
            self.pintar_jogando(tela)
        elif self.estado == "Pausado":
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado =="GameOver":
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)
        elif self.estado =="Vitoria":
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)

    def pintar_texto_centro(self, tela, texto):
        texto_img = fonte.render(texto, True, amarelo)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "P A R A B E N S , V O C Ê V E N C E U ! ! !")

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "G A M E  O V E R")

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S A D O")

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_score(tela)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(acima)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(abaixo)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(esquerda)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(direita)
        return direcoes

    def calcular_regras(self):
        if self.estado == "Jogando":
            self.calcular_regras_jogando()
        elif self.estado == "Pausado":
            self.calcular_regras_pausado()
        elif self.estado == "GameOver":
            self.calcular_regras_gameover()

    def calcular_regras_gameover(self):
        pass

    def calcular_regras_pausado(self):
        pass

    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha and movivel.coluna == self.pacman.coluna:
                self.vidas -= 1
                if self.vidas <= 0:
                    self.estado = "GameOver"
                else:
                    self.pacman.linha = 1
                    self.pacman.coluna = 1
            else:
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, Pacman) and self.matriz[lin][col]:
                        self.pontos += 1
                        self.matriz[lin][col] = 0
                        if self.pontos >= 306:
                            self.estado = "Vitoria"
                else:
                    movivel.recusar_movimento(direcoes)


    def processar_eventos(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.estado == "Jogando":
                        self.estado = "Pausado"
                    else:
                        self.estado = "Jogando"


class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.raio = self.tamanho // 2
        self.velocidade_x = 0
        self.velocidae_y = 0
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.abertura = 0
        self.velocidade_abertura = 1

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.velocidade_x
        self.linha_intencao = self.linha + self.velocidae_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def pintar(self, tela, direcao):
        # Desenhar corpo do Pacman
        pygame.draw.circle(tela, amarelo, (self.centro_x, self.centro_y), self.raio, 0)

        self.abertura += self.velocidade_abertura
        if self.abertura > self.raio:
            self.velocidade_abertura = -1
        if self.abertura <= 0:
            self.velocidade_abertura = 1

        if direcao == pygame.K_RIGHT:
            # Boca do Pacman
            canto_boca = (self.centro_x, self.centro_y)
            labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura)
            labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura)
            pontos = [canto_boca, labio_superior, labio_inferior]
            pygame.draw.polygon(tela, preto, pontos, 0)

            # Olho do Pacman
            olho_x = int(self.centro_x + self.raio / 3)
            olho_y = int(self.centro_y - self.raio * 0.7)
            olho_raio = int(self.raio / 10)
            pygame.draw.circle(tela, preto, (olho_x, olho_y), olho_raio, 0)

        elif direcao == pygame.K_LEFT:
            # Boca do Pacman
            canto_boca = (self.centro_x, self.centro_y)
            labio_superior = (self.centro_x - self.raio, self.centro_y - self.abertura)
            labio_inferior = (self.centro_x - self.raio, self.centro_y + self.abertura)
            pontos = [canto_boca, labio_superior, labio_inferior]
            pygame.draw.polygon(tela, preto, pontos, 0)

            # Olho do Pacman
            olho_x = int(self.centro_x - self.raio / 3)
            olho_y = int(self.centro_y - self.raio * 0.70)
            olho_raio = int(self.raio / 10)
            pygame.draw.circle(tela, preto, (olho_x, olho_y), olho_raio, 0)

        elif direcao == pygame.K_UP:
            # Boca do Pacman
            canto_boca = (self.centro_x, self.centro_y)
            labio_superior = (self.centro_x - self.abertura, self.centro_y - self.raio)
            labio_inferior = (self.centro_x + self.abertura, self.centro_y - self.raio)
            pontos = [canto_boca, labio_superior, labio_inferior]
            pygame.draw.polygon(tela, preto, pontos, 0)

            # Olho do Pacman
            olho_x = int(self.centro_x - self.raio * 0.70)
            olho_y = int(self.centro_y - self.raio / 3)
            olho_raio = int(self.raio / 10)
            pygame.draw.circle(tela, preto, (olho_x, olho_y), olho_raio, 0)

        elif direcao == pygame.K_DOWN:
            # Boca do Pacman
            canto_boca = (self.centro_x, self.centro_y)
            labio_superior = (self.centro_x + self.abertura, self.centro_y + self.raio)
            labio_inferior = (self.centro_x - self.abertura, self.centro_y + self.raio)
            pontos = [canto_boca, labio_superior, labio_inferior]
            pygame.draw.polygon(tela, preto, pontos, 0)

            # Olho do Pacman
            olho_x = int(self.centro_x + self.raio * 0.70)
            olho_y = int(self.centro_y + self.raio / 3)
            olho_raio = int(self.raio / 10)
            pygame.draw.circle(tela, preto, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.velocidade_x = velocidade
                elif e.key == pygame.K_LEFT:
                    self.velocidade_x = -velocidade
                elif e.key == pygame.K_UP:
                    self.velocidae_y = -velocidade
                elif e.key == pygame.K_DOWN:
                    self.velocidae_y = velocidade
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.velocidade_x = 0
                    return e.key
                elif e.key == pygame.K_LEFT:
                    self.velocidade_x = 0
                    return e.key
                elif e.key == pygame.K_UP:
                    self.velocidae_y = 0
                    return e.key
                elif e.key == pygame.K_DOWN:
                    self.velocidae_y = 0
                    return e.key

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
         pass


class Fantasma(ElementoJogo):
    def __init__(self, cor, tamanho):
        self.coluna = 13.0
        self.linha = 15.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.velocidade = 1
        self.direcao = abaixo
        self.tamanho = tamanho
        self.cor =cor

    def pintar(self, tela):
        fatia = self.tamanho // 10
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho),
                    (px + fatia, py + fatia * 2),
                    (px + (fatia * 2), py + fatia // 2),
                    (px + (fatia * 4), py),
                    (px + (fatia * 6), py),
                    (px + (fatia * 8), py + fatia // 2),
                    (px + (fatia * 9), py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho),
                    (px + fatia * 9, py + self.tamanho - fatia),
                    (px + fatia * 8, py + self.tamanho),
                    (px + fatia * 7, py + self.tamanho - fatia),
                    (px + fatia * 6, py + self.tamanho),
                    (px + fatia * 5, py + self.tamanho - fatia),
                    (px + fatia * 4, py + self.tamanho),
                    (px + fatia * 3, py + self.tamanho - fatia),
                    (px + fatia * 2, py + self.tamanho),
                    (px + fatia, py + self.tamanho - fatia)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)
        olho_raio_externo = fatia
        olho_raio_interno = fatia // 2

        olho_esquedo_x = int(px + fatia * 3)
        olho_esquerdo_y = int(py + fatia * 2.5)

        olho_direito_x = int(px + fatia * 7)
        olho_direito_y = int(py + fatia * 2.5)

        pygame.draw.circle(tela, branco, (olho_esquedo_x, olho_esquerdo_y), olho_raio_externo, 0)
        pygame.draw.circle(tela, preto, (olho_esquedo_x, olho_esquerdo_y), olho_raio_interno, 0)
        pygame.draw.circle(tela, branco, (olho_direito_x, olho_direito_y), olho_raio_externo, 0)
        pygame.draw.circle(tela, preto, (olho_direito_x, olho_direito_y), olho_raio_interno, 0)


    def calcular_regras(self):
        if self.direcao == acima:
            self.linha_intencao -= self.velocidade
        elif self.direcao == abaixo:
            self.linha_intencao += self.velocidade
        elif self.direcao == esquerda:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == direita:
            self.coluna_intencao += self.velocidade

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def processar_eventos(self, evts):
        pass


if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Fantasma(vermelho, size)
    inky = Fantasma(ciano, size)
    clyde = Fantasma(laranja, size)
    pinky = Fantasma(rosa, size)
    cenario = Cenario(size, pacman)
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)

    direcao = pygame.K_RIGHT

    while True:
        # Calcular Reagras
        pacman.calcular_regras()
        blinky.calcular_regras()
        inky.calcular_regras()
        clyde.calcular_regras()
        pinky.calcular_regras()
        cenario.calcular_regras()

        # Capturar Eventos
        eventos = pygame.event.get()
        aux_direcao = pacman.processar_eventos(eventos)
        if aux_direcao != None:
            direcao = aux_direcao
        cenario.processar_eventos(eventos)

        # Pintar Tela
        screen.fill(preto)
        cenario.pintar(screen)
        pacman.pintar(screen, direcao)
        blinky.pintar(screen)
        inky.pintar(screen)
        clyde.pintar(screen)
        pinky.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

