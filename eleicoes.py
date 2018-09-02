# Importação de bibliotecas
import pandas as pd
import numpy as np
import math

# Leitura do arquivo csv
data = pd.read_csv('eleicao.csv', sep=';')

# Variaveis predefinidas
total_vagas = 29
QE = 12684

# Filtragem de coligações
partidos = data['Partido/Coligação']

coligacoes = []

for i in partidos:
    elemento = i.split('-')
    if len(elemento) == 2:
        coligacoes.append(elemento[1][1:])
    else:
        coligacoes.append(elemento[0])
        
data['coligacoes'] = coligacoes

# Quantidade de votos de cada partido
votos = data['Votos']

coligacoes_e_votos = {}

for i, j in enumerate(coligacoes):
    if j in coligacoes_e_votos :
        coligacoes_e_votos [j] += votos[i]
    else:
        coligacoes_e_votos [j] = votos[i]

# Calculo do QP
QP = {key: math.floor(value / QE) for key, value in coligacoes_e_votos.items() 
      if math.floor(value / QE) > 0}

# Calculo das vagas ocupadas e restantes
vagas_ocupadas =  sum(QP.values())
vagas_restantes = total_vagas - vagas_ocupadas

# Distribuição das vagas restantes
for i in range(vagas_restantes):
    maior = {key : coligacoes_e_votos[key] / (value+1) for key, value in QP.items()}
    partido_vencedor = max(maior, key=maior.get)
    QP[partido_vencedor] += 1

# Ranking de candidatos
frames = []

for key, value in QP.items():
    partido_atual = data[data['coligacoes'] == key]
    partido_atual_ordenado = partido_atual.sort_values(by='Votos', ascending=False)
    frames.append(partido_atual_ordenado.iloc[0:value])
    
data_eleitos = pd.concat(frames)

data_eleitos_ordenado = data_eleitos.sort_values(by='Votos', ascending=False).drop('coligacoes', axis=1)

# Impressão de aquivo .tsv
data_eleitos_ordenado.to_csv('resultado_das_eleicoes.tsv', sep='\t', encoding='utf-8', index = False, header=False)