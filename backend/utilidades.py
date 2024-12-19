
def medir_tempo_e_memoria(func, *args, **kwargs):

    import time
    import tracemalloc

    tracemalloc.start()  # Inicia a medição de memória
    start_time = time.perf_counter()  # Inicia a medição de tempo

    # Executa a função
    result = func(*args, **kwargs)

    # Finaliza a medição de tempo
    end_time = time.perf_counter()
    # Obtém o uso de memória
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Exibe resultados
    dados = f"Tempo de execução: {end_time - start_time:.6f} segundos\nMemória usada: {current / 1024:.2f} KB\nMemória de pico: {peak / 1024:.2f} KB"

    info = {'exec_time': end_time - start_time,
            'used_memo': current / 1024, 'memo_peak': peak / 1024}

    return (result, dados, info)

def getInvCount(arr):
    inv_count = 0
    empty_value = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count

# Cálculo para verificar se o estado é possível de resolver
def isSolvable(puzzle):

    inv_count = getInvCount([j for sub in puzzle for j in sub])

    return (inv_count % 2 == 0)


def makeMatrizAdjacencia(n):
    # Tabela de adjacência
    adjacencia = {}

    # Gerar posições e calcular adjacências
    for i in range(n):
        for j in range(n):
            pos = (i, j)
            adjacentes = []
            # Direções: cima, baixo, esquerda, direita
            direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in direcoes:
                x, y = i + dx, j + dy
                if 0 <= x < n and 0 <= y < n:  # Dentro dos limites
                    adjacentes.append((x, y))
            adjacencia[pos] = adjacentes

    return adjacencia