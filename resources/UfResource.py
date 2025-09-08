from flask_restful import Resource , marshal
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask import request

from helpers.database import db
from helpers.database import cache
from helpers.logging import logger


from models.Uf import Uf ,uf_fields, UfSchema
from models.InstituicaoEnsino import InstituicaoEnsino
from models.Municipio import Municipio


class UfsResource(Resource):
    def get(self):
        logger.info("Get Ufs")
        try:
            stmt = db.select(Uf).order_by(Uf.no_uf)
            result = db.session.execute(stmt).scalars()
            ufs = result.all()
        except SQLAlchemyError as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
        return marshal(ufs, uf_fields), 200


    def post(self):

        logger.info("Post - Ufs")
        ufSchema = UfSchema()
        ufData = request.get_json()
        try:
            ufJson = ufSchema.load(ufData)
            co_uf = ufJson['co_uf']
            no_uf = ufJson['no_uf']
            sg_uf = ufJson['sg_uf']

            uf = Uf(co_uf, no_uf, sg_uf)
            db.session.add(uf)
            db.session.commit()
            
            return marshal(uf, uf_fields), 200
        
        except SQLAlchemyError as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
        except ValidationError as err:
            return {"mensagem": "Problema na validação."}, 400
        

        
class UfMatriculasResource(Resource):
    def get(self):
        logger.info("Get - Quantidade matriculas por estados")
        try:
            ano_censo = request.args.get("ano", default=2023, type = int)

            cache_key = f"matriculas_por_uf:{ano_censo}"
            cached_data = cache.get(cache_key)
            
            if cached_data:
                logger.info(f"CACHE HIT para a chave {cache_key}")
                return cached_data, 200
            

            logger.info(f"CACHE MISS para a chave {cache_key}")

            stmt = (
                db.select(
                    Uf.no_uf,
                    db.func.sum(InstituicaoEnsino.qt_mat_bas).label("qt_mat_bas"),
                    InstituicaoEnsino.nu_ano_censo
                )
                .select_from(InstituicaoEnsino)
                .join(Uf, InstituicaoEnsino.co_uf == Uf.co_uf)
                .where(InstituicaoEnsino.nu_ano_censo == ano_censo)
                .group_by(InstituicaoEnsino.nu_ano_censo, Uf.no_uf)
            )

            result = db.session.execute(stmt).all()

            lista =[{'estado': data[0],'matriculas': data[1]}for data in result]

            cache.set(cache_key,lista, timeout = 3600)

            return lista, 200

             
        except SQLAlchemyError as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        


class UfQuantidadesResource(Resource):

    def get(self):
        logger.info("Get - Quantidade de município e de matrícula")
        try:
            ano_censo = request.args.get("ano", default=2023, type = int)
            

            cache_key = f"qtd_municipio_matricula:{ano_censo}"
            cached_data = cache.get(cache_key)
            
            if cached_data:
                logger.info(f"CACHE HIT para a chave {cache_key}")
                return cached_data, 200
            

            logger.info(f"CACHE MISS para a chave {cache_key}")

            stmt = (
                db.select(
                    Uf.no_uf,
                    db.func.count(db.distinct(Municipio.co_municipio)).label("total_municipios"),
                    db.func.sum(InstituicaoEnsino.qt_mat_bas).label("qt_mat_bas"),
                )
                .select_from(InstituicaoEnsino)
                .join(Uf, InstituicaoEnsino.co_uf == Uf.co_uf)
                .join(Municipio, InstituicaoEnsino.co_municipio == Municipio.co_municipio)
                .where(InstituicaoEnsino.nu_ano_censo == ano_censo)
                .group_by( Uf.no_uf)
            )

            result = db.session.execute(stmt).all()

            lista =[{'estado': data[0],'total_municipios': data[1] ,'matriculas': data[2] } for data in result]

            cache.set(cache_key,lista, timeout = 3600)
            return lista, 200

             
        except SQLAlchemyError as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500