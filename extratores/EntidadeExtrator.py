import pandas as pd
import requests
import psycopg2
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import bindparam, text


from helpers.logging import logger
from helpers.database import db
from helpers.application import app
import models.Microrregiao
import models.Mesorregiao
import models.Municipio
import models.Uf
from models.InstituicaoEnsino import InstituicaoEnsino




def extratorDados(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json()
    dataList =[]
    for municipio in requisicaoJson:
        
        if  municipio.get('microrregiao') is not None:
           
           municipioId = municipio['id']
           microrregiaoId = municipio['microrregiao']['id']
           mesorregiaoId = municipio['microrregiao']['mesorregiao']['id']
           dataList.append({ "co_municipio":municipioId, "co_microrregiao":microrregiaoId, "co_mesorregiao":mesorregiaoId })
        
    return dataList


def armazenar_microdados_educacao(csv_file,chunksize): 
    colList = ['CO_ENTIDADE','NO_ENTIDADE','CO_UF','CO_MUNICIPIO',
        'CO_MESORREGIAO','CO_MICRORREGIAO','QT_MAT_BAS','QT_MAT_INF','QT_MAT_FUND',
        'QT_MAT_MED','QT_MAT_MED_CT','QT_MAT_MED_NM','QT_MAT_PROF','QT_MAT_PROF_TEC','QT_MAT_EJA','QT_MAT_ESP','NU_ANO_CENSO'] 
    
    data = pd.read_csv(csv_file, encoding='latin-1', delimiter=';', usecols = colList, chunksize = chunksize)
    with app.app_context(): 
        try:

            totalRegistros = 0    
            for chunk in data:

                entidades = chunk.fillna(0)
                entidadesDict = entidades.to_dict(orient='records')

                entidades_info = [{
                    'co_entidade': entidade['CO_ENTIDADE'],
                    'no_entidade': entidade['NO_ENTIDADE'],
                    'co_uf': entidade['CO_UF'],
                    'co_municipio': entidade['CO_MUNICIPIO'],
                    'co_mesorregiao': entidade['CO_MESORREGIAO'],
                    'co_microrregiao': entidade['CO_MICRORREGIAO'],
                    'qt_mat_bas': entidade['QT_MAT_BAS'],
                    'qt_mat_inf': entidade['QT_MAT_INF'],
                    'qt_mat_fund': entidade['QT_MAT_FUND'],
                    'qt_mat_med': entidade['QT_MAT_MED'],
                    'qt_mat_med_ct': entidade['QT_MAT_MED_CT'],
                    'qt_mat_med_nm': entidade['QT_MAT_MED_NM'],
                    'qt_mat_prof': entidade['QT_MAT_PROF'],
                    'qt_mat_prof_tec': entidade['QT_MAT_PROF_TEC'],
                    'qt_mat_eja': entidade['QT_MAT_EJA'],
                    'qt_mat_esp': entidade['QT_MAT_ESP'],
                    'nu_ano_censo': entidade['NU_ANO_CENSO'],
                } for entidade in entidadesDict]

                
                stmt = db.insert(InstituicaoEnsino)
                db.session.execute(stmt, entidades_info)


                db.session.commit() 
                totalRegistros += len(entidades_info) 
                


            logger.info(f"Entidades inseridas com sucesso: {totalRegistros} registros")       

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500 
        finally:
            db.session.close()
    

    
def atualizarMicro_e_Meso(dataList):
    with app.app_context(): 
        try:
    
            stmt = (
                text("""
                    UPDATE tb_instituicao_ensino 
                    SET co_microrregiao = :co_microrregiao, 
                        co_mesorregiao = :co_mesorregiao
                    WHERE co_municipio = :co_municipio
                    """)
                
                
            )

            db.session.execute(stmt, dataList)
            db.session.commit()
            logger.info(f"Dados atualizados com sucesso") 

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500 
        except Exception as e:
            db.session.rollback()
            logger.error(f"Exception: {e}")
        finally:
            
            db.session.close()    
    

def removerFk():

    with app.app_context():
        try:
        
            text1 = text('''
                ALTER TABLE tb_instituicao_ensino
                DROP CONSTRAINT tb_instituicao_ensino_co_mesorregiao_fkey;
            ''')
            db.session.execute(text1)

            text2 = text('''
                    ALTER TABLE tb_instituicao_ensino
                    DROP CONSTRAINT tb_instituicao_ensino_co_microrregiao_fkey;
            ''')
            db.session.execute(text2)
                
            db.session.commit()
            logger.info(f"fks de microrregiao e mesorregiao retiradas") 

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro no banco de dados: {e}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro inesperado: {e}")
        
        finally:
            
            db.session.close()   


def adicionarFk():
    with app.app_context():
        try:

            text1 =text('''
                ALTER TABLE tb_instituicao_ensino
                ADD CONSTRAINT tb_instituicao_ensino_co_microrregiao_fkey 
                FOREIGN KEY (co_microrregiao)
                REFERENCES tb_microrregiao(co_microrregiao);
            ''')
            db.session.execute(text1)

            text2 = text('''
                ALTER TABLE tb_instituicao_ensino
                ADD CONSTRAINT tb_instituicao_ensino_co_mesorregiao_fkey
                FOREIGN KEY (co_mesorregiao)
                REFERENCES tb_mesorregiao(co_mesorregiao);
            ''')
            db.session.execute(text2)
                
            db.session.commit()
            logger.info(f"FKs adicionadas") 

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500 
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro inesperado: {e}")
        finally:
            db.session.close() 



def importar_dados_seguro():
    with app.app_context():  
        try:
            
            with db.session.begin():
                
                removerFk()
                
                
                armazenar_microdados_educacao(csv_file2023, 1000)
                armazenar_microdados_educacao(csv_file2024, 1000)
                
               
                atualizarMicro_e_Meso(dataList)
                adicionarFk()
                
                
        except Exception as e:
            logger.error(f"Falha na importação: {str(e)}")
            db.session.rollback()
            
        finally:
            db.session.close()

if __name__ == "__main__":
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    dataList = extratorDados(url)
    
    csv_file2023 = "/mnt/c/Users/Jefferson/Downloads/microdados_ed_basica_2023.csv"
    csv_file2024 = "/mnt/c/Users/Jefferson/Downloads/microdados_ed_basica_2024.csv"
    
    importar_dados_seguro()