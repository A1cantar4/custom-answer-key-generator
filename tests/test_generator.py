import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from core.generator import gerar_gabarito_balanceado


class TestGerarGabaritoBalanceado(unittest.TestCase):
    def test_tamanho_do_gabarito(self):
        result = gerar_gabarito_balanceado(40, ['A', 'B', 'C', 'D'])
        self.assertEqual(len(result), 40)

    def test_contem_apenas_letras_validas(self):
        letras = ['A', 'B', 'C', 'D']
        result = gerar_gabarito_balanceado(30, letras)
        for letra in result:
            self.assertIn(letra, letras)

    def test_balanceamento_aproximado(self):
        letras = ['A', 'B', 'C', 'D', 'E']
        result = gerar_gabarito_balanceado(50, letras)
        contagem = {letra: result.count(letra) for letra in letras}
        esperado = 50 // len(letras)
        for letra in letras:
            self.assertTrue(abs(contagem[letra] - esperado) <= 1)

    def test_nao_ha_repeticoes_excessivas(self):
        result = gerar_gabarito_balanceado(60, ['A', 'B', 'C', 'D'], max_reps=2)
        count = 1
        for i in range(1, len(result)):
            if result[i] == result[i - 1]:
                count += 1
                self.assertLessEqual(count, 2)
            else:
                count = 1

if __name__ == "__main__":
    unittest.main()
