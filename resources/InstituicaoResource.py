from flask import request
from flask_restful import Resource , marshal
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
import psycopg2

from helpers.database import db
from helpers.logging import logger

from models.Uf import Uf
from models.Municipio import Municipio
from models.InstituicaoEnsino import InstituicaoEnsino, instituicao_fields, InstituicaoEnsinoSchema, ano_fields


class InstituicoesResource(Resource):
    def get(self):
       
        logger.info("Get - Instituições")

        try:
            page = request.args.get("page",1, type = int)
            limit = request.args.get("limit",1, type = int)
            offset = (page -1) * limit
    
            stmt = db.select(InstituicaoEnsino).limit(limit).offset(offset)
            result = db.session.execute(stmt).scalars()
            instituicoes = result.all()
            return marshal(instituicoes, instituicao_fields),200
        
        except SQLAlchemyError as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500

    

    def post(self):
        logger.info("Post - Instituições")
    
        instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
        instituicaoData = request.get_json()

        try:
            instituicaoJson = instituicaoEnsinoSchema.load(instituicaoData) 

            subquery = db.select(InstituicaoEnsino.co_entidade).where(InstituicaoEnsino.co_entidade == instituicaoJson["co_entidade"]).exists()
            stmt = db.select(subquery)
            result = db.session.execute(stmt)
            existInstituicao = result.scalar()
        
            if existInstituicao:
                logger.warning(f"Instituição com ID {instituicaoJson['co_entidade']} já existe no Database.")
                return {"mensagem":"Instituição de ensino já existe. Cadastro não realizado"}, 406
        
        
            co_entidade = instituicaoJson["co_entidade"]
            no_entidade = instituicaoJson["no_entidade"]
            co_uf = instituicaoJson["co_uf"]
            co_municipio = instituicaoJson["co_municipio"]
            co_mesorregiao = instituicaoJson["co_mesorregiao"]
            co_microrregiao = instituicaoJson["co_microrregiao"]
            qt_mat_bas = instituicaoJson["qt_mat_bas"]
            qt_mat_inf = instituicaoJson["qt_mat_inf"]
            qt_mat_fund = instituicaoJson["qt_mat_fund"]
            qt_mat_med = instituicaoJson["qt_mat_med"]
            qt_mat_med_ct = instituicaoJson["qt_mat_med_ct"]
            qt_mat_med_nm = instituicaoJson["qt_mat_med_nm"]
            qt_mat_prof = instituicaoJson["qt_mat_prof"]
            qt_mat_prof_tec = instituicaoJson["qt_mat_prof_tec"]
            qt_mat_eja = instituicaoJson["qt_mat_eja"]
            qt_mat_esp = instituicaoJson["qt_mat_esp"]
            nu_ano_censo = instituicaoJson["qt_mat_esp"]

            instituicao = InstituicaoEnsino(
                co_entidade,
                no_entidade,
                co_uf,
                co_municipio,
                co_mesorregiao ,
                co_microrregiao,
                qt_mat_bas,
                qt_mat_inf,
                qt_mat_fund,
                qt_mat_med,
                qt_mat_med_ct,
                qt_mat_med_nm,
                qt_mat_prof,
                qt_mat_prof_tec,
                qt_mat_eja,
                qt_mat_esp,
                nu_ano_censo
            )

            db.session.add(instituicao)
            db.session.commit()

            return marshal(instituicao, instituicao_fields),201   
    
        except ValidationError as err:
            logger.warning(f"Erro de validação: {err.messages}")
            return {"mensagem": "Problema com a validação. " +err. messages},400

        except SQLAlchemyError as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
    # def get():
    #     logger.info("Get Ano")
    #     try:

    #         cursor = getConnection().cursor()
    #         cursor.execute("""
    #             SELECT DISTINCT e.ano_censo FROM entidades e
    #             ORDER BY e.ano_censo DESC;
    #         """)

    #         anos = [ano for ano in cursor.fetchall()]
    #         return {"anos": anos}
        
    #     except psycopg2.Error as e:  
    #         logger.error(f"Erro no banco de dados: {e}")
    #         return {"mensagem": "Problema com o banco de dados."}, 500




# class InstituicaoResource(Resource):

#     def get(self,id):
#         logger.info("Get por Id - Instituições")

#         try:
#             cursor = getConnection().cursor()
#             cursor.execute('''
#                     SELECT 
#                         e.CO_ENTIDADE,
#                         e.NO_ENTIDADE,
#                         e.CO_UF,
#                         u.NO_UF,
#                         u.SG_UF,
#                         e.CO_MUNICIPIO,
#                         m.NO_MUNICIPIO,
#                         e.CO_MESORREGIAO,
#                         meso.NO_MESORREGIAO, 
#                         e.CO_MICRORREGIAO,
#                         micro.NO_MICRORREGIAO,
#                         e.QT_MAT_BAS,
#                         e.QT_MAT_INF,
#                         e.QT_MAT_FUND,
#                         e.QT_MAT_MED,
#                         e.QT_MAT_MED_CT,
#                         e.QT_MAT_MED_NM,
#                         e.QT_MAT_PROF,
#                         e.QT_MAT_PROF_TEC,
#                         e.QT_MAT_EJA,
#                         e.QT_MAT_ESP
#                     FROM Entidades e 
#                     JOIN UF u ON e.CO_UF = u.CO_UF
#                     JOIN  Municipio m  ON e.CO_MUNICIPIO  = m.CO_MUNICIPIO 
#                     JOIN Mesorregiao meso ON e.CO_MESORREGIAO  = meso.CO_MESORREGIAO 
#                     JOIN Microrregiao micro  ON e.CO_MICRORREGIAO  = micro.CO_MICRORREGIAO 
#                     WHERE CO_ENTIDADE = %s;''',(id,))
#             row = cursor.fetchone()

#             if not row:
#                 logger.warning(f"Instituição com ID {id} não encontrada.")
#                 return {"mensagem":"Instituição de ensino não encontrada."}, 404
            
#             instituicaoEnsino = InstituicaoEnsino(*row)
            
#             return marshal(instituicaoEnsino, instituicao_fields),200

#         except psycopg2.Error as e:  
#             logger.error(f"Erro no banco de dados: {e}")
#             return {"mensagem": "Problema com o banco de dados."}, 500
        
    
    
#     def put(self, id):
#         logger.info("Put - Instituições")

#         instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
#         try:
#             instituicaoData = request.get_json()
#             instituicaoJson = instituicaoEnsinoSchema.load(instituicaoData)
            
#             conn = getConnection()
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM Entidades WHERE CO_ENTIDADE = ?',(id,))
#             existe = cursor.fetchone()
            
#             if not existe:
#                 logger.warning(f"Instituição com ID {id} não encontrada.")
#                 return {"mensagem":"Instituição de ensino não encontrada."}, 404
            
#             cursor.execute(""" 
#                     UPDATE Entidades
#                     SET NO_ENTIDADE = %s, CO_UF = %s, CO_MUNICIPIO = %s, CO_MESORREGIAO = %s, CO_MICRORREGIAO = %s, QT_MAT_BAS = %s,
#                         QT_MAT_INF = %s, QT_MAT_FUND = %s, QT_MAT_MED = %s, QT_MAT_MED_CT = %s, 
#                         QT_MAT_MED_NM = %s, QT_MAT_PROF = %s, QT_MAT_PROF_TEC = %s, QT_MAT_EJA = %s, QT_MAT_ESP = %s
#                     WHERE CO_ENTIDADE = %s;""",  ( instituicaoJson["no_entidade"], instituicaoJson["co_uf"],
#                         instituicaoJson["co_municipio"], instituicaoJson["co_mesorregiao"], instituicaoJson["co_microrregiao"],
#                         instituicaoJson["qt_mat_bas"], instituicaoJson["qt_mat_inf"], instituicaoJson["qt_mat_fund"],
#                         instituicaoJson["qt_mat_med"], instituicaoJson["qt_mat_med_ct"], instituicaoJson["qt_mat_med_nm"],
#                         instituicaoJson["qt_mat_prof"], instituicaoJson["qt_mat_prof_tec"], instituicaoJson["qt_mat_eja"], 
#                         instituicaoJson["qt_mat_esp"],id ) )
            
#             cursor.execute('''
#                     SELECT 
#                         e.CO_ENTIDADE,
#                         e.NO_ENTIDADE,
#                         e.CO_UF,
#                         u.NO_UF,
#                         u.SG_UF,
#                         e.CO_MUNICIPIO,
#                         m.NO_MUNICIPIO,
#                         e.CO_MESORREGIAO,
#                         meso.NO_MESORREGIAO, 
#                         e.CO_MICRORREGIAO,
#                         micro.NO_MICRORREGIAO,
#                         e.QT_MAT_BAS,
#                         e.QT_MAT_INF,
#                         e.QT_MAT_FUND,
#                         e.QT_MAT_MED,
#                         e.QT_MAT_MED_CT,
#                         e.QT_MAT_MED_NM,
#                         e.QT_MAT_PROF,
#                         e.QT_MAT_PROF_TEC,
#                         e.QT_MAT_EJA,
#                         e.QT_MAT_ESP
#                     FROM Entidades e 
#                     JOIN UF u ON e.CO_UF = u.CO_UF
#                     JOIN  Municipio m  ON e.CO_MUNICIPIO  = m.CO_MUNICIPIO 
#                     JOIN Mesorregiao meso ON e.CO_MESORREGIAO  = meso.CO_MESORREGIAO 
#                     JOIN Microrregiao micro  ON e.CO_MICRORREGIAO  = micro.CO_MICRORREGIAO 
#                     WHERE CO_ENTIDADE = %s;''',(id,))
            
#             dadosAtualizados = cursor.fetchone()
            
#             instituicaoEnsino = InstituicaoEnsino(*dadosAtualizados)
            
#             conn.commit()

#             return marshal(instituicaoEnsino, instituicao_fields),200

#         except ValidationError as err:
#             logger.warning(f"Erro de validação: {err.messages}")
#             return {"mensagem": "Problema com a validação. " + err. messages},400

#         except psycopg2.Error as e:  
#             logger.error(f"Erro no banco de dados: {e}")
#             return {"mensagem": "Problema com o banco de dados."}, 500



#     def delete(self,id):
#         logger.info("Delete - Instituições")

#         try:
#             conn = getConnection()
#             cursor = conn.cursor()
#             cursor.execute("DELETE FROM Entidades WHERE CO_ENTIDADE = %s",(id,))
#             conn.commit()

#             return {"mensagem": "Removido com sucesso."}, 200
        
#         except psycopg2.Error as e:  
#             logger.error(f"Erro no banco de dados: {e}")
#             return {"mensagem": "Problema com o banco de dados."}, 500

    
    
    
class InstituicoesAno(Resource):
    def get(self):
        logger.info("Get Anos censo")
        try:
            
            stmt = db.select(InstituicaoEnsino.nu_ano_censo).distinct().order_by(InstituicaoEnsino.nu_ano_censo.desc())
            result = db.session.execute(stmt).scalars().all()
            anos = [{'nu_ano_censo': ano} for ano in result]
           
            
            return marshal(anos, ano_fields), 200

           
        
        except ValidationError as err:
            logger.warning(f"Erro de validação: {err.messages}")
            return {"mensagem": "Problema com a validação. " + err. messages},400

        except SQLAlchemyError as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        


# class InstituicoesPorCidadeResource(Resource):
#     def get(self):
#         logger.info("Get Quantidade matriculas por cidade")
#         try:
#             ano_censo = request.args.get("ano", default=2023, type = int)
#             sigla = request.args.get("sigla",'', type = str)

#             cursor = getConnection().cursor()
#             cursor.execute("""
#                 SELECT m.co_municipio, SUM(e.qt_mat_bas), m.no_municipio
#                 FROM entidades e
#                 JOIN municipio m ON e.co_municipio = m.co_municipio
#                 JOIN uf u ON u.co_uf = e.co_uf 
#                 WHERE e.ano_censo = %s and  u.sg_uf = %s
#                 GROUP BY m.co_municipio,  m.no_municipio;
#             """,(ano_censo,sigla))
#             requisicoesData = cursor.fetchall()
#             lista =[{'co_municipio': data[0],'matriculas': data[1], 'nome_municipio': data[2]}for data in requisicoesData]
            
#             return lista, 200  
        
#         except psycopg2.Error as e:  
#             logger.error(f"Erro no banco de dados: {e}")
#             return {"mensagem": "Problema com o banco de dados."}, 500