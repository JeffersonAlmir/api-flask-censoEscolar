import requests
import psycopg2


from helpers.logging import logger
from helpers.database import connectDb

def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 

    municipiosList = []
    for municipio in requisicaoJson:
        
        co_municipio = municipio['id']
        no_municipio = municipio['nome']
        if municipio.get('microrregiao') == None :
            co_uf = municipio['regiao-imediata']['regiao-intermediaria']['UF']['id']
            
        else:   
            co_uf = municipio['microrregiao']['mesorregiao']['UF']['id']
            
        municipiosList.append((co_municipio, no_municipio, co_uf))

    return municipiosList

def armazenarDados(municipiosList):
       
    try:
        connection = connectDb()
        cursor = connection.cursor()
        
        cursor.executemany("""INSERT INTO Municipio(CO_MUNICIPIO, NO_MUNICIPIO, CO_UF) VALUES(%s ,%s, %s);""", municipiosList)
        
        connection.commit()
        logger.info(f"Municípios inseridos com sucesso: {len(municipiosList)} registros")
    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Erro: {e.pgerror}")
    finally:
        cursor.close()
        connection.close()
    

     


if __name__ == "__main__":
    url ='https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    municipiosList = extrator(url)
    armazenarDados(municipiosList)
    