import time


# =====================
# Constantes compartilhadas
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
# Utilidades de interação e tempo
# =====================

def mensagem_tempo(inicio_epoca: float, limite_segundos: int) -> int:
    restante = int(limite_segundos - (time.time() - inicio_epoca))
    if restante <= 0:
        print("\n[ALARME] O tempo acabou! Sistema em falha crítica.")
        return restante
    if 0 < restante <= 20:
        print(f"\n[AVISO] Falha crítica iminente! Restam apenas {restante} s!")
    return restante


def pedir_acao() -> str:
    print("\n1 - Continuar Investigando (Pedir Dica)")
    print("2 - Inserir Valor no Painel")
    return input("Escolha uma opção: ").strip()


def obter_resposta(unidade: str) -> str:
    bruto = input("\nInsira o Valor no Painel: ").strip()
    bruto = bruto.replace(unidade, "").strip().replace(",", ".")
    return bruto


def checar_resposta(valor_str: str, resp_correta: float):
    try:
        val = float(valor_str)
    except ValueError:
        print("\n[ERRO] Insira um número válido!")
        return False, None
    if abs(val - resp_correta) <= TOL_ABS:
        return True, val
    return False, val


def animacao_transicao():
    print("\n[TRANSMISSÃO INTERROMPIDA…]")
    time.sleep(0.6)
    print("[REINICIANDO SISTEMA DE EMERGÊNCIA…]")
    time.sleep(0.6)
    print("[ACESSO PARCIAL RESTAURADO. NOVA AMEAÇA DETECTADA.]")


def mostrar_cada_dez_segundos(inicio_epoca: float, ultimo_marcador: int) -> int:
    """Mostra na tela a cada 10 s decorridos desde o início.

    Retorna o marcador atual (inteiro de 10 s) para ser mantido pelo chamador.
    """
    decorrido = int(time.time() - inicio_epoca)
    marcador_atual = decorrido // 10
    if marcador_atual > ultimo_marcador and marcador_atual > 0:
        print(f"[TEMPO] {marcador_atual * 10} s decorridos.")
    return marcador_atual

