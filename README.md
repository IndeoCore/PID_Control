# Como usar?

Executar o arquivo _"otimimzador.py"_. Ao iniciá-lo, ele irá pedir na seguinte ordem:

- Qual tipo de otimização você quer realizar. É em relação ao degrau unitário, ou é m _reference tracker_. Responda com:
  - D - resposta ao degrau
  - R - rastrear uma função u(t)

## Resposta ao degrau

Na resposta ao degrau, irá te pedir na seguinte sequência:

- Coeficientes do numerador da função de transferência da planta em ordem decrescente de grau.
- Coeficientes do denominador da função de transferência da planta em ordem decrescente de grau.
  - Exemplo: G(s) = (s + 1) / (3s^2 + 2s + 1):
    - Entradas numerador: 1 1
    - Entradas denominador: 3 2 1
- Pedirá os pesos (as relevâncias) de cada parâmetro importante para o sinal. Sendo eles:
- Sobressinal, tempo de subida, tempo de assentamento, erro no regime estacionário, nessa ordem.
  - Exemplo: Planta de um aquecedor de forno, onde o sobressinal é muito relevante (não se pode passar da temperatura desejada)
    - Entrada: 5 1 1 1
    - Isso significa que a otimização irá focar mais em otimizar o sobressinal em relação aos outros parâmetros.
- Tempo de simulação desejado, em segundos.
- Tamanho da população (quantos agentes simultanêos) cada geração do algoritmo genético terá.
  - Valores maiores implicam em uma maior variedade porém maior tempo de otimização
- Amplitude desejada do degrau.
- Após isso, o algoritmo de otimização genética irá ser iniciado e após um tempo, caso o sistema possa ser controlado por um controlador PID, irá convergir para um resultado e, após convergir, irá retonar no terminal os valores de Kp Ki e Kd do controlador, sendo K(s) = Ki/s + Kp + Kd.s´.
- Irá retornar no terminal também os seus valores de sobressinal, tempo de subida, tempo de assentamento e erro em regime.
- Além disso, irá também plotar o gráfico da resposta ao degrau considerando os valores de ganho PID otimizados.

## Resposta a uma função u(t)

Na resposta de um rastreador de função, o pgorama irá te pedir na seguinte sequência:

- Coeficientes do numerador da função de transferência da planta em ordem decrescente de grau.
- Coeficientes do denominador da função de transferência da planta em ordem decrescente de grau.
  - Exemplo: G(s) = (s + 1) / (3s^2 + 2s + 1):
    - Entradas numerador: 1 1
    - Entradas denominador: 3 2 1
- Pedirá os pesos (as relevâncias) de cada parâmetro importante para o sinal. Sendo eles:
- Erro quadrático integral, e erro em regime estacionário médio
  - Normalmente, é recomendado pesos iguais para ambos (valor diferente de 0), mas em casos específicos, como no caso em que o que importa é a resposta depois de um certo tempo somente, podemos avaliar com mais relevância o erro em regime, por exemplo.
- Tempo de simulação desejado, em segundos.
- Irá abrir um menu recursivo onde você tem 3 opções para sua função u(t) inicialmente igual 0:
  - P - Somar uma componente polinomial na sua função u(t)
    - Sinal polinomial = a.s^n + b.s^(n - 1) + c.s^(n -2)...
    - Digitar os coeficientes na ordem decrescente espaçados.
    - Se seu sinal for de grau 3, terá 4 componentes.
    - Ex: 3x^3 + 5x^2 + 1 - Sem componente x^1
    - Input: 3 5 0 1
  - S - Somar uma componente senoidal na sua função u(t)
    - sinal senoidal = _A_ x sen(2 x π x _f_ x t + _phi_ x π)
    - Pedirá _A_, _f_ e _phi_, onde:
    - A = amplitude, f = frequência (em Hz), phi = multiplicador de pi para a fase
  - F - Finalizar esse menu e enviar para o sistema a função u(t) construída até então
- Tamanho da população (quantos agentes simultanêos) cada geração do algoritmo genético terá.
  - Valores maiores implicam em uma maior variedade porém maior tempo de otimização
- Após isso, o algoritmo de otimização genética irá ser iniciado e após um tempo, caso o sistema possa ser controlado por um controlador PID, irá convergir para um resultado e, após convergir, irá retonar no terminal os valores de Kp Ki e Kd do controlador, sendo K(s) = Ki/s + Kp + Kd.s.
- Irá retornar no terminal também os seus valores de erro quadrático integral e erro médio em regime.
  - Note que são valores absolutos, então para avaliar se são valores altos ou não, é necessário olhar a ordem de grandeza da resposta final;
- Além disso, irá também plotar o gráfico do rastreamento da função u(t) considerando os valores de ganho PID otimizados.

## Observações

### Gerações

- É possível alterar o número de gerações e o número de gerações que o algoritmo aceita esperar antes de decidir que a convergência (ou divergência nos casos mais absurdos) já ocorreu.
- Por convenção do programa, esses valores são, para a resposta ao degrau:
  - MAX_GERACOES = 500 (cria no máximo 500 gerações)
  - GERACOES_ESPERA = 20 (espera até no máximo 20 gerações iguais)
- Para a resposta a u(t):
  - MAX_GERACOES = 1000
  - GERACOES_ESPERA = 30
- Para alterar, basta entrar no arquivo _gen_alg_ do rastreador ou do regulador, e alterar conforme a necessidade.

### Ganhos

- Também é possível aumentar o intervalo em que os ganhos são procurados
- Valores padrão, para a respota ao degrau
  - Kp = [0 ; 20]
  - Ki = [0 ; 20]
  - Kd = [0 ; 10]
- Valores padrão, para a respota a u(t)
  - Kp = [0 ; 50]
  - Ki = [0 ; 50]
  - Kd = [0 ; 25]
- Para alterar, basta também entrar no arquivo _gen_alg_ do rastreador ou do regulador, e alterar conforme a necessidade.
