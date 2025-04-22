################################################################
###                 M O S T R A   M A Z E                    ###
################################################################
### Neste teste, mostra o labirinto gerado pelo algoritmo de ###
### Aldous-Broder                                            ###
################################################################
### Prof. Filipo Mor, FILIPOMOR.COM                          ###
################################################################

import pygame
import sys
import copy
import random
from random import randint


class ArestasFechadas:
    def __init__(self, superior, inferior, esquerda, direita):
        self.superior = superior
        self.inferior = inferior
        self.esquerda = esquerda
        self.direita = direita


class Celula:
    def __init__(self, arestasFechadas, corPreenchimento, corVisitada, corLinha, corAberta, visitada, aberta):
        self.arestasFechadas = arestasFechadas
        self.corPreenchimento = corPreenchimento
        self.corVisitada = corVisitada
        self.corLinha = corLinha
        self.corAberta = corAberta
        self.visited = visitada
        self.aberta = aberta

    def get_corPreenchimento(self):
        return self.corPreenchimento

    def get_arestasFechadas(self):
        return self.arestasFechadas

    def is_visited(self):
        return self.visited

    def desenhar(self, tela, x, y, aresta):
        # x : coluna
        # y : linha

        # calcula as posicoes de desenho das linhas de cada aresta
        arSuperiorIni = (x, y)
        arSuperiorFim = (x + aresta, y)
        arInferiorIni = (x, y + aresta)
        arInferiorFim = (x + aresta, y + aresta)
        arEsquerdaIni = (x, y)
        arEsquerdaFim = (x, y + aresta)
        arDireitaIni = (x + aresta, y)
        arDireitaFim = (x + aresta, y + aresta)

        # preenche a célula com a cor definida
        if (self.aberta):
            pygame.draw.rect(tela, self.corAberta, (x, y, aresta, aresta))
        else:
            pygame.draw.rect(tela, self.corPreenchimento, (x, y, aresta, aresta))

        pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)

        
        # linha superior
        if (self.arestasFechadas.superior):
            pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        # linha inferior
        if (self.arestasFechadas.inferior):
            pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        # linha esquerda
        if (self.arestasFechadas.esquerda):
            pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        # linha direita
        if (self.arestasFechadas.direita):
            pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)
    
        
        pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)
    

# Classe que implementa o algoritmo de Aldous-Broder
class AldousBroder:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.matriz = Malha(qtLinhas, qtColunas, aresta, celulaPadrao)
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        # self.visitados = []

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def resetaLabirinto(self):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna] = copy.deepcopy(self.celulaPadrao)

    def SorteiaCelulaVizinha(self, linhaCelulaAtual, colunaCelulaAtual):
        encontrou = False
        while (encontrou == False):
            linhaVizinha = linhaCelulaAtual + randint(-1, 1)
            colunaVizinha = colunaCelulaAtual + randint(-1, 1)
            if (
                    linhaVizinha >= 0 and linhaVizinha < self.qtLinhas and colunaVizinha >= 0 and colunaVizinha < self.qtColunas):
                encontrou = True

        return linhaVizinha, colunaVizinha

    def GeraLabirinto(self):

        self.resetaLabirinto()

        unvisitedCells = self.qtLinhas * self.qtColunas
        currentCellLine, currentCellColumn, neighCellLine, neighCellColumn = -1, -1, -1, -1

        # sorteia uma célula qualquer
        currentCellLine = randint(0, self.qtLinhas - 1)
        currentCellColumn = randint(0, self.qtColunas - 1)

        while (unvisitedCells > 0):

            # Sorteia um vizinho qualquer da célula atual
            neighCellLine, neighCellColumn = self.SorteiaCelulaVizinha(currentCellLine, currentCellColumn)

            if (self.matriz[neighCellLine][neighCellColumn].visited == False):
                # incluir aqui a rotina paar abrir uma passagem. Por enquanto, apenas pinta a célula
                self.matriz[currentCellLine][currentCellColumn].aberta = True
                self.matriz[neighCellLine][neighCellColumn].visited = True
                '''
                self.matriz[currentCellLine][currentCellColumn].aberta = True
                self.matriz[neighCellLine][neighCellColumn].aberta     = True
                self.matriz[neighCellLine][neighCellColumn].visited    = True
                self.matriz[neighCellLine][neighCellColumn].corPreenchimento = (0, 255, 0)
                '''
                unvisitedCells -= 1
                # cont += 1

            currentCellLine, currentCellColumn = neighCellLine, neighCellColumn


class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        self.matriz = self.GeraMatriz()

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def __getitem__(self, index):
        return self.matriz[index]

    def __setitem__(self, index, value):
        self.matriz[index] = value

    def __aslist__(self):
        return self.matriz

    def GeraMatriz(self):
        matriz = []
        for i in range(self.qtLinhas):
            linha = []
            for j in range(self.qtColunas):
                #newCell = copy.deepcopy(self.celulaPadrao)
                linha.append(copy.deepcopy(self.celulaPadrao))
            matriz.append(linha)
        return matriz

    def DesenhaLabirinto(self, tela, x, y):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta)

# Função que garante a existência da entrada e da saída no labirinto
# Entrada na posição (1, 0) e saída na posição (N-1, M-1)
def garantir_entrada_saida(matriz, entrada, saida):
    lin_e, col_e = entrada
    lin_s, col_s = saida
    matriz[lin_e][col_e].aberta = True
    matriz[lin_e][col_e].corAberta = (0, 255, 0)  # verde para entrada
    matriz[lin_s][col_s].aberta = True
    matriz[lin_s][col_s].corAberta = (255, 0, 0)  # vermelho para saída


# Algoritmo de resolução por força bruta (backtracking)
def resolver_forca_bruta(matriz, entrada, saida, visitado=None, caminho=None):
    if visitado is None:
        visitado = set()
    if caminho is None:
        caminho = []

    lin, col = entrada
    if entrada == saida:
        caminho.append((lin, col))
        return True

    if entrada in visitado:
        return False

    visitado.add(entrada)
    caminho.append((lin, col))

    # Lista de movimentos possíveis: cima, baixo, esquerda, direita
    vizinhos = [(lin-1, col), (lin+1, col), (lin, col-1), (lin, col+1)]

    for l, c in vizinhos:
        if 0 <= l < len(matriz) and 0 <= c < len(matriz[0]):
            if matriz[l][c].aberta:
                if resolver_forca_bruta(matriz, (l, c), saida, visitado, caminho):
                    return True

    # Backtracking: remove do caminho se não der certo
    caminho.pop()
    return False


from collections import deque

# Algoritmo de resolução por BFS (Breadth-First Search)
def bfs_resolver(matriz, entrada, saida):
    N = len(matriz)
    M = len(matriz[0])
    fila = deque()
    fila.append((entrada, [entrada]))
    visitado = set()

    while fila:
        (lin, col), caminho = fila.popleft()
        if (lin, col) == saida:
            return caminho

        visitado.add((lin, col))

        # Movimentos possíveis: cima, baixo, esquerda, direita
        vizinhos = [(lin-1, col), (lin+1, col), (lin, col-1), (lin, col+1)]

        for l, c in vizinhos:
            if 0 <= l < N and 0 <= c < M:
                if matriz[l][c].aberta and (l, c) not in visitado:
                    fila.append(((l, c), caminho + [(l, c)]))

    return None  # sem solução


def main():
    pygame.init()

    ### definição das cores
    azul = (50, 50, 255)
    preto = (30, 30, 30)       # Cor de fundo - tom mais escuro
    branco = (200, 200, 255)   # Cor da célula aberta - azul claro
    vermelho = (255, 0, 0)
    cinza = (100, 100, 100)    # Cor das arestas

    # Dimensões da janela - maior para melhor visualização 
    [largura, altura] = [900, 700]

    ### Dimensões da malha (matriz NxM)
    N = 30  # número de linhas
    M = 30  # número de colunas
    aresta = 20  # dimensão dos lados das células

    # cores: preenchimento - visitada - linha - aberta
    celulaPadrao = Celula(ArestasFechadas(False, False, False, False), preto, cinza, preto, branco,False, False)
    labirinto = AldousBroder(N, M, aresta, celulaPadrao)
    labirinto.GeraLabirinto()

    # Garante a entrada e saída após gerar o labirinto
    entrada = (1, 0)
    saida = (N-1, M-1)
    garantir_entrada_saida(labirinto.matriz, entrada, saida)


    # Resolve com o algoritmo de força bruta
    caminho_fb = []
    sucesso_fb = resolver_forca_bruta(labirinto.matriz, entrada, saida, caminho=caminho_fb)

    # Se encontrou solução, marca o caminho com uma cor visível (ex: amarelo)
    if sucesso_fb:
        for (lin, col) in caminho_fb:
            labirinto.matriz[lin][col].corAberta = (255, 255, 0)
    else:
        print("Labirinto sem solução (força bruta)")


    # Resolve com BFS
    caminho_bfs = bfs_resolver(labirinto.matriz, entrada, saida)

    if caminho_bfs:
        for (lin, col) in caminho_bfs:
            labirinto.matriz[lin][col].corAberta = (0, 255, 255)  # azul claro para BFS
    else:
        print("Labirinto sem solução (BFS)")




    # Cria a janela
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Mostra Malha')

    ###
    ### Loop principal
    ###
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ### preenche a tela com a cor branca
        tela.fill(branco)

        ### centraliza a grade na janela
        [linha, coluna] = ((tela.get_width() - (M * aresta)) // 2,
                           (tela.get_height() - (N * aresta)) // 2)
        # desenhar_grade(tela, linha, coluna, aresta, N, M, matriz)
        labirinto.matriz.DesenhaLabirinto(tela, linha, coluna)

        ### atualiza a tela
        pygame.display.flip()


if __name__ == '__main__':
    main()
