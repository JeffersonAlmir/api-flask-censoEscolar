import requests
import psycopg2
from sqlalchemy.exc import SQLAlchemyError

from helpers.database import db
from helpers.application import app
from helpers.logging import logger
import models.InstituicaoEnsino
import models.Microrregiao
import models.Municipio
import models.Uf
from models.Mesorregiao import Mesorregiao

def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    mesorregiaoList = [{"co_mesorregiao":mesorregiao['id'], "no_mesorregiao":mesorregiao['nome'],
                         "co_uf":mesorregiao['UF']['id']} for mesorregiao  in dados]
    with app.app_context():
        try:

            stmt = db.insert(Mesorregiao)
            db.session.execute(stmt,mesorregiaoList)
            db.session.commit()
            
            logger.info(f"Mesorregião inseridas com sucesso: {len(mesorregiaoList)} registros")

        except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Erro no banco de dados: {e}")
                return {"mensagem": "Problema com o banco de dados."}, 500 
        finally:
                db.session.close()


if __name__ == "__main__":
    url ='https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes'
    dados = extrator(url)
    armazenarDados(dados)
    