import numpy as np
from collections import Counter

# =========================
# AVALIAÇÃO DO ESTADO
# =========================

def avaliar_estado(bits):

    intensidade = 0.1 + bits[0]*0.2
    luz = 0.005 + bits[1]*0.02
    tempo = 1 + bits[2]*2
    recuperacao = 0.4 + bits[3]*0.5

    ATP, ROS, Vm, dano = 1.0, 0.2, -70, 0

    for s in range(56):

        for _ in range(tempo):

            ATP -= intensidade * 0.025
            ROS += intensidade * 0.05
            Vm += intensidade * 3.0

            ATP += luz
            ROS += luz * 0.5

            ATP = np.clip(ATP, 0, 1)
            ROS = np.clip(ROS, 0, 1)

            dano += (ROS**2) * (1 - ATP) * 0.1

            if ROS > 0.4:
                dano += 0.03

            dano = min(2.5, dano)

        fator_dano = max(0.2, 1 - dano)

        ATP += (1 - ATP) * recuperacao * fator_dano
        ROS -= (ROS - 0.2) * recuperacao * fator_dano

        dano -= recuperacao * dano * 0.1
        dano = max(0, dano)

    return dano


# =========================
# AMOSTRAGEM COM SOFTMAX
# =========================

def amostrar(shots=2000, temperatura=0.5):

    estados = []
    danos = []

    # gerar todos os estados possíveis
    todos_estados = []
    for i in range(16):
        bits = list(map(int, format(i, '04b')))
        todos_estados.append(bits)
        danos.append(avaliar_estado(bits))

    danos = np.array(danos)

    # softmax
    probs = np.exp(danos / temperatura)
    probs /= probs.sum()

    # amostragem
    escolhas = np.random.choice(len(todos_estados), size=shots, p=probs)

    for idx in escolhas:
        estado = ''.join(map(str, todos_estados[idx]))
        estados.append(estado)

    return Counter(estados)


# =========================
# EXECUÇÃO
# =========================

resultados = amostrar(2000)

print("Distribuição de estados:")
for k, v in sorted(resultados.items(), key=lambda x: -x[1]):
    print(k, v)
    