import random as rd
import logica_controle as pf

LIMITES_GANHOS = {
    "kp":[0.0, 20.0],
    "ki":[0.0, 20.0],
    "kd":[0.0, 10.0]
}

def cria_populacao_inicial(tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        kp = rd.uniform(LIMITES_GANHOS["kp"][0], LIMITES_GANHOS["kp"][1])
        ki = rd.uniform(LIMITES_GANHOS["ki"][0], LIMITES_GANHOS["ki"][1])
        kd = rd.uniform(LIMITES_GANHOS["kd"][0], LIMITES_GANHOS["kd"][1])
        populacao.append([kp, ki, kd])
    return populacao

def selecao_por_torneio(populacao, fitnesses, k=3):
    indices_torneio = rd.choices(range(len(populacao)), k=k)
    fitness_participantes = [fitnesses[i] for i in indices_torneio]
    indice_vencedor_local = fitness_participantes.index(max(fitness_participantes))
    return populacao[indices_torneio[indice_vencedor_local]]

def cruzamento(pai1, pai2):
    kp_filho = (pai1[0] + pai2[0]) / 2
    ki_filho = (pai1[1] + pai2[1]) / 2
    kd_filho = (pai1[2] + pai2[2]) / 2
    
    kp_filho = max(min(kp_filho, LIMITES_GANHOS['kp'][1]), LIMITES_GANHOS['kp'][0])
    ki_filho = max(min(ki_filho, LIMITES_GANHOS['ki'][1]), LIMITES_GANHOS['ki'][0])
    kd_filho = max(min(kd_filho, LIMITES_GANHOS['kd'][1]), LIMITES_GANHOS['kd'][0])
    
    return [kp_filho, ki_filho, kd_filho]

def mutacao(individuo, taxa_mutacao=0.1):
    individuo_mutado = list(individuo)
    # Mutação no Kp
    if rd.random() < taxa_mutacao:
        variacao = rd.gauss(0, 1.0) # Média 0, desvio padrão 1.0
        individuo_mutado[0] += variacao
        individuo_mutado[0] = max(min(individuo_mutado[0], LIMITES_GANHOS['kp'][1]), LIMITES_GANHOS['kp'][0])

    # Mutação no Ki
    if rd.random() < taxa_mutacao:
        variacao = rd.gauss(0, 1.0)
        individuo_mutado[1] += variacao
        individuo_mutado[1] = max(min(individuo_mutado[1], LIMITES_GANHOS['ki'][1]), LIMITES_GANHOS['ki'][0])

    # Mutação no Kd
    if rd.random() < taxa_mutacao:
        variacao = rd.gauss(0, 0.5) # Mantendo a escala para o Kd
        individuo_mutado[2] += variacao
        individuo_mutado[2] = max(min(individuo_mutado[2], LIMITES_GANHOS['kd'][1]), LIMITES_GANHOS['kd'][0])
        
    return individuo_mutado

def algoritmo_genetico(planta, pesos, populacao_inicial):
    MAX_GERACOES = 500
    GERACOES_ESPERA = 20

    melhor_fitness = -1.0
    geracoes_sem_melhora = 0
    melhor_individuo = None
    populacao_atual = populacao_inicial

    for geracao in range(MAX_GERACOES):
        fitnesses = [pf.calcula_fitness(pf.calcula_performance(planta, *ind), pesos) for ind in populacao_atual]

        melhor_fitness_geracao = max(fitnesses)
        indice_melhor_da_geracao = fitnesses.index(melhor_fitness_geracao)
        melhor_geracao = populacao_atual[indice_melhor_da_geracao]
        
        if melhor_fitness_geracao > melhor_fitness:
            melhor_fitness = melhor_fitness_geracao
            melhor_individuo = populacao_atual[indice_melhor_da_geracao]
            geracoes_sem_melhora = 0
            print(f"Geração {geracao}: Nova melhor solução encontrada! Fitness: {melhor_fitness:.4f}")
        else:
            geracoes_sem_melhora += 1
            print(f"Geração {geracao}: Sem melhora. Melhor fitness global: {melhor_fitness:.4f}")
        
        if geracoes_sem_melhora >= GERACOES_ESPERA:
            print(f"\nEstagnação detectada após {GERACOES_ESPERA} gerações sem melhora. Parando...")
            break
        
        nova_populacao = []
        nova_populacao.append(melhor_geracao)

        for _ in range(len(populacao_inicial) - 1):
            pai1 = selecao_por_torneio(populacao_atual, fitnesses)
            pai2 = selecao_por_torneio(populacao_atual, fitnesses)
            filho = cruzamento(pai1, pai2)
            filho_mutado = mutacao(filho)
            nova_populacao.append(filho_mutado)
        
        populacao_atual = nova_populacao

    print(f"\nOtimização concluída!")
    print(f"Melhor solução encontrada: Kp={melhor_individuo[0]:.4f}, Ki={melhor_individuo[1]:.4f}, Kd={melhor_individuo[2]:.4f}")
    print(f"Com um fitness de: {melhor_fitness:.4f}")
    return melhor_individuo
