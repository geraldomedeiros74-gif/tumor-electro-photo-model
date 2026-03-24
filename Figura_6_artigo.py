import numpy as np
import matplotlib.pyplot as plt

# =========================
# MODELO FINAL (MESMO DA FIGURA 5)
# =========================

def simular_regime(intensidade, recuperacao, modo="continuo"):

    ATP, ROS, Vm, dano = 1.0, 0.2, -70, 0
    D_hist = []

    for s in range(56):  # 8 semanas

        # -----------------------
        # DEFINIÇÃO DO REGIME
        # -----------------------
        if modo == "6_2":
            ativo = (s % 8) < 6
        else:
            ativo = True

        # -----------------------
        # ESTÍMULO
        # -----------------------
        if ativo:
            for _ in range(3):

                ATP -= intensidade * 0.025
                ROS += intensidade * 0.05
                Vm += intensidade * 3.0

                ATP += 0.003
                ROS += 0.002

                ATP = np.clip(ATP, 0, 1)
                ROS = np.clip(ROS, 0, 1)

                # DANO NÃO LINEAR
                dano += (ROS**2) * (1 - ATP) * 0.1

                if ROS > 0.4:
                    dano += 0.03

                dano = min(2.5, dano)

        # -----------------------
        # RECUPERAÇÃO
        # -----------------------
        fator_dano = max(0.2, 1 - dano)

        ATP += (1 - ATP) * recuperacao * fator_dano
        ROS -= (ROS - 0.2) * recuperacao * fator_dano
        Vm  += (-70 - Vm) * recuperacao * fator_dano

        # RECUPERAÇÃO DO DANO
        dano -= recuperacao * dano * 0.1
        dano = max(0, dano)

        ATP = np.clip(ATP, 0, 1)
        ROS = np.clip(ROS, 0, 1)

        D_hist.append(dano)

    return np.array(D_hist)


# =========================
# PARÂMETROS
# =========================

intensidade = 0.22
recuperacao = 0.6

D_cont = simular_regime(intensidade, recuperacao, "continuo")
D_62 = simular_regime(intensidade, recuperacao, "6_2")


# =========================
# PLOT
# =========================

plt.figure(figsize=(7,5))

plt.plot(D_cont, label="Contínuo")
plt.plot(D_62, label="6/2 (com pausas)")

plt.xlabel("Sessões")
plt.ylabel("Dano acumulado")
plt.title("Comparação entre regimes de aplicação")

plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("fig6_regimes.pdf", dpi=300)
plt.show()