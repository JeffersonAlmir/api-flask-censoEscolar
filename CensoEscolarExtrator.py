import pandas as pd
import sqlite3
import requests

def extratorDados(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json()
    dataList = [(municipio['microrregiao']['id'], municipio['microrregiao']['mesorregiao']['id'],municipio['id'],) for municipio in requisicaoJson]
    return dataList


def processar_microdados_educacao(csv_file, filtro_coluna, valor_filtro):

    colList = ['CO_ENTIDADE','NO_ENTIDADE','CO_REGIAO','CO_UF','CO_MUNICIPIO',
        'CO_MESORREGIAO','CO_MICRORREGIAO','QT_MAT_BAS','QT_MAT_INF','QT_MAT_FUND',
        'QT_MAT_MED','QT_MAT_MED_CT','QT_MAT_MED_NM','QT_MAT_PROF','QT_MAT_PROF_TEC','QT_MAT_EJA','QT_MAT_ESP']
    
    data = pd.read_csv(csv_file, encoding='latin-1', delimiter=';', usecols = colList)
    filtro_data = data[data[filtro_coluna]==(valor_filtro)].fillna(0)

    entidades = filtro_data.to_dict(orient='records')

    entidades_info = [(entidade['CO_ENTIDADE'], entidade['NO_ENTIDADE'], entidade['CO_UF'] , entidade['CO_MUNICIPIO'], 
                       entidade['CO_MESORREGIAO'], entidade['CO_MICRORREGIAO'],entidade['QT_MAT_BAS'],entidade['QT_MAT_INF'],
                       entidade['QT_MAT_FUND'],entidade['QT_MAT_MED'],entidade['QT_MAT_MED_CT'],entidade['QT_MAT_MED_NM'],
                       entidade['QT_MAT_PROF'],entidade['QT_MAT_PROF_TEC'],entidade['QT_MAT_EJA'],entidade['QT_MAT_ESP']
                        ) for entidade in entidades]

    return entidades_info 


def armazenar_microdados_educacao(database, entidades_info):  
    try:
            #passo1
        connection = sqlite3.connect(database)
            
            #passo2
        cursor = connection.cursor() 
            
            #passo3
        with open('schemas/entidadeSchema.sql') as file:
            cursor.executescript(file.read())

            
        cursor.executemany(
        """INSERT INTO Entidades (
            CO_ENTIDADE, NO_ENTIDADE, CO_UF, CO_MUNICIPIO,
            CO_MESORREGIAO, CO_MICRORREGIAO, QT_MAT_BAS, QT_MAT_INF, 
            QT_MAT_FUND, QT_MAT_MED, QT_MAT_MED_CT, QT_MAT_MED_NM, QT_MAT_PROF, QT_MAT_PROF_TEC, 
            QT_MAT_EJA, QT_MAT_ESP
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,entidades_info)  
            
            #passo4
        connection.commit()        

    except sqlite3.Error as e:
        return e
    finally:   
        connection.close()

    return len(entidades_info)

    
def atualizarMicro_e_Meso(database, dataList):
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.executemany(
            '''UPDATE Entidades
                SET CO_MICRORREGIAO = ?, CO_MESORREGIAO = ?
                WHERE CO_MUNICIPIO = ?; ''',dataList)
        connection.commit()
    except sqlite3.Error as e:
        print( e)
    finally:
        connection.close()    
    


if __name__ == "__main__": 
    
    csv_file = "C:/Users/Jefferson/Documents/microdados_ed_basica_2024.csv"
    filtro_coluna ="CO_REGIAO"
    valor_filtro = 2
    database = 'entidades.db'

    entidates_info = processar_microdados_educacao(csv_file,filtro_coluna, valor_filtro)
    totalInstituicoes = armazenar_microdados_educacao(database, entidates_info)
    print(f"Operação finalizada! Foram cadastradas {totalInstituicoes} Entidades.")

    url ='https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/municipios'
    dataList = extratorDados(url)
    totalUpdate = atualizarMicro_e_Meso(database , dataList)
    print('concluido')




