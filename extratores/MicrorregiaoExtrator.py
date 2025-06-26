import requests
import psycopg2

from helpers.database import connectDb
from helpers.logging import logger


def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    microrregiaoList = [(microrregiao['id'], microrregiao['nome'],
                         microrregiao ['mesorregiao']['UF']['id']) for  microrregiao  in dados]
    try:
        connection = connectDb()
        cursor = connection.cursor()
        
        cursor.executemany("""INSERT INTO Microrregiao(CO_MICRORREGIAO, NO_MICRORREGIAO, CO_UF) VALUES (%s ,%s, %s);""",microrregiaoList)
        
        connection.commit()
        logger.info(f"Microrregião inseridas com sucesso: {len(microrregiaoList)} registros")

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Erro: {e.pgerror}") 
    finally:
        connection.close()
    
        


if __name__ == "__main__":

    url ='https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes'
    dados = extrator(url)
    armazenarDados(dados)
    