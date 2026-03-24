import numpy as np
import matplotlib.pyplot as plt

# =========================
# CONFIGURAÇÃO GLOBAL
# =========================

semanas = 8
sessoes = semanas * 7
t = np.arange(sessoes)

# estilo de gráfico (publicação)
plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "legend.fontsize": 9,
    "lines.linewidth": 2
})

# =========================
# FUNÇÃO PRINCIPAL
# =========================

def simular(nome, intensidade, delta_ROS, delta_ATP, recuperacao,
            fator_dano_base, fator_dano_extra, limite_dano,
            usar_luz=True):

    ATP, ROS, Vm, dano = 1.0, 0.2, -70, 0

    ATP_hist, ROS_hist, D_hist = [], [], []

    for s in range(sessoes):

        for _ in range(3):

            # estímulo elétrico
            ATP -= intensidade * delta_ATP
            ROS += intensidade * delta_ROS
            Vm  += intensidade * 3.0

            # fotobiomodulação
            if usar_luz:
                ATP += 0.003
                ROS += 0.002

            # limites fisiológicos
            ATP = np.clip(ATP, 0, 1)
            ROS = np.clip(ROS, 0, 1)
            Vm  = np.clip(Vm, -90, -40)

            # dano
            dano += ROS * fator_dano_base
            if ROS > 0.35:
                dano += fator_dano_extra

            dano = min(limite_dano, dano)

        # recuperação
        fator_dano = max(0.2, 1 - dano)

        ATP += (1 - ATP) * recuperacao * fator_dano
        ROS -= (ROS - 0.2) * recuperacao * fator_dano
        Vm  += (-70 - Vm) * recuperacao * fator_dano

        ATP = np.clip(ATP, 0, 1)
        ROS = np.clip(ROS, 0, 1)
        Vm  = np.clip(Vm, -90, -40)

        ATP_hist.append(ATP)
        ROS_hist.append(ROS)
        D_hist.append(dano)

    return np.array(ATP_hist), np.array(ROS_hist), np.array(D_hist)

# =========================
# SIMULAÇÕES
# =========================

# Tumor
ATP_t, ROS_t, D_t = simular("Tumor", 0.20, 0.05, 0.025, 0.65, 0.04, 0.015, 1.0, True)

# Saudável
ATP_s, ROS_s, D_s = simular("Saudável", 0.12, 0.02, 0.015, 0.90, 0.015, 0.003, 0.7, True)

# Com vs sem luz
_, _, D_luz = simular("Luz", 0.20, 0.05, 0.025, 0.65, 0.04, 0.015, 1.0, True)
_, _, D_sem = simular("Sem Luz", 0.20, 0.05, 0.025, 0.65, 0.04, 0.015, 1.0, False)

# =========================
# FIGURA 1 — ATP
# =========================

plt.figure()
plt.plot(t, ATP_t, label="Tumor")
plt.plot(t, ATP_s, label="Saudável")
plt.xlabel("Tempo (sessões)")
plt.ylabel("ATP")
plt.title("Dinâmica do ATP")
plt.legend()
plt.grid()
plt.savefig("fig1_ATP.pdf", bbox_inches='tight')

# =========================
# FIGURA 2 — ROS
# =========================

plt.figure()
plt.plot(t, ROS_t, label="Tumor")
plt.plot(t, ROS_s, label="Saudável")
plt.xlabel("Tempo")
plt.ylabel("ROS")
plt.title("Dinâmica de ROS")
plt.legend()
plt.grid()
plt.savefig("fig2_ROS.pdf", bbox_inches='tight')

# =========================
# FIGURA 3 — DANO
# =========================

plt.figure()
plt.plot(t, D_t, label="Tumor")
plt.plot(t, D_s, label="Saudável")
plt.xlabel("Tempo")
plt.ylabel("Dano acumulado")
plt.title("Acúmulo de Dano")
plt.legend()
plt.grid()
plt.savefig("fig3_DANO.pdf", bbox_inches='tight')

# =========================
# FIGURA 4 — LUZ vs SEM LUZ
# =========================

plt.figure()
plt.plot(t, D_luz, label="Com luz")
plt.plot(t, D_sem, label="Sem luz")
plt.xlabel("Tempo")
plt.ylabel("Dano")
plt.title("Efeito da Fotobiomodulação")
plt.legend()
plt.grid()
plt.savefig("fig4_LUZ.pdf", bbox_inches='tight')

print("✔ Todas as figuras foram geradas em PDF vetorial.")