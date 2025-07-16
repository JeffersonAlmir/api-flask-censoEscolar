from flask import request
from flask_restful import Resource , marshal
import sqlite3
from marshmallow import ValidationError
import psycopg2

from helpers.database import getConnection
from helpers.logging import logger

from models.InstituicaoEnsino import InstituicaoEnsino, instituicao_fields, InstituicaoEnsinoSchema


class InstituicoesResource(Resource):
    def get(self):
       
        logger.info("Get - Instituições")

        try:
            page = request.args.get("page",1, type = int)
            limit = request.args.get("limit",1, type = int)
            offset = (page -1) * limit
    
            cursor = getConnection().cursor()

            cursor.execute('''
                    SELECT 
                        e.CO_ENTIDADE,
                        e.NO_ENTIDADE,
                        e.CO_UF,
                        u.NO_UF,
                        u.SG_UF,
                        e.CO_MUNICIPIO,
                        m.NO_MUNICIPIO,
                        e.CO_MESORREGIAO,
                        meso.NO_MESORREGIAO, 
                        e.CO_MICRORREGIAO,
                        micro.NO_MICRORREGIAO,
                        e.QT_MAT_BAS,
                        e.QT_MAT_INF,
                        e.QT_MAT_FUND,
                        e.QT_MAT_MED,
                        e.QT_MAT_MED_CT,
                        e.QT_MAT_MED_NM,
                        e.QT_MAT_PROF,
                        e.QT_MAT_PROF_TEC,
                        e.QT_MAT_EJA,
                        e.QT_MAT_ESP
                    FROM Entidades e 
                    JOIN UF u ON e.CO_UF = u.CO_UF
                    JOIN  Municipio m  ON e.CO_MUNICIPIO  = m.CO_MUNICIPIO 
                    JOIN Mesorregiao meso ON e.CO_MESORREGIAO  = meso.CO_MESORREGIAO 
                    JOIN Microrregiao micro  ON e.CO_MICRORREGIAO  = micro.CO_MICRORREGIAO 
                    LIMIT %s OFFSET %s;''',(limit,offset))


            result = cursor.fetchall()
            instituicoesEnsino = [InstituicaoEnsino(*row) for row in result]

            return marshal(instituicoesEnsino, instituicao_fields),200
        
        except psycopg2.Error as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500

    

    def post(self):
        logger.info("Post - Instituições")
    
        instituicaoEnsinoSchema = InstituicaoEnsinoSchema()

        try:
            instituicaoData = request.get_json()
            instituicaoJson = instituicaoEnsinoSchema.load(instituicaoData)

            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Entidades WHERE CO_ENTIDADE = %s',(instituicaoJson['co_entidade'],))
            existe = cursor.fetchone()
        
            if existe:
                logger.warning(f"Instituição com ID {instituicaoJson['co_entidade']} já existe no Database.")
                return {"mensagem":"Instituição de ensino já existe. Cadastro não realizado"}, 406
        
        
            cursor.execute("""
                        INSERT INTO Entidades
                            (CO_ENTIDADE, NO_ENTIDADE, CO_UF, CO_MUNICIPIO, CO_MESORREGIAO, CO_MICRORREGIAO,
                            QT_MAT_BAS, QT_MAT_INF, QT_MAT_FUND, QT_MAT_MED, QT_MAT_MED_CT, QT_MAT_MED_NM, 
                            QT_MAT_PROF, QT_MAT_PROF_TEC, QT_MAT_EJA, QT_MAT_ESP)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );""",
                    (instituicaoJson["co_entidade"], instituicaoJson["no_entidade"], instituicaoJson["co_uf"],
                        instituicaoJson["co_municipio"], instituicaoJson["co_mesorregiao"], instituicaoJson["co_microrregiao"],
                        instituicaoJson["qt_mat_bas"], instituicaoJson["qt_mat_inf"], instituicaoJson["qt_mat_fund"],
                        instituicaoJson["qt_mat_med"], instituicaoJson["qt_mat_med_ct"], instituicaoJson["qt_mat_med_nm"],
                        instituicaoJson["qt_mat_prof"], instituicaoJson["qt_mat_prof_tec"], instituicaoJson["qt_mat_eja"], 
                        instituicaoJson["qt_mat_esp"]
                        ))


            instituicaoEnsino = InstituicaoEnsino(instituicaoJson["co_entidade"], instituicaoJson["no_entidade"], instituicaoJson["co_uf"],
                        instituicaoJson["no_uf"], instituicaoJson["sg_uf"],instituicaoJson["co_municipio"], instituicaoJson["no_municipio"] ,
                        instituicaoJson["co_mesorregiao"], instituicaoJson["no_mesorregiao"], instituicaoJson["co_microrregiao"],
                        instituicaoJson["no_microrregiao"], instituicaoJson["qt_mat_bas"], instituicaoJson["qt_mat_inf"], 
                        instituicaoJson["qt_mat_fund"], instituicaoJson["qt_mat_med"], instituicaoJson["qt_mat_med_ct"], 
                        instituicaoJson["qt_mat_med_nm"], instituicaoJson["qt_mat_prof"], instituicaoJson["qt_mat_prof_tec"], 
                        instituicaoJson["qt_mat_eja"], instituicaoJson["qt_mat_esp"])
        
            conn.commit()
            return marshal(instituicaoEnsino, instituicao_fields),201   
    
        except ValidationError as err:
            logger.warning(f"Erro de validação: {err.messages}")
            return {"mensagem": "Problema com a validação. " +err. messages},400

        except sqlite3.Error as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados. "}, 500
        
    def get():
        logger.info("Get Ano")
        try:

            cursor = getConnection().cursor()
            cursor.execute("""
                SELECT DISTINCT e.ano_censo FROM entidades e
                ORDER BY e.ano_censo DESC;
            """)

            anos = [ano for ano in cursor.fetchall()]
            return {"anos": anos}
        
        except psycopg2.Error as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500




class InstituicaoResource(Resource):

    def get(self,id):
        logger.info("Get Id - Instituições")

        try:
            cursor = getConnection().cursor()
            cursor.execute('''
                    SELECT 
                        e.CO_ENTIDADE,
                        e.NO_ENTIDADE,
                        e.CO_UF,
                        u.NO_UF,
                        u.SG_UF,
                        e.CO_MUNICIPIO,
                        m.NO_MUNICIPIO,
                        e.CO_MESORREGIAO,
                        meso.NO_MESORREGIAO, 
                        e.CO_MICRORREGIAO,
                        micro.NO_MICRORREGIAO,
                        e.QT_MAT_BAS,
                        e.QT_MAT_INF,
                        e.QT_MAT_FUND,
                        e.QT_MAT_MED,
                        e.QT_MAT_MED_CT,
                        e.QT_MAT_MED_NM,
                        e.QT_MAT_PROF,
                        e.QT_MAT_PROF_TEC,
                        e.QT_MAT_EJA,
                        e.QT_MAT_ESP
                    FROM Entidades e 
                    JOIN UF u ON e.CO_UF = u.CO_UF
                    JOIN  Municipio m  ON e.CO_MUNICIPIO  = m.CO_MUNICIPIO 
                    JOIN Mesorregiao meso ON e.CO_MESORREGIAO  = meso.CO_MESORREGIAO 
                    JOIN Microrregiao micro  ON e.CO_MICRORREGIAO  = micro.CO_MICRORREGIAO 
                    WHERE CO_ENTIDADE = %s;''',(id,))
            row = cursor.fetchone()

            if not row:
                logger.warning(f"Instituição com ID {id} não encontrada.")
                return {"mensagem":"Instituição de ensino não encontrada."}, 404
            
            instituicaoEnsino = InstituicaoEnsino(*row)
            

        except sqlite3.Error as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
        return marshal(instituicaoEnsino, instituicao_fields),200
    
    
    def put(self, id):
        logger.info("Put - Instituições")

        instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
        try:
            instituicaoData = request.get_json()
            instituicaoJson = instituicaoEnsinoSchema.load(instituicaoData)
            
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Entidades WHERE CO_ENTIDADE = ?',(id,))
            existe = cursor.fetchone()
            
            if not existe:
                logger.warning(f"Instituição com ID {id} não encontrada.")
                return {"mensagem":"Instituição de ensino não encontrada."}, 404
            
            cursor.execute(""" 
                    UPDATE Entidades
                    SET NO_ENTIDADE = %s, CO_UF = %s, CO_MUNICIPIO = %s, CO_MESORREGIAO = %s, CO_MICRORREGIAO = %s, QT_MAT_BAS = %s,
                        QT_MAT_INF = %s, QT_MAT_FUND = %s, QT_MAT_MED = %s, QT_MAT_MED_CT = %s, 
                        QT_MAT_MED_NM = %s, QT_MAT_PROF = %s, QT_MAT_PROF_TEC = %s, QT_MAT_EJA = %s, QT_MAT_ESP = %s
                    WHERE CO_ENTIDADE = %s;""",  ( instituicaoJson["no_entidade"], instituicaoJson["co_uf"],
                        instituicaoJson["co_municipio"], instituicaoJson["co_mesorregiao"], instituicaoJson["co_microrregiao"],
                        instituicaoJson["qt_mat_bas"], instituicaoJson["qt_mat_inf"], instituicaoJson["qt_mat_fund"],
                        instituicaoJson["qt_mat_med"], instituicaoJson["qt_mat_med_ct"], instituicaoJson["qt_mat_med_nm"],
                        instituicaoJson["qt_mat_prof"], instituicaoJson["qt_mat_prof_tec"], instituicaoJson["qt_mat_eja"], 
                        instituicaoJson["qt_mat_esp"],id ) )
            
            cursor.execute('''
                    SELECT 
                        e.CO_ENTIDADE,
                        e.NO_ENTIDADE,
                        e.CO_UF,
                        u.NO_UF,
                        u.SG_UF,
                        e.CO_MUNICIPIO,
                        m.NO_MUNICIPIO,
                        e.CO_MESORREGIAO,
                        meso.NO_MESORREGIAO, 
                        e.CO_MICRORREGIAO,
                        micro.NO_MICRORREGIAO,
                        e.QT_MAT_BAS,
                        e.QT_MAT_INF,
                        e.QT_MAT_FUND,
                        e.QT_MAT_MED,
                        e.QT_MAT_MED_CT,
                        e.QT_MAT_MED_NM,
                        e.QT_MAT_PROF,
                        e.QT_MAT_PROF_TEC,
                        e.QT_MAT_EJA,
                        e.QT_MAT_ESP
                    FROM Entidades e 
                    JOIN UF u ON e.CO_UF = u.CO_UF
                    JOIN  Municipio m  ON e.CO_MUNICIPIO  = m.CO_MUNICIPIO 
                    JOIN Mesorregiao meso ON e.CO_MESORREGIAO  = meso.CO_MESORREGIAO 
                    JOIN Microrregiao micro  ON e.CO_MICRORREGIAO  = micro.CO_MICRORREGIAO 
                    WHERE CO_ENTIDADE = %s;''',(id,))
            
            dadosAtualizados = cursor.fetchone()
            
            instituicaoEnsino = InstituicaoEnsino(*dadosAtualizados)
            
            conn.commit()

        except ValidationError as err:
            logger.warning(f"Erro de validação: {err.messages}")
            return {"mensagem": "Problema com a validação. " + err. messages},400

        except sqlite3.Error as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500

        return marshal(instituicaoEnsino, instituicao_fields),200


    def delete(self,id):
        logger.info("Delete - Instituições")

        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Entidades WHERE CO_ENTIDADE = %s",(id,))
            conn.commit()

        except sqlite3.Error as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500

        return {"mensagem": "Removido com sucesso."}, 200
    
    
    
class InstituicoesConsultaResource(Resource):
    def get(self):
        logger.info("Get Ano")
        try:

            cursor = getConnection().cursor()
            cursor.execute("""
                SELECT DISTINCT e.ano_censo FROM entidades e
                ORDER BY e.ano_censo DESC;
            """)
            anos = cursor.fetchall()
            lista_anos = [{"ano": ano[0]} for ano in anos]
            
            return lista_anos, 200  
        
        except psycopg2.Error as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        

class InstituicoesConsultaPorAnoResource(Resource):
    def get(self):
        logger.info("Get Quantidade matriculas")
        try:
            ano_censo = request.args.get("ano", default=2023, type = int)

            cursor = getConnection().cursor()
            cursor.execute("""
                SELECT  
                uf.no_uf, 
                SUM(qt_mat_bas) AS qt_mat_bas, 
                e.ano_censo 
                FROM entidades e
                JOIN uf ON e.co_uf = uf.co_uf
                WHERE e.ano_censo = %s
                GROUP BY  e.ano_censo, uf.no_uf ;
            """,(ano_censo,))
            requisicoesData = cursor.fetchall()
            lista =[{'estado': data[0],'matriculas': data[1]}for data in requisicoesData]
            
            return lista, 200  
        
        except psycopg2.Error as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        
class InstituicoesPorCidadeResource(Resource):
    def get(self):
        logger.info("Get Quantidade matriculas por cidade")
        try:
            ano_censo = request.args.get("ano", default=2023, type = int)
            sigla = request.args.get("sigla",'', type = str)

            cursor = getConnection().cursor()
            cursor.execute("""
                SELECT m.no_municipio, SUM(e.qt_mat_bas), u.sg_uf
                FROM entidades e
                JOIN municipio m ON e.co_municipio = m.co_municipio
                JOIN uf u ON u.co_uf = e.co_uf 
                WHERE e.ano_censo = %s and  u.sg_uf = %s
                GROUP BY m.no_municipio, u.sg_uf;
            """,(ano_censo,sigla))
            requisicoesData = cursor.fetchall()
            lista =[{'cidade': data[0],'matriculas': data[1]}for data in requisicoesData]
            
            return lista, 200  
        
        except psycopg2.Error as e:  
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500