import numpy as np
import pandas as pd

# Constantes físicas
g = 9.81  # aceleración gravitacional en m/s²
altura_inicial = 100  # altura inicial en metros
tiempo_total = np.sqrt(2 * altura_inicial / g)  # tiempo total de caída
dt = 0.1  # intervalo de tiempo en segundos

# Crear array de tiempo base
tiempo = np.arange(0, tiempo_total + dt, dt)
n_muestras = len(tiempo)

# Calcular valores teóricos
posicion = altura_inicial - 0.5 * g * tiempo**2
velocidad = -g * tiempo
aceleracion = np.full_like(tiempo, -g)

# Agregar ruido aleatorio para simular mediciones reales
np.random.seed(42)  # Para reproducibilidad
ruido_posicion = np.random.normal(0, 0.5, n_muestras)
ruido_velocidad = np.random.normal(0, 0.8, n_muestras)
ruido_aceleracion = np.random.normal(0, 0.2, n_muestras)

posicion += ruido_posicion
velocidad += ruido_velocidad
aceleracion += ruido_aceleracion

# Crear DataFrame base
df = pd.DataFrame({
    'tiempo': tiempo,
    'posicion': posicion,
    'velocidad': velocidad,
    'aceleracion': aceleracion
})

# 1. Introducir valores nulos de manera aleatoria (10% de los datos)
for columna in ['posicion', 'velocidad', 'aceleracion']:
    mascara_nulos = np.random.random(n_muestras) < 0.1
    df.loc[mascara_nulos, columna] = np.nan

# 2. Introducir duplicados (5% de los datos)
n_duplicados = int(n_muestras * 0.05)
indices_duplicados = np.random.choice(df.index, n_duplicados)
duplicados = df.loc[indices_duplicados].copy()
# Agregar pequeñas variaciones a los duplicados
duplicados['tiempo'] += np.random.normal(0, 0.001, len(duplicados))
df = pd.concat([df, duplicados], ignore_index=True)

# 3. Introducir valores atípicos (outliers)
n_outliers = int(n_muestras * 0.02)  # 2% de outliers
indices_outliers = np.random.choice(df.index, n_outliers)
df.loc[indices_outliers, 'posicion'] *= np.random.uniform(1.5, 2.0, n_outliers)
df.loc[indices_outliers, 'velocidad'] *= np.random.uniform(1.5, 2.0, n_outliers)
df.loc[indices_outliers, 'aceleracion'] *= np.random.uniform(1.5, 2.0, n_outliers)

# Ordenar por tiempo para mejor visualización
df = df.sort_values('tiempo').reset_index(drop=True)

# Guardar datos en CSV
df.to_csv('datos_caida_libre_transformaciones.csv', index=False)

# Mostrar información sobre el dataset
print("Información del dataset:")
print(df.info())
print("\nEstadísticas descriptivas:")
print(df.describe())
print("\nValores nulos por columna:")
print(df.isnull().sum())
print("\nNúmero de duplicados:", df.duplicated().sum())

# Ejemplos de las transformaciones solicitadas
print("\n=== Ejemplos de transformaciones ===")

# 1. Eliminar nulos
df_sin_nulos = df.dropna()
print("\nRegistros después de eliminar nulos:", len(df_sin_nulos))

# 2. Eliminar duplicados (considerando pequeñas variaciones en tiempo)
df_sin_duplicados = df.round(3).drop_duplicates()
print("Registros después de eliminar duplicados:", len(df_sin_duplicados))

# 3. Normalizar datos
df_normalizado = df.copy()
for columna in ['posicion', 'velocidad', 'aceleracion']:
    df_normalizado[columna] = (df[columna] - df[columna].mean()) / df[columna].std()
print("\nDatos normalizados (primeras 5 filas):")
print(df_normalizado.head())

# 4. Rellenar nulos con la media
df_rellenado = df.copy()
for columna in ['posicion', 'velocidad', 'aceleracion']:
    df_rellenado[columna] = df_rellenado[columna].fillna(df_rellenado[columna].mean())
print("\nDatos después de rellenar nulos (valores nulos restantes):")
print(df_rellenado.isnull().sum())