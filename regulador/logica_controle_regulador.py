import numpy as np
import matplotlib.pyplot as plt
import control as ct

def cria_funcao_do_controlador(k_p, k_i, k_d):
    num = np.array([k_d, k_p, k_i]) # (Kd*s² + Kp*s + Ki)
    den = np.array([1, 0]) # 1s + 0
    func_trans = ct.tf(num, den)
    return func_trans

def cria_funcao_da_planta():
    N = input("Digite os coeficiente do numerador do maior expoente ao menor (espaçados, 0 caso não tenha algum intermediário): ")
    D = input("Digite os coeficiente do denominador do maior expoente ao menor (espaçados, 0 caso não tenha algum intermediário): ")
    num = np.array([float(x) for x in N.split()])
    den = np.array([float(x) for x in D.split()])
    func_trans = ct.tf(num, den)
    return func_trans

def calcula_performance(planta, k_p, k_i, k_d, sim_time = 10, setpoint = 1.0):
    try:
        # Montagem da malha fechada com planta pré-estabelecida e controlador variável
        controle = cria_funcao_do_controlador(k_p, k_i, k_d)
        malha_aberta = planta * controle
        sistema_final = ct.feedback(malha_aberta, 1)
        
        polos = ct.poles(sistema_final)

        if any(p.real >= 0 for p in polos):
            return float('inf'), float('inf'), float('inf'), float('inf')

        # Simulação
        tempo = np.linspace(0, sim_time, sim_time*100 + 1)
        tempo, resposta_nao_escalada = ct.step_response(sistema_final, T = tempo)
        resposta = resposta_nao_escalada * setpoint

        # Valor de y_inf 
        valor_final = resposta[-1] 

        # Verificação de sistemas instáveis
        if max(abs(resposta)) > 1e5:
            return float('inf'), float('inf'), float('inf'), float('inf')

        # Mp (Overshoot/Sobressinal)
        pico = max(resposta)
        if pico > valor_final:
            sobressinal = (pico - valor_final)/(valor_final + 1e-9)
        else:
            sobressinal = 0 # Inexistência de sobressinal
        
        # Erro em regime estacionário
        err_regime = abs((valor_final - setpoint)/(setpoint + 1e-9))

        # Tempo de Assentamento (lógica considerando velocidade e aceleração do sinal)
        tolerancia = 0.02 # Tolerância de 2%
        desvio_sup = valor_final * (1 + tolerancia)
        desvio_inf = valor_final * (1 - tolerancia)
        derivada = np.diff(resposta)/np.diff(tempo)
        if(len(derivada) > 1):
            aceleracao = np.diff(derivada) / np.diff(tempo[:-1])
            aceleracao_final = abs(aceleracao[-1])
        else:
            aceleracao_final = 0
        velocidade_final = abs(derivada[-1]) if len(derivada) > 0 else 0
        limiar_vel = 0.05
        limiar_acl = 0.005
        ultimo_ponto_dentro = (desvio_inf <= resposta[-1] <= desvio_sup)
        parando_de_fato = ((velocidade_final < limiar_vel) and (aceleracao_final < limiar_acl))
        if (ultimo_ponto_dentro and parando_de_fato):
            t_a = tempo[0]
            for i in range(len(resposta) - 1, -1, -1):
                if not(desvio_inf <= resposta[i] <= desvio_sup):
                    if i == len(resposta) - 1:
                        t_a = sim_time
                    else:
                        t_a = tempo[i + 1]
                    break
        else:
            t_a = sim_time
        
        # Tempo de subida
            
        indice_10 = None # Placeholder de 10%
        indice_90 = None # Placeholder de 90%

        for i, valor in enumerate(resposta):
            if (indice_10 is None) and (valor > valor_final*0.1):
                indice_10 = i
            if (indice_90 is None) and (valor > valor_final*0.9):
                indice_90 = i
            if (indice_10 is not None) and (indice_90 is not None):
                break

        if (indice_10 is None) or (indice_90 is None):
            t_s = float('inf')
        else:
            t_s = tempo[indice_90] - tempo[indice_10]
        
        return sobressinal, t_s, t_a, err_regime
    except Exception as e:
        print(f"Ocorreu um erro na simulação: {e}")
        return float('inf'), float('inf'), float('inf'), float('inf')

def calcula_fitness(parametros, pesos, sim_time = 10):
    sobressinal, t_s, t_a, err_regime = parametros
    peso_os, peso_ts, peso_ta, peso_err = pesos

    sobressinal_norm = sobressinal
    err_regime_norm = err_regime
    t_a_norm = t_a/sim_time
    t_s_norm = t_s/sim_time

    if any(p == float('inf') for p in parametros):
        return 0.0 

    custo = (peso_os * sobressinal_norm) + (peso_ts * t_s_norm) + \
            (peso_ta * t_a_norm) + (peso_err * err_regime_norm)

    fitness = 1 / (custo + 1e-9)
    return fitness

def determina_pesos():
    P = input("Na seguinte ordem: sobressinal, tempo de subida, tempo de \
          assentamento, erro no estacionário \nDiga o nível de relevância \
          do parâmetro numa escala de 0.0 a 10.0 (números diferentes espaçados): ")
    
    pesos = np.array([float(x) for x in P.split()])
    return pesos

def plot_system(planta, melhor_individuo, sim_time_input = 10, setpoint = 1.0):
    kp, ki, kd = melhor_individuo
    controlador = cria_funcao_do_controlador(kp, ki, kd)
    sistema_malha_fechada = ct.feedback(planta * controlador, 1)
    tempo = np.linspace(0, sim_time_input, sim_time_input*100 + 1)
    tempo, resposta_sem_escala = ct.step_response(sistema_malha_fechada, T = tempo)
    resposta = resposta_sem_escala * setpoint
    fig, ax = plt.subplots(figsize=(12, 7))
    parametros = calcula_performance(planta, kp, ki, kd)
    print(f"\nSobressinal: {100*parametros[0]:.4f}%")
    print(f"Tempo de subida: {parametros[1]:.4f} (s)")
    print(f"Tempo de assentamento: {parametros[2]:.4f} (s)")
    print(f"Erro em regime estacionário: {100*parametros[3]:.4f}%")
    ax.plot(tempo, resposta, linewidth=2, label = 'Resposta otimizada')
    ax.set_title("Resposta do sistema ao degrau com ganhos otimizados", )
    ax.set_xlabel("Tempo (s)", fontsize=12)
    ax.set_ylabel("Posição", fontsize=12)
    ax.grid(True, which="both", linestyle=":", linewidth=0.7)
    ax.axhline(y = setpoint, color='r', linestyle='-.', label=f"Setpoint: {setpoint:.1f}")
    ax.axhline(y = setpoint*(1.02), color ='gray', linestyle ='--', label="Faixa de desvio de 2%")
    ax.axhline(y = setpoint*(0.98), color ='gray', linestyle ='--')
    ax.legend()
    plt.show()

