import requests
import psycopg2


from helpers.logging import logger
from helpers.database import connectDb



def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    ufsList = [(uf['id'], uf["nome"], uf['sigla']) for uf  in dados]
    try:
        connection = connectDb()
        cursor = connection.cursor()

        cursor.executemany("""INSERT INTO UF(CO_UF ,NO_UF, SG_UF) VALUES(%s ,%s ,%s);""",ufsList)
        
        connection.commit()
        logger.info(f"UFs inseridos com sucesso: {len(ufsList)} registros")

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Erro: {e.pgerror}") 
    finally: 
        cursor.close()
        connection.close()
   




if __name__ == "__main__":
    
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    dados = extrator(url)
    armazenarDados(dados)
    