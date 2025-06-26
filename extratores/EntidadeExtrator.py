import pandas as pd
import requests
import psycopg2


from helpers.logging import logger
from helpers.database import connectDb




def extratorDados(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json()
    dataList =[]
    for municipio in requisicaoJson:
        
        if  municipio.get('microrregiao') is not None:
           
           municipioId = municipio['id']
           microrregiaoId = municipio['microrregiao']['id']
           mesorregiaoId = municipio['microrregiao']['mesorregiao']['id']
           dataList.append(( microrregiaoId,  mesorregiaoId, municipioId ))
        
    #dataList = [(municipio['microrregiao']['id'], municipio['microrregiao']['mesorregiao']['id'], municipio['id'],) for municipio in requisicaoJson]
    return dataList


def armazenar_microdados_educacao(csv_file,chunksize): 
    colList = ['CO_ENTIDADE','NO_ENTIDADE','CO_UF','CO_MUNICIPIO',
        'CO_MESORREGIAO','CO_MICRORREGIAO','QT_MAT_BAS','QT_MAT_INF','QT_MAT_FUND',
        'QT_MAT_MED','QT_MAT_MED_CT','QT_MAT_MED_NM','QT_MAT_PROF','QT_MAT_PROF_TEC','QT_MAT_EJA','QT_MAT_ESP','NU_ANO_CENSO'] 
    
    data = pd.read_csv(csv_file, encoding='latin-1', delimiter=';', usecols = colList, chunksize = chunksize)

    try:
            #passo1
        connection = connectDb()
            
            #passo2
        cursor = connection.cursor() 

        totalRegistros = 0    
            #passo3
        for chunk in data:

            entidades = chunk.fillna(0)
            entidadesDict = entidades.to_dict(orient='records')

            entidades_info = [(entidade['CO_ENTIDADE'], entidade['NO_ENTIDADE'], entidade['CO_UF'] , entidade['CO_MUNICIPIO'], 
                       entidade['CO_MESORREGIAO'], entidade['CO_MICRORREGIAO'],entidade['QT_MAT_BAS'],entidade['QT_MAT_INF'],
                       entidade['QT_MAT_FUND'],entidade['QT_MAT_MED'],entidade['QT_MAT_MED_CT'],entidade['QT_MAT_MED_NM'],
                       entidade['QT_MAT_PROF'],entidade['QT_MAT_PROF_TEC'],entidade['QT_MAT_EJA'],entidade['QT_MAT_ESP'],entidade['NU_ANO_CENSO'],
                        ) for entidade in entidadesDict]

            cursor.executemany(
            """INSERT INTO Entidades (
                CO_ENTIDADE, NO_ENTIDADE, CO_UF, CO_MUNICIPIO,
                CO_MESORREGIAO, CO_MICRORREGIAO, QT_MAT_BAS, QT_MAT_INF, 
                QT_MAT_FUND, QT_MAT_MED, QT_MAT_MED_CT, QT_MAT_MED_NM, QT_MAT_PROF, QT_MAT_PROF_TEC, 
                QT_MAT_EJA, QT_MAT_ESP, ANO_CENSO
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,entidades_info)

            totalRegistros += len(entidades_info) 
             
        #passo4

        connection.commit()
        logger.info(f"Entidades inseridas com sucesso: {totalRegistros} registros")       

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Erro: {e.pgerror}")
    finally:   
        cursor.close()
        connection.close()


    
def atualizarMicro_e_Meso(dataList):
    try:
        connection = connectDb()
        cursor = connection.cursor()
        cursor.executemany(
            '''UPDATE Entidades
                SET CO_MICRORREGIAO = %s, CO_MESORREGIAO = %s
                WHERE CO_MUNICIPIO = %s; ''',dataList)
        connection.commit()
        logger.info(f"Dados atualizados com sucesso") 

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Erro: {e.pgerror}")
    except Exception as e:
        connection.rollback()
        logger.error(f"Exception: {e}")
    finally:
        cursor.close()
        connection.close()    
    

def removerFk():
    try:
        connection = connectDb()
        cursor = connection.cursor()
            
        cursor.execute('''
            ALTER TABLE entidades
            DROP CONSTRAINT entidades_co_mesorregiao_fkey;
        ''')

        cursor.execute('''
                ALTER TABLE entidades
                DROP CONSTRAINT entidades_co_microrregiao_fkey;
        ''')
            
        connection.commit()
        logger.info(f"fks de microrregiao e mesorregiao retiradas") 

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Erro: {e.pgerror}")
    except Exception as e:
        connection.rollback()
        logger.error(f"Erro inesperado: {e}")
    finally:
        cursor.close()
        connection.close()   


def adicionarFk():
    try:
        connection = connectDb()
        cursor = connection.cursor()
            
        cursor.execute('''
            ALTER TABLE entidades
            ADD CONSTRAINT entidades_co_microrregiao_fkey 
            FOREIGN KEY (co_microrregiao)
            REFERENCES microrregiao(co_microrregiao);
        ''')

        cursor.execute('''
            ALTER TABLE entidades
            ADD CONSTRAINT entidades_co_mesorregiao_fkey
            FOREIGN KEY (co_mesorregiao)
            REFERENCES mesorregiao(co_mesorregiao);
        ''')
            
        connection.commit()
        logger.info(f"FKs adicionadas") 

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Erro: {e.pgerror}")
    except Exception as e:
        connection.rollback()
        logger.error(f"Erro inesperado: {e}")
    finally:
        cursor.close()
        connection.close() 


if __name__ == "__main__": 
    
    
    removerFk()

    csv_file2023 = "/mnt/c/Users/Jefferson/Downloads/microdados_ed_basica_2023.csv"
    csv_file2024 = "/mnt/c/Users/Jefferson/Downloads/microdados_ed_basica_2024.csv"
    
    
    armazenar_microdados_educacao(csv_file2023,10000)
    armazenar_microdados_educacao(csv_file2024,10000)
    
    
    url ='https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    dataList = extratorDados(url)
    atualizarMicro_e_Meso( dataList)
   
    adicionarFk()



