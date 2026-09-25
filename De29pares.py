import pandas as pd
from descarga_salida import data

# ============================
# 1. Crear DataFrame
# ============================
df = pd.DataFrame(data, columns=["anio","mes","dia","dia_semana","valor1","valor2","valor3","valor4","valor5"])

# ============================
# 2. Limpiar espacios y convertir a enteros
# ============================
df["anio"] = df["anio"].str.strip().astype(int)
df["mes"] = df["mes"].str.strip().astype(int)
df["dia"] = df["dia"].str.strip().astype(int)
df["dia_semana"] = df["dia_semana"].str.strip()

# ============================
# 3. Crear columna fecha y weekday
# ============================
df["fecha"] = pd.to_datetime(df["anio"].astype(str) + "-" +
                             df["mes"].astype(str) + "-" +
                             df["dia"].astype(str))
df["weekday"] = df["fecha"].dt.weekday

# Excluir domingos
df = df[df["weekday"] != 6]

# ============================
# 4. Extraer pares finales (últimos dos dígitos)
# ============================
for i in range(1, 6):
    df[f"par{i}"] = df[f"valor{i}"].astype(str).str[-2:]

# ============================
# 5. Preguntar al usuario el par objetivo
# ============================
par_objetivo = input("Ingrese el par objetivo (ejemplo: '62'): ").strip()

# ============================
# 6. Generar bloques de máximo 6 filas
# ============================
bloques = []
i = 0
while i < len(df):
    fila = df.iloc[i]
    pares = [fila[f"par{j}"] for j in range(1,6)]
    if par_objetivo in pares:
        bloque = [fila]
        j = i + 1
        while j < len(df) and len(bloque) < 6:
            fila_sig = df.iloc[j]
            pares_sig = [fila_sig[f"par{k}"] for k in range(1,6)]
            bloque.append(fila_sig)
            # si aparece el objetivo en esta fila, cortar aquí y reiniciar
            if par_objetivo in pares_sig and len(bloque) > 1:
                bloques.append(bloque[:-1])  # guardar bloque hasta antes del nuevo objetivo
                bloque = [fila_sig]          # reiniciar bloque desde esta fila
            j += 1
        bloques.append(bloque)
        i = j
    else:
        i += 1

# ============================
# 7. Mostrar bloques
# ============================
print("=== BLOQUES GENERADOS ===")
for idx, bloque in enumerate(bloques, start=1):
    print(f"\nBloque {idx} (inicia {bloque[0]['fecha'].date()}):")
    for _, row in enumerate(bloque):
        pares = [row[f"par{i}"] for i in range(1,6)]
        # Convertimos la lista en string manualmente para que quede todo en una sola línea
        pares_str = "[" + ", ".join([f"'{p}'" for p in pares]) + "]"
        print(f"{row['fecha'].date()} ({row['dia_semana']}): {pares_str}")

# ============================
# 8. Ranking de pares acompañantes
# ============================
pares = []
for bloque in bloques:
    for _, row in enumerate(bloque):
        for i in range(1,6):
            par = row[f"par{i}"]
            if par != par_objetivo:
                pares.append(par)

conteo = pd.Series(pares).value_counts().reset_index()
conteo.columns = ["par", "repeticiones"]

total_tablas = len(bloques)
conteo["porcentaje"] = (conteo["repeticiones"] * 100 / total_tablas).round(2)

print("\n=== RANKING DE PARES QUE ACOMPAÑARON AL OBJETIVO ===")
print(f"Objetivo: {par_objetivo}")
print(f"{'Idx':<5}{'Par':<5}{'Reps':<12}{'Porcentaje':<10}")
print("-"*40)
for idx, row in conteo.iterrows():
    perc_str = f"{row['porcentaje']:.2f}%"
    print(f"{idx:<5}{str(row['par']):<5}{row['repeticiones']:<12}{perc_str:<10}")


# ============================
# 9. Guardar resultados en archivo (formato prolijo)
# ============================
with open("29pares.txt", "w", encoding="utf-8") as f:
    f.write("=== BLOQUES GENERADOS ===\n")
    for idx, bloque in enumerate(bloques, start=1):
        f.write(f"\nBloque {idx} (inicia {bloque[0]['fecha'].date()}):\n")
        f.write("-"*50 + "\n")
        for _, row in enumerate(bloque):
            pares = [row[f"par{i}"] for i in range(1,6)]
            pares_str = "[" + ", ".join([f"{p:>2}" for p in pares]) + "]"
            f.write(f"{row['fecha'].date()} ({row['dia_semana']:<9}): {pares_str}\n")
        f.write("-"*50 + "\n")

    f.write("\n=== RANKING DE PARES QUE ACOMPAÑARON AL OBJETIVO ===\n")
    f.write(f"Objetivo: {par_objetivo}\n")
    f.write(f"{'Idx':<5}{'Par':<5}{'Reps':<12}{'Porcentaje':<10}\n")
    f.write("-"*40 + "\n")
    for idx, row in conteo.iterrows():
        perc_str = f"{row['porcentaje']:.2f}%"
        f.write(f"{idx:<5}{str(row['par']):<5}{row['repeticiones']:<12}{perc_str:<10}\n")
