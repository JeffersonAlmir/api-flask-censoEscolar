from flask_restful import Resource , marshal
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask import request

from helpers.database import db
from helpers.logging import logger

from models.InstituicaoEnsino import InstituicaoEnsino
from models.Uf import Uf
from models.Municipio import Municipio, municipio_fields, MunicipioSchema


class MunicipiosResource(Resource):
    def get(self):
        logger.info("Get - Municipios")
        try:
            page = request.args.get("page",1, type = int)
            limit = request.args.get("limit",1, type = int)
            offset = (page -1) * limit

            stmt = db.select(Municipio).limit(limit).offset(offset)
            result = db.session.execute(stmt).scalars()
            municipios = result.all()

            return marshal(municipios, municipio_fields), 200
        
        except SQLAlchemyError as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        


    def post(self):

        logger.info("Post Municipio")
        
        municipioSchema = MunicipioSchema()
        municipioData = request.get_json()

        try:
            municipioJson = municipioSchema.load(municipioData )

            co_municipio = municipioJson['co_municipio']
            no_municipio = municipioJson['no_municipio']
            co_uf = municipioJson['co_uf']
            co_mesorregiao = municipioJson['co_mesorregiao']
            co_microrregiao = municipioJson['co_microrregiao']
            

            municipio = Municipio(co_municipio, no_municipio, co_uf, co_mesorregiao ,co_microrregiao )
            
            db.session.add(municipio)
            db.session.commit()
            
            return marshal(municipio, municipio_fields), 200
        
        except SQLAlchemyError as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
        except ValidationError as err:
            return {"mensagem": "Problema na validação."}, 400
        


class MunicipioMatriculasResource(Resource):
    def get(self):
        logger.info("Get Quantidade matriculas por cidade")
        try:
            ano_censo = request.args.get("ano", default=2023, type = int)
            sigla = request.args.get("sigla",'', type = str)
            stmt =(
                db.select(
                    Municipio.co_municipio,
                    db.func.sum(InstituicaoEnsino.qt_mat_bas),
                    Municipio.no_municipio
                )
                .select_from(InstituicaoEnsino)
                .join(Municipio, InstituicaoEnsino.co_municipio == Municipio.co_municipio)
                .join(Uf, Uf.co_uf == InstituicaoEnsino.co_uf)
                .where(
                    InstituicaoEnsino.nu_ano_censo == ano_censo,
                    Uf.sg_uf == sigla
                )
                .group_by(Municipio.co_municipio, Municipio.no_municipio)
            )

            result = db.session.execute(stmt).all()

            lista =[{'co_municipio': data[0],'matriculas': data[1], 'nome_municipio': data[2]}for data in result]
            
            return lista, 200  
        
        except SQLAlchemyError as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        