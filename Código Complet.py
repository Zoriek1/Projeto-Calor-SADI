#09/09/25

import time
import numpy as np

# =====================
# Utilidades e núcleo
# =====================

TOL_ABS = 0.1  # tolerância absoluta para respostas numéricas
MAX_DICAS = 3
TEMPO_ESTAGIO_1 = 400  # s
TEMPO_ESTAGIO_2 = 600  # s
PONTUACAO_INICIAL = 1000
VALOR_ERRO = 100
VALOR_DICA = 200
BONUS_ACERTO = 100
CONVERSAO_ATM_L_PARA_KJ = 0.101325  # 1 atm·L = 0.101325 kJ


def mensagem_tempo(ini, limite):
    restante = int(limite - (time.time() - ini))
    if restante <= 0:
        print("\n[ALARME] O tempo acabou! Sistema em falha crítica.")
        return restante
    if 0 < restante <= 20:
        print(f"\n[AVISO] Falha crítica iminente! Restam apenas {restante} s!")
    return restante


def pedir_acao():
    print("\n1 - Continuar Investigando (Pedir Dica)")
    print("2 - Inserir Valor no Painel")
    return input("Escolha uma opção: ").strip()


def obter_resposta(unidade):
    bruto = input("\nInsira o Valor no Painel: ").strip()
    bruto = bruto.replace(unidade, "").strip().replace(",", ".")
    return bruto


def checar_resposta(valor_str, resp_correta):
    try:
        val = float(valor_str)
    except ValueError:
        print("\n[ERRO] Insira um número válido!")
        return False, None
    if abs(val - resp_correta) <= TOL_ABS:
        return True, val
    return False, val


# =====================
# Narrativa compartilhada
# =====================

INTRO_LONGA = """
O som estridente de sirenes ecoa alto como se estivessem dentro da sua cabeça. Você acorda no chão frio, a visão embaçada. Uma luz vermelha intermitente tinge o laboratório ao seu redor.
Há uma parede de vidro reforçado separando a sala de uma caldeira massiva. O alarme cessa — no lugar, um ruído elétrico. A voz firme da Dra. Ignis toma o ambiente:

"Bem-vindo(a) ao meu laboratório! Sou a Dra. Ignis, a maior mente que a termodinâmica já conheceu. Ignoraram meu trabalho — então, você aprenderá do jeito difícil. A caldeira está perto do ponto crítico. Resolva os enigmas e estabilize o sistema. O relógio está correndo."

As luzes estabilizam, revelando quadros cheios de diagramas, papéis espalhados com trechos de artigos sublinhados e vidros quebrados. O painel de controle abaixo da janela pisca sem parar.
"""


# =====================
# Estágio 1
# =====================

def primeiro_estagio(estado):
    vidas = 3
    pontuacao = PONTUACAO_INICIAL
    inicio = time.time()

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
            "\"Se não lembrar da relação fundamental, eu mesma forçarei a falha.\"\n"
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


# =====================
# Estágio 2
# =====================

def animacao_transicao():
    print("\n[TRANSMISSÃO INTERROMPIDA…]")
    time.sleep(0.6)
    print("[REINICIANDO SISTEMA DE EMERGÊNCIA…]")
    time.sleep(0.6)
    print("[ACESSO PARCIAL RESTAURADO. NOVA AMEAÇA DETECTADA.]")


def segundo_estagio(estado, pontuacao_inicial):
    vidas = 3
    pontuacao = pontuacao_inicial
    inicio = time.time()

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


# =====================
# Execução
# =====================

if __name__ == "__main__":
    estado = {}
    ok1, score = primeiro_estagio(estado)
    if ok1:
        ok2, score = segundo_estagio(estado, score)
        if ok2:
            print(f"\n[SISTEMA ESTÁVEL] Pontuação final: {score}")
        else:
            print(f"\n[FALHA NO ESTÁGIO 2] Pontuação: {score}")
    else:
        print(f"\n[FALHA NO ESTÁGIO 1] Pontuação: {score}")
