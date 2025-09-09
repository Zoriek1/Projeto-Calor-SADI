
import numpy as np
from utildades import pedir_acao, mensagem_tempo, obter_resposta, checar_resposta
from utildades import TOL_ABS, VALOR_ERRO, VALOR_DICA, BONUS_ACERTO, TEMPO_ESTAGIO_1

import Fases.Fase1  # importa o módulo da fase 1

estado = {}
vidas = 3
pontuacao = PONTUACAO_INICIAL
inicio = time.time()

sucesso, vidas, pontuacao, estado = Fase1.iniciar(estado, vidas, pontuacao, inicio)

if sucesso:
    print("Fase 1 concluída!")
else:
    print("Você perdeu na fase 1!")
