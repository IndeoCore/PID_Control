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

def obter_sinal_polinomial(tempo):
    try:
        coef_str = input("\n(Polinômio) Digite os coeficientes em ordem DECRESCENTE (ex: 2 1 5): ")
        coeffs = np.array([float(x) for x in coef_str.split()])
        return np.polyval(coeffs, tempo)
    except ValueError:
        print("Entrada inválida. Retornando sinal zero.")
        return np.zeros_like(tempo)

def obter_sinal_senoidal(tempo):
    try:
        print("\n(Senoide) Configurando: A * sin(2*pi*f*t + phi*pi)")
        amp = float(input("Digite a amplitude (A): "))
        freq = float(input("Digite a frequência em Hz (f): "))
        fase_mult = float(input("Digite o multiplicador da fase para pi (phi): "))
        fase = fase_mult * np.pi
        return amp * np.sin(2 * np.pi * freq * tempo + fase)
    except ValueError:
        print("Entrada inválida. Retornando sinal zero.")
        return np.zeros_like(tempo)


def cria_funcao_de_referencia_flexivel(tempo):
    
    sinal_final = np.zeros_like(tempo)
    
    while True:
        print("\n--- Construtor de Sinal de Referência ---")
        escolha = input("O que você quer fazer?\n"
                        " (P) Adicionar um componente Polinomial\n"
                        " (S) Adicionar um componente Senoidal\n"
                        " (F) Finalizar e retornar o sinal\n"
                        ">> ").upper()

        if escolha == 'P':
            sinal_final += obter_sinal_polinomial(tempo)
            print("Componente polinomial adicionado.")
        elif escolha == 'S':
            sinal_final += obter_sinal_senoidal(tempo)
            print("Componente senoidal adicionado.")
        elif escolha == 'F':
            print("Sinal final gerado.")
            break 
        else:
            print("Opção inválida. Tente novamente.")
            
    return sinal_final

def cria_funcao_de_transferencia():
    N = input("Digite os coeficiente do numerador do maior expoente ao menor (espaçados, 0 caso não tenha algum intermediário): ")
    D = input("Digite os coeficiente do denominador do maior expoente ao menor (espaçados, 0 caso não tenha algum intermediário): ")
    num = np.array([float(x) for x in N.split()])
    den = np.array([float(x) for x in D.split()])
    func_trans = ct.tf(num, den)
    return func_trans

def calcula_performance(planta, func_referencia, k_p, k_i, k_d, sim_time = 20):
    try:
        # Montagem da malha fechada com planta pré-estabelecida e controlador variável
        controle = cria_funcao_do_controlador(k_p, k_i, k_d)
        malha_aberta = planta * controle
        sistema_final = ct.feedback(malha_aberta, 1)

        polos = ct.poles(sistema_final)

        if any(p.real >= 0 for p in polos):
            return float('inf'), float('inf')

        # Simulação
        tempo = np.linspace(0, sim_time, sim_time*100 + 1)
        tempo, resposta = ct.forced_response(sistema_final, T = tempo, U=func_referencia)

        # Array de erro
        err = np.array(resposta - func_referencia)
        
        # Integral do Erro Quadrado (ISE)
        err_ise = err ** 2 
        ise = np.sum(err_ise) * 0.01

        # Erro do regime estacionário
        indice_inicio = int(len(err)*0.8)
        err_20_prct = np.abs(err[indice_inicio:])
        err_regime_medio = err_20_prct.mean()

        return ise, err_regime_medio
       
    except Exception as e:
        print(f"Ocorreu um erro na simulação: {e}")
        return float('inf'), float('inf')

def calcula_fitness(parametros, pesos, sim_time = 20):
    peso_ise, peso_regime = pesos
    erro_ise, erro_regime = parametros

    fator_escala = 1000

    if any(p == float('inf') for p in parametros):
        return 0.0 
    
    custo = (peso_ise * erro_ise) + \
            (peso_regime * erro_regime * fator_escala)

    fitness = 100 * (1 / (custo + 1e-9))
    return fitness

def determina_pesos():
    P = input("Na seguinte ordem: erro quadrático integral (ise), erro em regime estacionário \
          \nDiga o nível de relevância do parâmetro numa escala de 0.0 a 10.0 (números diferentes espaçados): ")
    
    pesos = np.array([float(x) for x in P.split()])
    return pesos


def plot_system(planta, funcao_referencia, melhor_individuo, sim_time = 20):
    kp, ki, kd = melhor_individuo
    controlador = cria_funcao_do_controlador(kp, ki, kd)
    malha_aberta = planta * controlador
    sistema_malha_fechada = ct.feedback(malha_aberta, 1)
    tempo = np.linspace(0, sim_time, sim_time*100 + 1)
    tempo, resposta = ct.forced_response(sistema_malha_fechada, T = tempo, U = funcao_referencia)
    parametros = calcula_performance(planta, funcao_referencia, kp, ki, kd, sim_time)
    print(f"\nErro ISE (Quadrático): {parametros[0]:.4f}")
    print(f"Erro médio de regime: {parametros[1]:.4f}")
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(tempo, resposta, linewidth=2, label = 'Resposta otimizada')
    ax.plot(tempo, funcao_referencia, linewidth=1, label = 'Função de referência', color='red')
    ax.set_title("Resposta do sistema a função de referência com ganhos otimizados" )
    ax.set_xlabel("Tempo (s)", fontsize=12)
    ax.set_ylabel("Posição", fontsize=12)
    ax.grid(True, which="both", linestyle=":", linewidth=0.7)
    ax.legend()
    plt.show()

