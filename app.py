from flask import Flask,request ,jsonify
import sqlite3

from flask import Flask,request ,jsonify, g
import sqlite3
from marshmallow import ValidationError

from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema

DATABASE = 'entidades.db'

app = Flask(__name__)

def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
 
@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    versao = {"versao":"0.0.1"}
    return jsonify(versao),200

@app.get("/instituicoes")
def getInstituicoesResource():
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
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify(instituicoesEnsino),200



@app.get("/instituicoes/<int:id>")
def getInstituicoesByIdResource(id):
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
             return jsonify({"mensagem":"Instituição de ensino não encontrada."}), 404
        
        instituicaoEnsino = InstituicaoEnsino(*row)
        

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    
    return jsonify(instituicaoEnsino.toDict()),200



@app.delete("/instituicoes/<int:id>")
def deleteInstituicaoResource(id):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Entidades WHERE CO_ENTIDADE = ?",(id,))
        conn.commit()

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return "", 200


@app.post("/instituicoes")
def createInstituicaoResource():

    instituicaoEnsinoSchema = InstituicaoEnsinoSchema()

    try:
        instituicaoData = request.get_json()
        instituicaoJson = instituicaoEnsinoSchema.load(instituicaoData)
       
        keysList = ['co_entidade', 'no_entidade','co_uf', 'no_uf', 'sg_uf', 'co_municipio', 'no_municipio',
                    'co_mesorregiao', 'no_mesorregiao', 'co_microrregiao', 'no_microrregiao',
                    'qt_mat_bas', 'qt_mat_inf', 'qt_mat_fund', 'qt_mat_med', 'qt_mat_med_ct', 'qt_mat_med_nm',
                    'qt_mat_prof', 'qt_mat_prof_tec', 'qt_mat_eja', 'qt_mat_esp']
        
        instituicao = tuple(instituicaoJson[key] for key in keysList)

        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Entidades WHERE CO_ENTIDADE = ?',(instituicaoJson['co_entidade'],))
        existe = cursor.fetchone()
        
        if existe:
            return jsonify({"mensagem":"Instituição de ensino já existe."}), 409
        
        cursor.execute("""
                    INSERT INTO Entidades
                       (CO_ENTIDADE, NO_ENTIDADE, CO_UF, NO_UF, SG_UF, CO_MUNICIPIO, NO_MUNICIPIO, 
                        CO_MESORREGIAO, NO_MESORREGIAO, CO_MICRORREGIAO, NO_MICRORREGIAO, QT_MAT_BAS, QT_MAT_INF, QT_MAT_FUND,
                        QT_MAT_MED, QT_MAT_MED_CT, QT_MAT_MED_NM, QT_MAT_PROF, QT_MAT_PROF_TEC, QT_MAT_EJA, QT_MAT_ESP)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",instituicao)
        
        instituicaoEnsino = InstituicaoEnsino(*instituicao)
        
        conn.commit()

   
    except ValidationError as err:
        return jsonify(err.messages), 400

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify(instituicaoEnsino.toDict()),201


@app.put("/instituicoes/<int:id>")
def updateInstituicaoResource(id):

    instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
    try:
        instituicaoJson = request.get_json()
        
        keysList = ['co_entidade', 'no_entidade','co_uf', 'no_uf', 'sg_uf', 'co_municipio', 'no_municipio',
                    'co_mesorregiao', 'no_mesorregiao', 'co_microrregiao', 'no_microrregiao',
                    'qt_mat_bas', 'qt_mat_inf', 'qt_mat_fund', 'qt_mat_med', 'qt_mat_med_ct', 'qt_mat_med_nm',
                    'qt_mat_prof', 'qt_mat_prof_tec', 'qt_mat_eja', 'qt_mat_esp']
        
        instituicao = tuple(instituicaoJson[key] for key in keysList)

        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Entidades WHERE CO_ENTIDADE = ?',(id,))
        existe = cursor.fetchone()
        
        if not existe:
            return jsonify({"mensagem":"Instituição de ensino não encontrada."}), 404
        
        cursor.execute(""" 
                UPDATE Entidades
                SET NO_ENTIDADE = ?, CO_UF = ?, SG_UF = ?, CO_MUNICIPIO = ?, 
                    CO_MESORREGIAO = ?,  CO_MICRORREGIAO = ?,  
                    QT_MAT_BAS = ?, QT_MAT_INF = ?, QT_MAT_FUND = ?, QT_MAT_MED = ?, QT_MAT_MED_CT = ?, 
                    QT_MAT_MED_NM = ?, QT_MAT_PROF = ?, QT_MAT_PROF_TEC = ?, QT_MAT_EJA = ?, QT_MAT_ESP = ?
                WHERE CO_ENTIDADE = ?;""", instituicao[1:] + (id,))
        
        instituicaoEnsino = InstituicaoEnsino(*instituicao)
        
        conn.commit()

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify(instituicaoEnsino.toDict()),200

    