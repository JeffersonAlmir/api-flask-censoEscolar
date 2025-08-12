import requests
import psycopg2
from sqlalchemy.exc import SQLAlchemyError


from helpers.logging import logger
from helpers.database import db
from helpers.application import app
import models.InstituicaoEnsino
import models.Microrregiao
import models.Municipio
import models.Mesorregiao
from models.Uf import Uf


def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    ufsList = [{"co_uf":uf['id'], "no_uf":uf["nome"], "sg_uf":uf['sigla']} for uf  in dados]
    with app.app_context():
        try:
            stmt = db.insert(Uf)
            db.session.execute(stmt,ufsList)
            db.session.commit()
            
            logger.info(f"UFs inseridos com sucesso: {len(ufsList)} registros")
            
        except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Erro no banco de dados: {e}")
                return {"mensagem": "Problema com o banco de dados."}, 500 
        finally:
             db.session.close()
    
   




if __name__ == "__main__":
    
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    dados = extrator(url)
    armazenarDados(dados)
    
    