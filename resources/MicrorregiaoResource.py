from flask_restful import Resource , marshal
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask import request

from helpers.database import db
from helpers.logging import logger

from models.Microrregiao import Microrregiao, microrregiao_fields, MicrorregiaoSchema


class MicrorregioesResource(Resource):
    def get(self):
        logger.info("Get - Micorregiões")
        try:
            page = request.args.get("page",1, type = int)
            limit = request.args.get("limit",1, type = int)
            offset = (page -1) * limit
    
            stmt = db.select(Microrregiao).limit(limit).offset(offset)
            result = db.session.execute(stmt).scalars()
            microrregioes = result.all()

        except SQLAlchemyError as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
        return marshal(microrregioes, microrregiao_fields), 200


    def post(self):

        logger.info("Post - Micorregião")
        microrregiaoSchema = MicrorregiaoSchema()
        microrregiaoData = request.get_json()
        try:
            microrregiaoJson = microrregiaoSchema.load(microrregiaoData )
            co_microrregiao = microrregiaoJson['co_microrregiao']
            no_microrregiao = microrregiaoJson['no_microrregiao']
            co_uf = microrregiaoJson['co_uf']
            

            microrregiao = microrregiao(co_microrregiao, no_microrregiao, co_uf)

            db.session.add(microrregiao)
            db.session.commit()
            
            return marshal(microrregiao, microrregiao_fields), 200
        
        except SQLAlchemyError as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
        except ValidationError as err:
            return {"mensagem": "Problema na validação."}, 400
        