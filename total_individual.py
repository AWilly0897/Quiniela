import pandas as pd
from descarga_salida import data

# ============================
# 1. Crear DataFrame
# ============================
df = pd.DataFrame(data, columns=["anio","mes","dia","dia_semana",
                                 "valor1","valor2","valor3","valor4","valor5"])

# ============================
# 2. Limpiar espacios y convertir a enteros
# ============================
df["anio"] = df["anio"].astype(str).str.strip().astype(int)
df["mes"] = df["mes"].astype(str).str.strip().astype(int)
df["dia"] = df["dia"].astype(str).str.strip().astype(int)
df["dia_semana"] = df["dia_semana"].astype(str).str.strip()

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
# 5. Loop automático por todos los pares 00–99
# ============================
for objetivo in range(100):
    par_objetivo = f"{objetivo:02d}"

    # Generar bloques de máximo 6 filas
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
                if par_objetivo in pares_sig and len(bloque) > 1:
                    bloques.append(bloque[:-1])
                    bloque = [fila_sig]
                j += 1
            bloques.append(bloque)
            i = j
        else:
            i += 1

    # Ranking de pares acompañantes
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
    if total_tablas > 0:
        conteo["porcentaje"] = (conteo["repeticiones"] * 100 / total_tablas).round(2)

        # ============================
        # 6. Imprimir resultados de cada objetivo
        # ============================
        print("\n=== RANKING DE PARES QUE ACOMPAÑARON AL OBJETIVO ===")
        print(f"Objetivo: {par_objetivo}")
        print(f"{'Idx':<5}{'Par':<5}{'Reps':<12}{'Porcentaje':<10}")
        print("-"*40)
        for idx, row in conteo.iterrows():
            perc_str = f"{row['porcentaje']:.2f}%"
            print(f"{idx:<5}{str(row['par']):<5}{row['repeticiones']:<12}{perc_str:<10}")
