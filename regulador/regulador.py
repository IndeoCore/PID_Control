from regulador.logica_controle_regulador import cria_funcao_da_planta, determina_pesos, plot_system
from regulador.gen_alg_regulador import cria_populacao_inicial, algoritmo_genetico

def regulador_main():
    print("--- Otimizador de ganhos PID com Algoritmo Genético ---")
    print("--- Função de transferência ---")
    planta = cria_funcao_da_planta()

    pesos = determina_pesos()

    sim_time_input = int(input("\nQuantos segundos de simulação você deseja (recomendado -> 10)?\n"))

    tamanho_populacao = int(input("Qual é o tamanho de população que deseja para a otimização? (recomendado = 100)\n"))
    populacao_inicial = cria_populacao_inicial(tamanho_populacao)

    setpoint = int(input("Qual a amplitude do degrau que deseja ser testado?\n"))

    print("\nIniciando o processo de otimização")

    melhor_individuo = algoritmo_genetico(planta, pesos, populacao_inicial, sim_time_input, setpoint)

    if melhor_individuo:
        print("\n--- Resultados da otimização ---")
        Kp_ot, Ki_ot, Kd_ot = melhor_individuo
        print("--- Ganhos ótimos encontrados ---")
        print(f"Kp = {Kp_ot:.4f}")
        print(f"Ki = {Ki_ot:.4f}")
        print(f"Kd = {Kd_ot:.4f}")
        plot_system(planta, melhor_individuo, sim_time_input, setpoint)
    else:
        print("\nNão foi possível encontrar uma solução.")
    
