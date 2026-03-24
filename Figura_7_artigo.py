import matplotlib.pyplot as plt

resultados = {
'0000': 207, '0110': 141, '1111': 346, '0001': 158,
'0100': 186, '0101': 86, '1110': 19, '1011': 31,
'1001': 137, '0011': 151, '1000': 160, '1100': 157,
'0010': 165, '1010': 58, '0111': 21, '1101': 25
}

estados = list(resultados.keys())
frequencias = list(resultados.values())

plt.figure(figsize=(8,4))
plt.bar(estados, frequencias)
plt.xticks(rotation=90)
plt.xlabel("Estados binários")
plt.ylabel("Frequência")
plt.title("Distribuição de estados — otimização quântica simulada")
plt.tight_layout()
plt.savefig("fig7_quantum.pdf")