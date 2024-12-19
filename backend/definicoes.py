import numpy as np
from collections import deque
from utilidades import makeMatrizAdjacencia

# Classe para criar os tabuleiros
class Tabuleiro:
    def __init__(self, **kwargs):  # Inicializador da classe tabuleiro
        if kwargs.get('generate'):
            self.__casas = self.__generateTabuleiro()
            return

        self.__casas = kwargs.get('casas')
        
    def serialize(self):
        serialized = ''

        for linha in self.casas:
            serialized += str(linha).replace(']',
                                             '').replace('[', '').replace(' ', '')

        return serialized

    def getPosPeca(self, peca):
        for i in range(3):
            for j in range(3):
                if self.__casas[i][j] == peca:
                    return (i, j)

    def setPeca(self, peca: int, pos: tuple[int]):
        self.__casas[pos[0]][pos[1]] = peca

    def getPeca(self, pos: tuple[int]):
        return self.__casas[pos[0]][pos[1]]

    @property
    def casas(self):
        return self.__casas

    @casas.setter
    def casas(self, value):
        self.__casas = value

    def __getInvCount(self, arr):
        inv_count = 0
        empty_value = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                    inv_count += 1
        return inv_count

    # Cálculo para verificar se o estado é possível de resolver
    def __isSolvable(self, puzzle):

        inv_count = self.__getInvCount([j for sub in puzzle for j in sub])

        return (inv_count % 2 == 0)

    def __generateTabuleiro(self):

        import random
        import numpy as np

        # Preenche a tabela casas, de 9 posições, com o valor 0
        casas = [0 for _ in range(9)]

        # pega 8 índices aleatórios no intervalo [0, 8]
        indices = random.sample(range(0, 9), 8)

        # coloca os valores de acordo com os índices
        for i, rand_index in zip(range(9), indices):
            casas[rand_index] = i + 1

        casas = np.array([casas[:3], casas[3:6], casas[6:9]]
                         )  # estrutura a matriz

        # Verifica se é um estado possível de resolver; caso não, executa recursivamente até encontrar algum com solução
        if self.__isSolvable(casas):
            return casas
        else:
            return self.__generateTabuleiro()


MATRIZ_ADJACENTES = makeMatrizAdjacencia(3)
POSICAO_CORRETA = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (
    1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1)}
OBJETIVO = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

class Estado:

    def __init__(self, tabuleiro: Tabuleiro):
        self._tabuleiro = tabuleiro

    def __str__(self):
        tabuleiro_str = ""
        for linha in self._tabuleiro.casas:
            tabuleiro_str += str(linha) + '\n'

        return tabuleiro_str

    def calcularSucessores(self):
        possiveis = deque()  # lista de possiveis estados

        vazia = self._tabuleiro.getPosPeca(0)  # obtém a posicao da casa vazia

        # percorre a lista de posições do dicionário no índice i
        for i in MATRIZ_ADJACENTES.get(vazia):
            novo = Tabuleiro()  # Cria uma nova instância de Tabuleiro
            novo.casas = self._tabuleiro.casas.copy()  # Cria cópia do tabuleiro atual
            # O novo estado, na posição da casa vazia, recebe o valor da posicao da casa adjacente
            novo.setPeca(self._tabuleiro.getPeca(i), vazia)
            novo.setPeca(0, i)  # posição adjascente, no tabuleiro, recebe 0
            possiveis.append(Estado(novo))  # Adiciona o novo estado à lista

        return possiveis

    def isGoal(self):
        casas = self._tabuleiro.casas
        return np.array_equal(casas, OBJETIVO)

    def asTuple(self):
        return tuple(tuple(row) for row in self._tabuleiro.casas)

    def imprimirTabuleiro(self):
        for linha in self._tabuleiro.casas:
            print(linha)

    @property
    def anterior(self):
        return self._anterior

# Estado com Heurística


class EstadoH(Estado):

    def __init__(self, tabuleiro: Tabuleiro):
        super().__init__(tabuleiro)

        from collections import deque

        pares_pecas = deque()

        man_dist = 0

        trocas = 0  # Valor de k(node) (COPPIN, 2004)

        # varrer todas as posições da matriz
        for i in range(3):
            for j in range(3):
                pos_peca = (i, j)  # armazena a posição atual em uma tupla

                # armazena o valor da peça atual
                peca = self._tabuleiro.getPeca(pos_peca)

                if peca:  # ignorar casa vazia do tabuleiro

                    objetivo = POSICAO_CORRETA.get(peca)

                    if objetivo == pos_peca:  # se a peça estiver na posição correta
                        continue

                    # distancia de manhattan entre posição atual da peça e a posição objetivo
                    # |x_atual - x_objetivo| +  |y_atual - y_objetivo|
                    man_dist += abs(pos_peca[0]-objetivo[0]) + \
                        abs(pos_peca[1]-objetivo[1])

                    # Cálculo do k(node) (incrementa o valor de trocas)
                    # para cada posição na matriz de adjacentes
                    for k in MATRIZ_ADJACENTES.get(pos_peca):
                        if k in pares_pecas:  # não analisar peças que formam um par de troca entre si
                            continue

                        # guarda o valor da peca adjacente
                        valor = self._tabuleiro.getPeca(k)

                        pos_final_peca_adjacente = POSICAO_CORRETA.get(
                            valor)  # guarda a posição da peça adjacente

                        # se as peças trocadas entre si ficam na posição correta
                        if (k == objetivo) and (pos_final_peca_adjacente == pos_peca):
                            trocas += 1
                            pares_pecas.append(k)
                            pares_pecas.append(pos_peca)
                            break

        # h(node) = h2(node) + 2 * k(node) (COPPIN, 2004)
        self._heuristic = man_dist+2*trocas

    @property
    def h(self):
        return self._heuristic

    def calcularSucessores(self):
        possiveis = deque()  # lista de possiveis estados

        vazia = self._tabuleiro.getPosPeca(0)  # obtém a posicao da casa vazia

        # percorre a lista de posições do dicionário no índice i
        for i in MATRIZ_ADJACENTES.get(vazia):
            novo = Tabuleiro()  # Cria uma nova instância de Tabuleiro
            novo.casas = self._tabuleiro.casas.copy()  # Cria cópia do tabuleiro atual
            # O novo estado, na posição da casa vazia, recebe o valor da posicao da casa adjacente
            novo.setPeca(self._tabuleiro.getPeca(i), vazia)
            novo.setPeca(0, i)  # posição adjascente, no tabuleiro, recebe 0
            possiveis.append(EstadoH(novo))  # Adiciona o novo estado à lista

        return possiveis



