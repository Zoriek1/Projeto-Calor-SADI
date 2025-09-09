import numpy as np
import time
from utils import pedir_acao, mensagem_tempo, obter_resposta, checar_resposta  # funções comuns

def fase_temperatura(estado, vidas, pontuacao, inicio):
    T_menor = np.random.randint(15, 31) * 10
    T_maior = np.random.randint(50, 71) * 10
    resp_T = (T_menor + T_maior) / 2

    enigma = {
        "nome": "Fase Temperatura",
        "texto": (
            f"Um termômetro quebrado marca {T_menor} K e {T_maior} K.\n"
            "Entre papéis no chão, um trecho sublinhado de um artigo diz: \n"
            "\"Nem o universo sobrevive nos extremos. Procure o ponto onde forças opostas se equilibram.\""
        ),
        "dicas": [
            "Equilíbrio entre extremos → média aritmética.",
            "Fórmula: T = (T_maior + T_menor) / 2.",
            f"Substitua {T_menor} e {T_maior} (em K)."
        ],
        "resposta": resp_T,
        "unidade": "K",
        "variavel": "temperatura"
    }

    acertou = False
    dicas = 0
    while not acertou and vidas > 0:
        if mensagem_tempo(inicio, TEMPO_ESTAGIO_1) <= 0:
            return False, vidas, pontuacao, estado

        print(f"\n=== {enigma['nome']} ===")
        print(enigma["texto"])
        acao = pedir_acao()

        if acao == "1":
            if dicas < len(enigma["dicas"]):
                print(enigma["dicas"][dicas])
                dicas += 1
                pontuacao -= VALOR_DICA
            else:
                print("Não há mais pistas para este enigma!")
        elif acao == "2":
            valor_str = obter_resposta(enigma["unidade"])
            ok, valor = checar_resposta(valor_str, enigma["resposta"])
            if ok:
                print("\n[SUCESSO] Parâmetro correto!")
                acertou = True
                estado[enigma["variavel"]] = valor
                pontuacao += BONUS_ACERTO
            else:
                print("\n[ERRO] Valor incorreto!")
                vidas -= 1
                pontuacao -= VALOR_ERRO
                print(f"Vidas restantes: {vidas}")
        else:
            print("\n[ERRO] Entrada inválida! Digite 1 ou 2.")

    return True, vidas, pontuacao, estado
