from regulador.regulador import regulador_main
from rastreador.rastreador import rastreador_main

def main():
    while True:
        escolha = input("Olá, bem-vindo ao otimizador de ganhos PID!" \
        " O que deseja fazer?\n(R) - Rastreador de função" \
        "\n(D) - Resposta ao degrau\n").upper()

        if escolha == "R":
            rastreador_main()
            break
        if escolha == "D":
            regulador_main()
            break
        else:
            print("Escolha inválida, tente novamente!\n")

if __name__ == "__main__":
    main()
