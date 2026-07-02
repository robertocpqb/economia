# Deflator

# Vamos criar um código que deflacione valores pelo IPCA cheio
#Primeira coisa vamos importar o valor do IPCA Mensal pela SIDRA do IBGE

# 1. Importando a inflação
#region


# 1.1 Baixando a Bibliotecas
#region
import numpy as np
import requests
import truststore
truststore.inject_into_ssl()
from sidrapy import get_table
import sidrapy
import ssl
import pandas as pd
#endregion


# 1.2 Parâmetros de importação
#region

tabela = '1737'          # Tabela no site do SIDRA que contém a variável que queremos (https://sidra.ibge.gov.br/home/pimpfbr/brasil)
variable = '63'         # Através do Código da tabela, buscamos o código da variével que queremos, pode achar pela tabela (https://apisidra.ibge.gov.br/)
#cnae = '56318'          # No mesmo lugar do passo anterior vemos o código CNAE da atividade buscado

#endregion


# 1.3. Requisição via API do SIDRA 
#region


# Aqui ele monta a url segundo nossos parâmetros dados e pede TODOS os períodos
url = f"https://apisidra.ibge.gov.br/values/t/{tabela}/n1/all/v/{variable}/p/all"
r = requests.get(url, verify=False)  # verify=False só para teste rápido
r.raise_for_status()
  
# Transforma o JSON em DataFrame
data = r.json()
df = pd.DataFrame(data[0:],)  # pula o primeiro item (metadados)

# Exibe o resultado
print(df.head())

#endregion


# 1.4 Limpando a base de dados
#region 

print(df.columns)


df = df[['D3C', 'D3N', 'V']]

df.columns = ['Data Código', 'Data', 'Valor']

print(df)
#endregion


#endregion


# 2. Determinando parâmetros de importação
#region

ano = input('Qual o ano de referência?')
mês = input('Qual o ano de referência?')







# 2. Determinando parâmetros de 
# 2. Determinando parâmetros de 