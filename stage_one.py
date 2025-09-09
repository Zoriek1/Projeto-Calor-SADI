import time
import numpy as np

from utils import (
    INTRO_LONGA,
    mensagem_tempo,
    pedir_acao,
    obter_resposta,
    checar_resposta,
    mostrar_cada_dez_segundos,
    TEMPO_ESTAGIO_1,
    MAX_DICAS,
    PONTUACAO_INICIAL,
    VALOR_DICA,
    VALOR_ERRO,
    BONUS_ACERTO,
)


def primeiro_estagio(estado: dict):
    vidas = 3
    pontuacao = PONTUACAO_INICIAL
    inicio = time.time()
    ultimo_marcador = -1

    print(INTRO_LONGA)
    input("(Pressione Enter para começar.)")

    enigmas = []

    # Fase Temperatura — média dos extremos
    T_menor = np.random.randint(15, 31) * 10   # 150 a 300 K
    T_maior = np.random.randint(50, 71) * 10   # 500 a 700 K
    resp_T = (T_menor + T_maior) / 2
    enigmas.append({
        "nome": "Fase Temperatura",
        "texto": (
            f"Um termômetro quebrado marca {T_menor} K e {T_maior} K.\n"
            "Entre papéis no chão, um trecho sublinhado de um artigo diz: \n"
            '"Nem o universo sobrevive nos extremos. Procure o ponto onde forças opostas se equilibram."'
        ),
        "dicas": [
            "Equilíbrio entre extremos → média aritmética.",
            "Fórmula: T = (T_maior + T_menor) / 2.",
            f"Substitua {T_menor} e {T_maior} (em K)."
        ],
        "resposta": resp_T,
        "unidade": "K",
        "variavel": "temperatura"
    })

    # Fase Pressão — Boyle (dobrar volume)
    P1 = np.random.randint(10, 31) * 10  # atm
    V1 = np.random.randint(10, 31) * 10  # L
    V2 = V1 * 2
    resp_P = (P1 * V1) / V2
    enigmas.append({
        "nome": "Fase Pressão",
        "texto": (
            f"O painel reporta: pressão {P1} atm para {V1} L.\n"
            "Uma anotação desgastada: \"Dobre o espaço e a pressão cede.\""
        ),
        "dicas": [
            "Lei de Boyle: P1V1 = P2V2.",
            f"Use P1={P1} atm, V1={V1} L, V2={V2} L.",
            "Ao dobrar V, a pressão cai pela metade."
        ],
        "resposta": resp_P,
        "unidade": "atm",
        "variavel": "pressao"
    })

    # Fase Volume — Charles (proporcional a T)
    T1 = resp_T
    V1v = np.random.randint(10, 21) * 10  # L
    T2 = T1 + np.random.randint(50, 101)  # K
    resp_V = (V1v * T2) / T1
    enigmas.append({
        "nome": "Fase Volume",
        "texto": (
            f"A temperatura sobe de {T1:.0f} K para {T2:.0f} K.\n"
            f"O volume inicial é {V1v} L. Ajuste o volume final para estabilizar."
        ),
        "dicas": [
            "Lei de Charles: V/T = constante (em P constante).",
            f"V1={V1v} L, T1={T1:.0f} K, T2={T2:.0f} K.",
            "Fórmula: V2 = V1·T2/T1."
        ],
        "resposta": resp_V,
        "unidade": "L",
        "variavel": "volume"
    })

    # Fase n (gás ideal)
    R = 0.082  # atm·L/(mol·K)
    resp_n = (resp_P * resp_V) / (R * resp_T)
    enigmas.append({
        "nome": "Fase Número de Mols",
        "texto": (
            "A voz da Dra. Ignis retorna, impaciente: \n"
            '"Se não lembrar da relação fundamental, eu mesma forçarei a falha."\n'
            "Determine quantos mols há no interior da caldeira."
        ),
        "dicas": [
            "Equação dos gases ideais: n = PV/(RT).",
            f"Use P={resp_P:.2f} atm, V={resp_V:.2f} L, T={resp_T:.2f} K, R={R}.",
            "Unidade final em mol."
        ],
        "resposta": resp_n,
        "unidade": "mol",
        "variavel": "mols"
    })

    # Loop de resolução
    for enigma in enigmas:
        print(f"\n=== {enigma['nome']} ===")
        print(enigma["texto"])
        acertou = False
        dicas = 0

        while not acertou and vidas > 0:
            if mensagem_tempo(inicio, TEMPO_ESTAGIO_1) <= 0:
                return False, pontuacao
            ultimo_marcador = mostrar_cada_dez_segundos(inicio, ultimo_marcador)
            acao = pedir_acao()
            if acao == "1":
                if dicas < MAX_DICAS and dicas < len(enigma["dicas"]):
                    print(enigma["dicas"][dicas])
                    dicas += 1
                    pontuacao -= VALOR_DICA
                else:
                    print("Não há mais pistas para este enigma!")
                continue
            elif acao == "2":
                valor_str = obter_resposta(enigma["unidade"])
            else:
                print("\n[ERRO] Entrada inválida! Digite 1 ou 2.")
                continue

            ok, valor = checar_resposta(valor_str, enigma["resposta"])
            if ok:
                print("\n[SUCESSO] A parametrização está correta. O sistema se estabiliza um pouco mais!")
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

    print("\n[ESTÁGIO 1 CONCLUÍDO] Você estabilizou a caldeira — por enquanto...")
    return True, pontuacao

