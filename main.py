from utils import PONTUACAO_INICIAL
from stage_one import primeiro_estagio
from stage_two import segundo_estagio


def main():
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


if __name__ == "__main__":
    main()

