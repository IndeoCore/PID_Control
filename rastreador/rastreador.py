from rastreador.logica_controle_rt import cria_funcao_da_planta, cria_funcao_de_referencia_flexivel, determina_pesos, plot_system
from rastreador.gen_alg_rt import cria_populacao_inicial, algoritmo_genetico
import numpy as np

def rastreador_main():
    print("--- Otimizador de ganhos PID com Algoritmo Genético ---")
    print("--- Função de transferência ---")
    planta = cria_funcao_da_planta()

    pesos = determina_pesos()

    sim_time_input = int(input("Quantos segundos de simulação você deseja (recomendado -> 20)?\n"))
    tempo = np.linspace(0, sim_time_input, sim_time_input*100 + 1)

    tamanho_populacao = int(input("Qual é o tamanho de população que deseja para a otimização? (recomendado = 100)\n"))
    populacao_inicial = cria_populacao_inicial(tamanho_populacao)
    
    print("\n--- Função de referência ---")
    func_referencia = cria_funcao_de_referencia_flexivel(tempo)

    print("\n--- Iniciando o processo de otimização ---")

    melhor_individuo = algoritmo_genetico(planta, func_referencia, pesos, populacao_inicial, sim_time_input)

    if melhor_individuo:
        print("\n--- Resultados da otimização ---")
        Kp_ot, Ki_ot, Kd_ot = melhor_individuo
        print("--- Ganhos ótimos encontrados ---")
        print(f"Kp = {Kp_ot:.4f}")
        print(f"Ki = {Ki_ot:.4f}")
        print(f"Kd = {Kd_ot:.4f}")
        plot_system(planta, func_referencia, melhor_individuo, sim_time = sim_time_input )
    else:
        print("\nNão foi possível encontrar uma solução.")
    
