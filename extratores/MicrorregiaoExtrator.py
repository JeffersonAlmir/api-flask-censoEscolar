import requests
import psycopg2
from sqlalchemy.exc import SQLAlchemyError

from helpers.database import db
from helpers.application import app
from helpers.logging import logger
import models.InstituicaoEnsino
import models.Mesorregiao
import models.Municipio
import models.Uf
from models.Microrregiao import Microrregiao


def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    microrregiaoList = [{"co_microrregiao":microrregiao['id'],"no_microrregiao": microrregiao['nome'],
                         "co_uf":microrregiao ['mesorregiao']['UF']['id']} for  microrregiao  in dados]
    
    with app.app_context():
        try:
            stmt = db.insert(Microrregiao)
            db.session.execute(stmt,microrregiaoList)
            db.session.commit()

            logger.info(f"Microrregião inseridas com sucesso: {len(microrregiaoList)} registros")

        except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Erro no banco de dados: {e}")
                return {"mensagem": "Problema com o banco de dados."}, 500 
        finally:
                db.session.close()
    
        


if __name__ == "__main__":

    url ='https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes'
    dados = extrator(url)
    armazenarDados(dados)
    