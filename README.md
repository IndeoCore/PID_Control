# Como usar?

Executar o arquivo _"simulador.py"_. Ao iniciá-lo, ele irá pedir na seguinte ordem:

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
- Após isso, o algoritmo de otimização genética irá rodar e após um tempo irá convergir para um resultado, após convergir, irá retonar no terminal os valores de Kp Ki e Kd do controlador, sendo K(s) = Ki/s + Kp + Kd.s´.
- Além disso, irá também plotar o gráfico da resposta ao degrau considerando os valores de ganho PID otimizados.   
  
