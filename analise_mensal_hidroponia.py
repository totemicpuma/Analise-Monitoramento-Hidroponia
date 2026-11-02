import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. CARREGAMENTO DOS DADOS DO RESERVATÓRIO HIDROPÔNICO
nome_arquivo = 'dados_monitoramento_hidroponia.xlsx'

try:
    df = pd.read_excel(nome_arquivo)
    print("Planilha de telemetria hidropônica carregada com sucesso!")
except Exception as e:
    print(f"Erro ao abrir o arquivo: {e}")
    exit()

# 2. PREPARAÇÃO E FILTRO (Mês de Março)
df['Data e Hora (GMT)'] = pd.to_datetime(df['Data e Hora (GMT)'], errors='coerce')
df_marco = df[df['Data e Hora (GMT)'].dt.month == 3].copy()

# 3. ANÁLISE QUALITATIVA (Distribuição de Frequências da Qualidade do Sensor)
qual_var = 'Classificação de dados de nível'
freq_abs = df_marco[qual_var].value_counts()
freq_rel = df_marco[qual_var].value_counts(normalize=True) * 100

print("\n--- Tabela de Frequência (Qualitativa - Sensores) ---")
for cat, val in freq_abs.items():
    print(f"{cat}: {val} registros ({freq_rel[cat]:.2f}%)")

# Gráfico de Barras Nomeado
plt.figure(figsize=(8, 6))
freq_abs.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribuição da Qualidade das Leituras Telemétricas (Março)')
plt.xlabel('Classificação do Registro do Sensor')
plt.ylabel('Quantidade de Leituras (Frequência)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('grafico_qualitativo.png', dpi=150)
plt.close()

# 4. ANÁLISE QUANTITATIVA (Medidas de Tendência Central, Posição e Dispersão)
col_nivel = 'Correção Nível (m)'
dados = df_marco[col_nivel].dropna()

# Cálculos Estatísticos
media = dados.mean()
mediana = dados.median()
desvio = dados.std()
cv = (desvio / media) * 100
q1 = dados.quantile(0.25)
q3 = dados.quantile(0.75)

print(f"\n--- Estatísticas Descritivas do Nível da Solução Nutritiva ---")
print(f"Média: {media:.4f} m")
print(f"Mediana (Q2): {mediana:.4f} m")
print(f"1º Quartil (Q1): {q1:.4f} m")
print(f"3º Quartil (Q3): {q3:.4f} m")
print(f"Desvio Padrão: {desvio:.4f}")
print(f"Coeficiente de Variação: {cv:.2f}%")

# Histograma e Boxplot Nomeados
plt.figure(figsize=(12, 5))

# Subplot 1: Histograma
plt.subplot(1, 2, 1)
plt.hist(dados, bins=15, color='lightgreen', edgecolor='black')
plt.title('Histograma: Distribuição do Nível da Solução')
plt.xlabel('Nível do Reservatório (m)')
plt.ylabel('Frequência (Nº de Registros)')

# Subplot 2: Box-plot
plt.subplot(1, 2, 2)
plt.boxplot(dados, vert=True, patch_artist=True, tick_labels=['Nível da Solução'])
plt.title('Box-plot: Medidas de Posição e Outliers')
plt.ylabel('Nível do Reservatório (m)')

plt.tight_layout()
plt.savefig('graficos_quantitativos.png', dpi=150)
plt.close()

# 5. ANÁLISE DA CORRELAÇÃO (Reposição Hídrica vs Nível)
correlacao = df_marco['Correção chuva (mm)'].corr(df_marco[col_nivel])
print(f"\n--- Análise de Correlação ---")
print(f"Coeficiente r de Pearson: {correlacao:.4f}")

# Gráfico de Dispersão Nomeado
plt.figure(figsize=(8, 6))
plt.scatter(df_marco['Correção chuva (mm)'], df_marco[col_nivel], alpha=0.4, color='orange')
plt.title(f'Gráfico de Dispersão: Reposição Hídrica vs Nível (r = {correlacao:.4f})')
plt.xlabel('Volume de Reposição / Aporte Hídrico (mm)')
plt.ylabel('Nível do Reservatório Hidropônico (m)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafico_dispersao.png', dpi=150)
plt.close()

print("\nSucesso! Todos os gráficos e cálculos mensais foram gerados.")
