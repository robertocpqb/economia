# 1.0 Importações necessárias
#region
import pandas as pd
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import requests
import urllib3
import io
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#endregion



exp_f = {}


ano_inicial = int(input('Qual o ano inicial? '))
ano_final   = int(input('Qual o ano final? '))

ncm = 62042200
#62042200

ano = ano_inicial



# 2.0 Vamos importar os código dos países 
#region

#2.1 Webscrapp desse lugar aqui
#region
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url2 = 'https://www.fazcomex.com.br/npe/codigo-de-pais-para-siscomex-e-nf-e/'
response = requests.get(url2, verify=False, timeout=120)

soup = BeautifulSoup(response.text, "html.parser")
tabelas = pd.read_html(response.text)

#endregion

#2.2 Ajustes nos dados importados
#region

# Transforma em um DF mesmo
tabelas = tabelas[0].copy()


# Transforma a linha 0 em cabeçalho
tabelas.columns = tabelas.iloc[0]

# Remove a Linha antiga                
tabelas = tabelas.iloc[1:].reset_index(drop=True) 

tabelas.columns = [ 'SPED', 'PAIS', 'SECEX']
print(tabelas)

#endregion


# 2.3 Tirar o zero dos códigos
#region

# Se for 0317 deve virar 317, se for 1786 deve ficar igual

tabelas['SPED'] = tabelas['SPED'].astype(int)
tabelas['SECEX'] = tabelas['SECEX'].astype(int)

#endregion
#endregion




# 3. Loop que pega os anos do intervalo indicado
for ano in range(ano_inicial, ano_final + 1):
    
     
    # 3.1 URL E DOWLOAD dos dados
    #region
    url = f'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_{ano}.csv'
    r = requests.get(url, verify=False, timeout=120)
    print("status:", r.status_code, "bytes:", len(r.content))
    dfs = {}
    dfs[ano] = pd.read_csv(io.BytesIO(r.content), sep=';', encoding='latin1', low_memory=False)
    #endregion


    # 3.2 Limpada nos Dados
    #region
    print(dfs[ano].columns)
    df_limpo = dfs[ano][['CO_ANO', 'CO_NCM', 'CO_PAIS', 'CO_URF', 'VL_FOB']]
    print(df_limpo)
    #endregion


    # # 5.0 Vamos adicionar o nome dos países
    #region
    # paises = pd.read_excel('paises.xlsx', skiprows=6)

    # paises = paises[['CÓDIGO SPED (uso na NF-e)', 'NO_PAIS_POR']]
    # paises = paises.rename(columns={'CÓDIGO SPED (uso na NF-e)': 'cod', 'NO_PAIS_POR': 'PAÍS'})
    # paises = (paises.sort_values('cod', ascending=True))
    # print(paises)
    


    # # 6.0 Criando a coluna códigos pra comparar e testando
    # #region
    # codigos = pd.DataFrame(df_limpo['CO_PAIS'].unique())
    # codigos = codigos.rename(columns={0: 'cod'})
    # codigos = (codigos.sort_values('cod', ascending=True))
    # print(codigos)


    # print(codigos['cod'].corr(paises['cod']))


    # with pd.ExcelWriter('check codigos.xlsx') as w:
    #     codigos[['cod']].to_excel(w, 'aba1', index=False)
    #     paises[['cod']].to_excel(w, 'aba2', index=False)

    


    # # 7.0 Mesclando as colunas
    # #region

    # df_novo = pd.merge(df_limpo, paises, left_on='CO_PAIS', right_on='cod', how='left')
    # print(df_novo)

    # #Ficou uma merda, não ta batendo são códigos diferentes
    #endregion


    # 3.3 Novo Merge
    #region

    print(df_limpo)
    print(tabelas)


    print(df_limpo['CO_PAIS'].unique())
    print(tabelas['SECEX'].unique())

    df_novo = pd.merge(df_limpo, tabelas, left_on='CO_PAIS', right_on='SECEX', how='left')
    print(df_novo)

    df_novo.drop(['CO_URF','SPED', 'SECEX'], axis=1, inplace =True)

    # Agora vamos deixar apenas a NCM buscada
    
    print(df_novo)
    df_novo = df_novo[df_novo['CO_NCM'] == ncm]
    

    print(df_novo)
    #endregion


    # 3.4 PIVOT Table Exportação x Ano
    #region
            
    exp_f[ano] = df_novo.pivot_table(
    values='VL_FOB',
    index='PAIS',
    columns='CO_ANO',
    aggfunc='sum')
        
        
    print(exp_f[ano])
    #endregion


print(type(ano_inicial), ano_inicial)
print(type(ano_final), ano_final)


# 4.0 Agora junta todos em uma coluna
exp_f_todos = (
    pd.concat(exp_f.values(), axis=1)   # junta pelas colunas
      .groupby(level=0, axis=1).sum()   # se repetir coluna do mesmo ano, soma
      .sort_index(axis=1)               # ordena anos
)

exp_f_todos = exp_f_todos.sort_index(ascending=True)

print(exp_f_todos)



