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

# Converter data e garantir que os dados numéricos estão corretos
df['Data e Hora (GMT)'] = pd.to_datetime(df['Data e Hora (GMT)'], errors='coerce')
col_nivel = 'Correção Nível (m)'
col_aporte = 'Correção chuva (mm)'

# 2. DEFINIÇÃO DOS PERÍODOS (Comparativo de Semanas Operacionais)
inicio_antes = pd.Timestamp('2024-03-13')
fim_antes = pd.Timestamp('2024-03-19 23:59:59')

inicio_pico = pd.Timestamp('2024-03-20')
fim_pico = pd.Timestamp('2024-03-26 23:59:59')

inicio_depois = pd.Timestamp('2024-03-27')
fim_depois = pd.Timestamp('2024-04-02 23:59:59')

# Filtragem dos DataFrames
df_antes = df[(df['Data e Hora (GMT)'] >= inicio_antes) & (df['Data e Hora (GMT)'] <= fim_antes)].copy()
df_pico = df[(df['Data e Hora (GMT)'] >= inicio_pico) & (df['Data e Hora (GMT)'] <= fim_pico)].copy()
df_depois = df[(df['Data e Hora (GMT)'] >= inicio_depois) & (df['Data e Hora (GMT)'] <= fim_depois)].copy()

periodos = [
    (df_antes, "Operação Estável (Sem. 1)"),
    (df_pico, "Pico de Vazão (Sem. 2)"),
    (df_depois, "Estabilização (Sem. 3)")
]

# 3. ANÁLISE QUANTITATIVA: Medidas de Tendência, Posição e Dispersão
print("\n" + "="*55)
print("ANÁLISE COMPARATIVA: NÍVEL DO RESERVATÓRIO HIDROPÔNICO")
print("="*55)

lista_para_boxplot = []
nomes_periodos = []

for dados_periodo, nome in periodos:
    v = dados_periodo[col_nivel].dropna()
    lista_para_boxplot.append(v)
    nomes_periodos.append(nome)

    print(f"\n>>> {nome.upper()}:")
    print(f"Média: {v.mean():.4f} m | Mediana: {v.median():.4f} m")
    print(f"Q1: {v.quantile(0.25):.4f} m | Q3: {v.quantile(0.75):.4f} m")
    print(f"Desvio Padrão: {v.std():.4f} | Máximo: {v.max():.4f} m")
    print(f"CV: {(v.std()/v.mean())*100:.2f}%")

# 4. GRÁFICOS COMPARATIVOS (Box-plot e Histograma)
# Gráfico 1: Box-plot Comparativo
plt.figure(figsize=(10, 6))
plt.boxplot(lista_para_boxplot, vert=True, patch_artist=True, tick_labels=nomes_periodos)
plt.title('Comparação do Nível Hidropônico: Estável, Pico de Recirculação e Pós-Ajuste')
plt.ylabel('Nível do Reservatório (m)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('boxplot_comparativo.png', dpi=150)
plt.close()

# Gráfico 2: Histograma Comparativo (Sobreposto)
plt.figure(figsize=(10, 6))
plt.hist(df_antes[col_nivel], bins=15, alpha=0.5, label='Semana 1 (Estável)', color='green')
plt.hist(df_pico[col_nivel], bins=15, alpha=0.5, label='Semana 2 (Pico de Vazão)', color='red')
plt.hist(df_depois[col_nivel], bins=15, alpha=0.5, label='Semana 3 (Estabilização)', color='blue')
plt.title('Distribuição de Frequências (Nível do Reservatório Hidropônico)')
plt.xlabel('Nível do Reservatório (m)')
plt.ylabel('Frequência de Registros')
plt.legend()
plt.tight_layout()
plt.savefig('histograma_comparativo.png', dpi=150)
plt.close()

# 5. ANÁLISE DE CORRELAÇÃO (Semana de Pico)
corr_pico = df_pico[col_aporte].corr(df_pico[col_nivel])
print("\n" + "="*55)
print(f"CORRELAÇÃO (Semana de Pico): r = {corr_pico:.4f}")
print("="*55)

plt.figure(figsize=(8, 6))
plt.scatter(df_pico[col_aporte], df_pico[col_nivel], color='orange', alpha=0.6)
plt.title(f'Dispersão na Semana de Pico de Recirculação (r = {corr_pico:.4f})')
plt.xlabel('Aporte Hídrico / Reposição (mm)')
plt.ylabel('Nível do Reservatório (m)')
plt.grid(True)
plt.tight_layout()
plt.savefig('dispersao_semana_pico.png', dpi=150)
plt.close()

print("\nProcessamento concluído! Gráficos comparativos salvos na pasta.")
