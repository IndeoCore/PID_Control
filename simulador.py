from logica_controle import cria_funcao_da_planta, determina_pesos, plot_system
from gen_alg import cria_populacao_inicial, algoritmo_genetico

def main():
    print("--- Otimizador de ganhos PID com Algoritmo Genético ---")

    planta = cria_funcao_da_planta()

    pesos = determina_pesos()

    tamanho_populacao = 100
    populacao_inicial = cria_populacao_inicial(tamanho_populacao)

    print("\nIniciando o processo de otimização")

    melhor_individuo = algoritmo_genetico(planta, pesos, populacao_inicial)

    if melhor_individuo:
        print("\n--- Resultados da otimização ---")
        Kp_ot, Ki_ot, Kd_ot = melhor_individuo
        print("--- Ganhos ótimos encontrados ---")
        print(f"Kp = {Kp_ot:.4f}")
        print(f"Kd = {Kd_ot:.4f}")
        print(f"Ki = {Ki_ot:.4f}")
        plot_system(planta, melhor_individuo)
    else:
        print("\nNão foi possível encontrar uma solução.")
    
if __name__ == "__main__":
    main()
