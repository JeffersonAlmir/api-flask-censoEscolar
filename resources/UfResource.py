from flask_restful import Resource , marshal
import psycopg2

from helpers.database import getConnection
from helpers.logging import logger

from models.Uf import Uf ,uf_fields


class UfResource(Resource):

    def get(self):
        logger.info("Get Ufs")
        try:
            cursor = getConnection().cursor()
            cursor.execute("""
                SELECT uf.co_uf, uf.no_uf, uf.sg_uf from uf 
                ORDER BY uf.no_uf ASC;
            """)
            ufs = cursor.fetchall()  
            

            lista_ufs = [Uf(*uf) for uf in ufs]
            
            return marshal(lista_ufs, uf_fields), 200
            
        except psycopg2.Error as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
        