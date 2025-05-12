import random

def tem_repeticoes_excessivas(lista, max_reps=2):
    count = 1
    for i in range(1, len(lista)):
        if lista[i] == lista[i-1]:
            count += 1
            if count > max_reps:
                return True
        else:
            count = 1
    return False

def gerar_gabarito_simples(qtd=40, letras=None, min_pct=10, max_pct=60):
    if letras is None:
        letras = ['A', 'B', 'C', 'D']
    for _ in range(1000):
        letras_embaralhadas = letras[:]
        random.shuffle(letras_embaralhadas)
        percentuais = [random.randint(min_pct, max_pct) for _ in range(len(letras) - 1)]
        restante = 100 - sum(percentuais)
        if min_pct <= restante <= max_pct:
            percentuais.append(restante)
            quantidades = [round(pct * qtd / 100) for pct in percentuais]
            while sum(quantidades) < qtd:
                quantidades[quantidades.index(min(quantidades))] += 1
            while sum(quantidades) > qtd:
                quantidades[quantidades.index(max(quantidades))] -= 1
            gabarito = []
            for letra, quantidade in zip(letras_embaralhadas, quantidades):
                gabarito.extend([letra] * quantidade)
            random.shuffle(gabarito)
            if not tem_repeticoes_excessivas(gabarito, max_reps=2 if len(letras) == 2 else 3):
                return gabarito
    raise ValueError("Não foi possível gerar um gabarito com os parâmetros fornecidos.")