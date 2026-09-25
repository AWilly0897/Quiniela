from collections import Counter
from descarga_salida import data  # tu lista importada
import pandas as pd

# Crear DataFrame con nombres de columnas
df = pd.DataFrame(data, columns=["anio","mes","dia","dia_semana",
                                 "valor1","valor2","valor3","valor4","valor5"])

# Convertir tipos
df["anio"] = df["anio"].astype(str).str.strip().astype(int)
df["mes"] = df["mes"].astype(str).str.strip().astype(int)
df["dia"] = df["dia"].astype(str).str.strip().astype(int)
df["dia_semana"] = df["dia_semana"].astype(str).str.strip()

# Crear columna fecha y weekday
df["fecha"] = pd.to_datetime(df["anio"].astype(str) + "-" +
                             df["mes"].astype(str) + "-" +
                             df["dia"].astype(str))
df["weekday"] = df["fecha"].dt.weekday

# Excluir domingos (weekday = 6)
df = df[df["weekday"] != 6]

# Extraer los pares (últimos dos dígitos de cada valor)
for i in range(1,6):
    df[f"par{i}"] = df[f"valor{i}"].astype(str).str[-2:]

# Juntar todos los pares en una sola lista
pares = []
for i in range(1,6):
    pares.extend(df[f"par{i}"].astype(int).tolist())

# Contar ocurrencias
conteo = Counter(pares)

# Ordenar de mayor a menor frecuencia
ordenado = conteo.most_common()

# Escribir tabla en archivo
with open("pares_frecuentes.txt", "w", encoding="utf-8") as f:
    f.write("{:<5} {:<10} {:<10}\n".format("Pos", "Par", "Frecuencia"))
    f.write("-" * 30 + "\n")
    for i, (numero, frecuencia) in enumerate(ordenado, start=1):
        f.write("{:<5} {:<10} {:<10}\n".format(i, numero, frecuencia))

print("Tabla generada en pares_frecuentes.txt")
