import random

def tem_repeticoes_excessivas(lista, max_reps=2):
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
    if letras is None:
        letras = ['A', 'B', 'C', 'D']

    total_letras = len(letras)
    base = qtd // total_letras
    resto = qtd % total_letras

    # Distribuição inicial equilibrada
    gabarito = []
    for letra in letras:
        gabarito.extend([letra] * base)

    # Distribui o restante aleatoriamente entre as letras
    extras = random.sample(letras, resto)
    for letra in extras:
        gabarito.append(letra)

    # Tenta embaralhar sem criar padrões
    for _ in range(1000):
        random.shuffle(gabarito)
        if not tem_repeticoes_excessivas(gabarito, max_reps=max_reps):
            return gabarito

    raise ValueError("Não foi possível gerar um gabarito balanceado e sem repetições excessivas.")
