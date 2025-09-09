import time
import numpy as np

from utils import (
    mensagem_tempo,
    pedir_acao,
    obter_resposta,
    checar_resposta,
    animacao_transicao,
    mostrar_cada_dez_segundos,
    TEMPO_ESTAGIO_2,
    MAX_DICAS,
    VALOR_DICA,
    VALOR_ERRO,
    BONUS_ACERTO,
    CONVERSAO_ATM_L_PARA_KJ,
)


def segundo_estagio(estado: dict, pontuacao_inicial: int):
    vidas = 3
    pontuacao = pontuacao_inicial
    inicio = time.time()
    ultimo_marcador = -1

    animacao_transicao()
    print("\n=== SEGUNDO ESTÁGIO: LABORATÓRIO DE IGNIÇÃO ===")
    print(
        "O motor de ventilação do complexo falha. Sem ajuste, o oxigênio cairá a níveis críticos.\n"
        "Pelos arquivos queimados, você encontra dados de testes e anotações da Dra. Ignis."
    )
    input("(Pressione Enter para continuar.)")

    enigmas = []

    # Fase Q = mcΔT (em kJ)
    gases = {"CO2": 0.844, "Ar": 1.005, "N2": 1.040}  # kJ/kg·K
    gas = np.random.choice(list(gases.keys()))
    c = gases[gas]
    m = np.random.randint(1200, 2501) / 1000  # kg
    T1 = np.random.randint(100, 181)
    T2 = np.random.randint(320, 401)
    dT = T2 - T1
    resp_Q = m * c * dT
    enigmas.append({
        "nome": "Fase Calor Q",
        "texto": (
            f"Dossiê: com {gas}, variações de {T1} °C a {T2} °C exigem energia térmica controlada."
        ),
        "dicas": [
            "Considere ΔT em K = ΔT em °C (variação).",
            "Fórmula: Q = m·c·ΔT (em kJ se c estiver em kJ/kg·K).",
            f"Use m={m:.2f} kg, c={c:.3f} kJ/kg·K, ΔT={dT} K."
        ],
        "resposta": resp_Q,
        "unidade": "kJ",
        "variavel": "Q"
    })

    # Fase Trabalho a pressão constante — converter para kJ
    P_atm = np.random.randint(1, 6)  # atm
    Vi = np.random.uniform(1.0, 5.0)  # L
    Vf = Vi * np.random.uniform(0.70, 0.90)  # compressão
    dV = Vf - Vi  # negativo
    W_atmL = P_atm * dV
    resp_W_kJ = W_atmL * CONVERSAO_ATM_L_PARA_KJ
    enigmas.append({
        "nome": "Fase Trabalho W",
        "texto": (
            f"Registro: a {P_atm} atm, o volume reduziu de {Vi:.2f} L para {Vf:.2f} L (compressão)."
        ),
        "dicas": [
            "Processo isobárico: W = P·(Vf − Vi).",
            f"Calcule em atm·L e converta: 1 atm·L = {CONVERSAO_ATM_L_PARA_KJ} kJ.",
            "Compressão → W negativo."
        ],
        "resposta": resp_W_kJ,
        "unidade": "kJ",
        "variavel": "W"
    })

    # Fase Energia interna ΔU = Q + W (kJ)
    resp_U = resp_Q + resp_W_kJ
    enigmas.append({
        "nome": "Fase Energia Interna ΔU",
        "texto": (
            "Diário: \"Todo calor e trabalho impostos a um sistema reverberam em sua energia interna.\""
        ),
        "dicas": [
            "Primeira Lei: ΔU = Q + W (convencão: W do sistema).",
            "Use os valores de Q e W já determinados (em kJ)."
        ],
        "resposta": resp_U,
        "unidade": "kJ",
        "variavel": "dU"
    })

    for enigma in enigmas:
        print(f"\n=== {enigma['nome']} ===")
        print(enigma["texto"])
        acertou = False
        dicas = 0

        while not acertou and vidas > 0:
            if mensagem_tempo(inicio, TEMPO_ESTAGIO_2) <= 0:
                return False, pontuacao
            ultimo_marcador = mostrar_cada_dez_segundos(inicio, ultimo_marcador)
            acao = pedir_acao()
            if acao == "1":
                if dicas < MAX_DICAS and dicas < len(enigma["dicas"]):
                    print(enigma["dicas"][dicas])
                    dicas += 1
                    pontuacao -= VALOR_DICA
                else:
                    print("Não há mais arquivos disponíveis!")
                continue
            elif acao == "2":
                valor_str = obter_resposta(enigma["unidade"])
            else:
                print("\n[ERRO] Entrada inválida! Digite 1 ou 2.")
                continue

            ok, valor = checar_resposta(valor_str, enigma["resposta"])
            if ok:
                print("\n[SUCESSO] Parâmetro aceito. O sistema segue funcionando!")
                acertou = True
                estado[enigma["variavel"]] = valor
                pontuacao += BONUS_ACERTO
            else:
                print("\n[ERRO] Valor incorreto!")
                vidas -= 1
                pontuacao -= VALOR_ERRO
                print(f"Vidas restantes: {vidas}")

    if vidas <= 0:
        return False, pontuacao

    print("\n[ESCAPE CONCLUÍDO] Você manteve a ventilação e sobreviveu ao segundo desafio!")
    return True, pontuacao

