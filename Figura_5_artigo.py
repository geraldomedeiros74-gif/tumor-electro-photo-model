import numpy as np
import matplotlib.pyplot as plt

def simular_dano(intensidade, recuperacao):

    ATP, ROS, Vm, dano = 1.0, 0.2, -70, 0

    for s in range(56):

        # -----------------------
        # ESTÍMULO
        # -----------------------
        for _ in range(3):

            ATP -= intensidade * 0.025
            ROS += intensidade * 0.05
            Vm += intensidade * 3.0

            # efeito da luz
            ATP += 0.003
            ROS += 0.002

            ATP = np.clip(ATP, 0, 1)
            ROS = np.clip(ROS, 0, 1)

            # -----------------------
            # DANO (AGORA NÃO LINEAR)
            # -----------------------
            dano += (ROS**2) * (1 - ATP) * 0.1

            if ROS > 0.4:
                dano += 0.03

            dano = min(2.5, dano)

        # -----------------------
        # RECUPERAÇÃO FISIOLÓGICA
        # -----------------------
        fator_dano = max(0.2, 1 - dano)

        ATP += (1 - ATP) * recuperacao * fator_dano
        ROS -= (ROS - 0.2) * recuperacao * fator_dano
        Vm  += (-70 - Vm) * recuperacao * fator_dano

        # -----------------------
        # RECUPERAÇÃO DE DANO (CORRIGIDA)
        # -----------------------
        dano -= recuperacao * dano * 0.1
        dano = max(0, dano)

        ATP = np.clip(ATP, 0, 1)
        ROS = np.clip(ROS, 0, 1)

    return dano


# =========================
# VARIAÇÃO DE PARÂMETROS
# =========================

intensidades = np.linspace(0.05, 0.3, 50)
recuperacoes = np.linspace(0.4, 0.95, 50)

heatmap = np.zeros((len(intensidades), len(recuperacoes)))

for i, I in enumerate(intensidades):
    for j, r in enumerate(recuperacoes):
        heatmap[i, j] = simular_dano(I, r)


# =========================
# PLOT
# =========================

plt.figure(figsize=(7,5))

plt.imshow(
    heatmap,
    origin='lower',
    aspect='auto',
    extent=[recuperacoes.min(), recuperacoes.max(),
            intensidades.min(), intensidades.max()]
)

plt.colorbar(label="Dano final")
plt.xlabel("Recuperação")
plt.ylabel("Intensidade")
plt.title("Mapa de regime — modelo final")

plt.tight_layout()
plt.savefig("fig5_heatmap_final.pdf", dpi=300)
plt.show()