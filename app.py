from flask import request ,jsonify, g
import sqlite3
from marshmallow import ValidationError

from helpers.application import app
from helpers.database import getConnection
from helpers.CORS import cors
from helpers.logging import logger

from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema


cors.init_app(app)


@app.route("/")
def index():
    versao = {"versao":"0.0.1"}
    return jsonify(versao),200

@app.get("/instituicoes")
def getInstituicoesResource():
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
                LIMIT ? OFFSET ?;''',(limit,offset))


        result = cursor.fetchall()
        instituicoesEnsino = [InstituicaoEnsino(*row).toDict()  for row in result]

    except sqlite3.Error as e:
        logger.error(f"Erro no banco de dados: {e}")
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify(instituicoesEnsino),200



@app.get("/instituicoes/<int:id>")
def getInstituicoesByIdResource(id):
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
                WHERE CO_ENTIDADE = ?;''',(id,))
        row = cursor.fetchone()

        if not row:
            logger.warning(f"Instituição com ID {id} não encontrada.")
            return jsonify({"mensagem":"Instituição de ensino não encontrada."}), 404
        
        instituicaoEnsino = InstituicaoEnsino(*row)
        

    except sqlite3.Error as e:
        logger.error(f"Erro no banco de dados: {e}")
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    
    return jsonify(instituicaoEnsino.toDict()),200



@app.delete("/instituicoes/<int:id>")
def deleteInstituicaoResource(id):
    logger.info("Delete - Instituições")

    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Entidades WHERE CO_ENTIDADE = ?",(id,))
        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Erro no banco de dados: {e}")
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return "", 200


@app.post("/instituicoes")
def createInstituicaoResource():
    logger.info("Post - Instituições")
    
    instituicaoEnsinoSchema = InstituicaoEnsinoSchema()

    try:
        instituicaoData = request.get_json()
        instituicaoJson = instituicaoEnsinoSchema.load(instituicaoData)

        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Entidades WHERE CO_ENTIDADE = ?',(instituicaoJson['co_entidade'],))
        existe = cursor.fetchone()
      
        if existe:
            logger.warning(f"Instituição com ID {instituicaoJson['co_entidade']} já existe no Database.")
            return jsonify({"mensagem":"Instituição de ensino já existe. Cadastro não realizado"}), 406
      
      
        cursor.execute("""
                    INSERT INTO Entidades
                        (CO_ENTIDADE, NO_ENTIDADE, CO_UF, CO_MUNICIPIO, CO_MESORREGIAO, CO_MICRORREGIAO,
                        QT_MAT_BAS, QT_MAT_INF, QT_MAT_FUND, QT_MAT_MED, QT_MAT_MED_CT, QT_MAT_MED_NM, 
                        QT_MAT_PROF, QT_MAT_PROF_TEC, QT_MAT_EJA, QT_MAT_ESP)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );""",
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
 
    except ValidationError as err:
       logger.warning(f"Erro de validação: {err.messages}")
       return jsonify(err.messages), 400

    except sqlite3.Error as e:
        logger.error(f"Erro no banco de dados: {e}")
        return jsonify({"mensagem": "Problema com o banco de dados. "}), 500

    return jsonify(instituicaoEnsino.toDict()),201

# corrigir logica do update ainda acho que ta errado
@app.put("/instituicoes/<int:id>")
def updateInstituicaoResource(id):
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
            return jsonify({"mensagem":"Instituição de ensino não encontrada."}), 404
        
        cursor.execute(""" 
                UPDATE Entidades
                SET NO_ENTIDADE = ?, CO_UF = ?, CO_MUNICIPIO = ?, CO_MESORREGIAO = ?, CO_MICRORREGIAO = ?, QT_MAT_BAS = ?,
                    QT_MAT_INF = ?, QT_MAT_FUND = ?, QT_MAT_MED = ?, QT_MAT_MED_CT = ?, 
                    QT_MAT_MED_NM = ?, QT_MAT_PROF = ?, QT_MAT_PROF_TEC = ?, QT_MAT_EJA = ?, QT_MAT_ESP = ?
                WHERE CO_ENTIDADE = ?;""",  ( instituicaoJson["no_entidade"], instituicaoJson["co_uf"],
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
                WHERE CO_ENTIDADE = ?;''',(id,))
        
        dadosAtualizados = cursor.fetchone()
        
        instituicaoEnsino = InstituicaoEnsino(*dadosAtualizados)
        
        conn.commit()

    except ValidationError as err:
       logger.warning(f"Erro de validação: {err.messages}")
       return jsonify(err.messages), 400

    except sqlite3.Error as e:
        logger.error(f"Erro no banco de dados: {e}")
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify(instituicaoEnsino.toDict()),200

    