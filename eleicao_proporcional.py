# Importação de bibliotecas
import pandas as pd

# Leitura do arquivo csv
data =  pd.read_csv('eleicao.csv', sep=';')

# Variaveis predefinidas
total_vagas = 29
QE = 12684

# Filtragem de coligações
coligacoes = []

for i in data['Partido/Coligação']:
    elemento = i.split('-')
    if len(elemento) == 2:
        coligacoes.append(elemento[1][1:])
    else:
        coligacoes.append(elemento[0])
        
data['coligacoes'] = coligacoes

# Quantidade de votos de cada partido
coligacoes_e_votos = {}

for i, j in enumerate(coligacoes):
    if j in coligacoes_e_votos :
        coligacoes_e_votos [j] += data['Votos'][i]
    else:
        coligacoes_e_votos [j] = data['Votos'][i]

# Calculo do QP
QP = {key: int(value / QE) for key, value in coligacoes_e_votos.items() 
      if int(value / QE) > 0}

# Calculo das vagas ocupadas e restantes
vagas_ocupadas =  sum(QP.values())
vagas_restantes = total_vagas - vagas_ocupadas

# Distribuição das vagas restantes
for i in range(vagas_restantes):
    media = {key : coligacoes_e_votos[key] / (value+1) for key, value in QP.items()}
    partido_vencedor = max(media, key=media.get)
    QP[partido_vencedor] += 1

# Ranking de candidatos
data_ordenado = data.sort_values(by='Votos', ascending=False)

frames = []

for key, value in QP.items():
    partido_atual = data_ordenado[data_ordenado['coligacoes'] == key]
    frames.append(partido_atual.iloc[0:value])
    
resultado = pd.concat(frames).sort_values(by='Votos', 
                                          ascending=False).drop('coligacoes', axis=1)

# Impressão de aquivo .tsv
resultado.to_csv('resultado.tsv', sep='\t', encoding='utf-8', index = False, header=False)