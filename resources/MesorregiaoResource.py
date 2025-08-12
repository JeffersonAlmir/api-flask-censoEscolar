from flask_restful import Resource , marshal
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask import request

from helpers.database import db
from helpers.logging import logger

from models.Mesorregiao import Mesorregiao, mesorregiao_fields, MesorregiaoSchema


class MesorregioesResource(Resource):
    def get(self):
        logger.info("Get - Mesorregiões")
        try:

            page = request.args.get("page",1, type = int)
            limit = request.args.get("limit",1, type = int)
            offset = (page -1) * limit

            stmt = db.select(Mesorregiao).limit(limit).offset(offset)
            result = db.session.execute(stmt).scalars()
            mesorregioes = result.all()

        except SQLAlchemyError as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
        return marshal(mesorregioes, mesorregiao_fields), 200


    def post(self):

        logger.info("Post Mesorregião")
        mesorregiaoSchema = MesorregiaoSchema()
        mesorregiaoData = request.get_json()
        try:
            mesorregiaoJson = mesorregiaoSchema.load(mesorregiaoData)
            co_mesorregiao = mesorregiaoJson['co_mesorregiao']
            no_mesorregiao = mesorregiaoJson['no_mesorregiao']
            co_uf = mesorregiaoJson['co_uf']
            

            mesorregiao = Mesorregiao(co_mesorregiao, no_mesorregiao, co_uf)
            db.session.add(mesorregiao)
            db.session.commit()
            
            return marshal(mesorregiao, mesorregiao_fields), 200
        
        except SQLAlchemyError as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
        except ValidationError as err:
            return {"mensagem": "Problema na validação."}, 400
        