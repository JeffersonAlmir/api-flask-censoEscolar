import requests
import psycopg2
from sqlalchemy.exc import SQLAlchemyError


from helpers.logging import logger
from helpers.database import db
from helpers.application import app
import models.InstituicaoEnsino
import models.Mesorregiao
import models.Microrregiao
import models.Uf
from models.Municipio import Municipio

def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 

    municipiosList = []
    for municipio in requisicaoJson:
        
        co_municipio = municipio['id']
        no_municipio = municipio['nome']
       

        if municipio.get('microrregiao') == None :
            co_uf = municipio['regiao-imediata']['regiao-intermediaria']['UF']['id']
            if co_uf == 51:
                co_mesorregiao = 5101
                co_microrregiao = 51006
            
        else:   
            co_uf = municipio['microrregiao']['mesorregiao']['UF']['id']
            co_mesorregiao = municipio ['microrregiao'] ['mesorregiao']['id']
            co_microrregiao = municipio ['microrregiao'] ['id']
            
        municipiosList.append({"co_municipio":co_municipio, "no_municipio":no_municipio,"co_uf":co_uf,
                               "co_mesorregiao":co_mesorregiao, "co_microrregiao":co_microrregiao})

    return municipiosList

def armazenarDados(municipiosList):
    with app.app_context():  
        try:
            stmt = db.insert(Municipio)
            db.session.execute(stmt,municipiosList)
            db.session.commit()
            
            logger.info(f"Municípios inseridos com sucesso: {len(municipiosList)} registros")
        except SQLAlchemyError as e:
                    db.session.rollback()
                    logger.error(f"Erro no banco de dados: {e}")
                    return {"mensagem": "Problema com o banco de dados."}, 500 
        finally:
                db.session.close()
    

     


if __name__ == "__main__":
    url ='https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    municipiosList = extrator(url)
    armazenarDados(municipiosList)
    