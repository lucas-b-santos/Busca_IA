
from definicoes import Estado, EstadoH
from utilidades import medir_tempo_e_memoria

def hill(estadoInicial):
    from collections import deque

    fila = deque()     # Fila eficiente
    visitados = set()

    visitados.add(estadoInicial.asTuple())
    fila.append(estadoInicial)

    nos_gerados = 0
    nos_visitados = 0

    atual = None

    while True:
        if not fila:
            return {'estado': atual, 'nos_gerados': nos_gerados, 'nos_visitados': nos_visitados}

        atual = fila.popleft()  # Remove o primeiro elemento da fila

        nos_visitados += 1

        if atual.isGoal():
            return {'estado': atual, 'nos_gerados': nos_gerados, 'nos_visitados': nos_visitados}

        sucessores = atual.calcularSucessores()
        sucessores_ordenados = deque()

        for i in sucessores:
            if i.asTuple() not in visitados:
                nos_gerados += 1
                visitados.add(i.asTuple())  # marca como visitado
                sucessores_ordenados.append(i)  # adiciona na fila

        sucessores_ordenados = sorted(
            sucessores_ordenados, key=lambda x: x.h)  # ordena pela heuristica

        fila.extendleft(reversed(sucessores_ordenados))


def buscaLargura(estadoInicial):
    from collections import deque

    visitados = set()  # lista de nós visitados
    fila = deque()     # Fila eficiente
    # primeiro elemento de visitados é o estado incial
    visitados.add(estadoInicial.asTuple())
    fila.append(estadoInicial)

    nos_gerados = 0
    nos_visitados = 0

    atual = None

    while True:
        if not fila:
            return {'estado': atual, 'nos_gerados': nos_gerados, 'nos_visitados': nos_visitados}

        atual = fila.popleft()  # Remove o primeiro elemento da fila

        nos_visitados += 1

        if atual.isGoal():  # se o atual for o estado objetivo, retorna sucesso
            return {'estado': atual, 'nos_gerados': nos_gerados, 'nos_visitados': nos_visitados}

        # calcula os sucessores do primeiro elemento da fila
        sucessores = atual.calcularSucessores()

        for i in sucessores:
            if i.asTuple() not in visitados:
                nos_gerados += 1
                visitados.add(i.asTuple())  # marca como visitado
                fila.append(i)  # adiciona na fila


def exec_algoritmos(instancia):
    estado_inicial = EstadoH(instancia)
    resultado = medir_tempo_e_memoria(hill, estado_inicial)
    nos_gerados_hill = resultado[0].get('nos_gerados')
    nos_visitados_hill = resultado[0].get('nos_visitados')

    info = resultado[2]

    tempo_exec_hill = info.get('exec_time')
    memoria_hill = info.get('memo_peak')

    estado_inicial = Estado(instancia)
    resultado = medir_tempo_e_memoria(buscaLargura, estado_inicial)
    nos_gerados_largura = resultado[0].get('nos_gerados')
    nos_visitados_largura = resultado[0].get('nos_visitados')

    info = resultado[2]
    
    tempo_exec_largura = info.get('exec_time')
    memoria_largura = info.get('memo_peak')

    info = {
        "nos_gerados_hill": nos_gerados_hill,
        "nos_visitados_hill": nos_visitados_hill,
        "tempo_exec_hill": tempo_exec_hill,
        "memoria_usada_hill": memoria_hill,
        "nos_gerados_largura": nos_gerados_largura,
        "nos_visitados_largura": nos_visitados_largura,
        "tempo_exec_largura": tempo_exec_largura,
        "memoria_usada_largura": memoria_largura,
    }
    
    return info