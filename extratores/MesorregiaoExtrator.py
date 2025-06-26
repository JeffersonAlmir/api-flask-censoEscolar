import requests
import psycopg2

from helpers.database import connectDb
from helpers.logging import logger

def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    mesorregiaoList = [(mesorregiao['id'], mesorregiao['nome'],
                         mesorregiao['UF']['id']) for mesorregiao  in dados]
    
    try:
        connection = connectDb()
        cursor = connection.cursor()  
        cursor.executemany("""INSERT INTO Mesorregiao(CO_MESORREGIAO, NO_MESORREGIAO, CO_UF) VALUES (%s ,%s, %s);""",mesorregiaoList)
        
        connection.commit()
        logger.info(f"Mesorregião inseridas com sucesso: {len(mesorregiaoList)} registros")

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Erro: {e.pgerror}") 
    finally:
        cursor.close()
        connection.close()
    
        


if __name__ == "__main__":
    url ='https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes'
    dados = extrator(url)
    armazenarDados(dados)
    