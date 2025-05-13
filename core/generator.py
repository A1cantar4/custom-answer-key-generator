import random

DEFAULT_LETRAS = ['A', 'B', 'C', 'D']

def tem_repeticoes_excessivas(lista, max_reps=2):
    """
    Verifica se a lista contém mais de `max_reps` repetições consecutivas do mesmo item.
    """
    count = 1
    for i in range(1, len(lista)):
        if lista[i] == lista[i - 1]:
            count += 1
            if count > max_reps:
                return True
        else:
            count = 1
    return False

def gerar_gabarito_balanceado(qtd=40, letras=None, max_reps=2):
    """
    Gera uma lista de gabarito balanceado com as letras fornecidas,
    evitando repetições consecutivas acima de `max_reps`.

    Args:
        qtd (int): número total de questões.
        letras (list): letras a serem distribuídas (ex: ['A', 'B', 'C', 'D']).
        max_reps (int): número máximo de repetições consecutivas permitidas.

    Returns:
        list: gabarito balanceado como lista de letras.
    """
    if letras is None:
        letras = DEFAULT_LETRAS

    total_letras = len(letras)
    base = qtd // total_letras
    resto = qtd % total_letras

    # Distribuição inicial equilibrada
    gabarito = [letra for letra in letras for _ in range(base)]

    # Distribui o restante aleatoriamente entre as letras
    extras = random.sample(letras, resto)
    gabarito.extend(extras)

    # Tenta embaralhar evitando padrões indesejados
    for _ in range(1000):
        random.shuffle(gabarito)
        if not tem_repeticoes_excessivas(gabarito, max_reps=max_reps):
            return gabarito

    raise ValueError("Não foi possível gerar um gabarito balanceado e sem repetições excessivas.")
