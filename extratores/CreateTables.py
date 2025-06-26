import psycopg2
from helpers.logging import logger
from helpers.database import connectDb


def createTable(arquivo):

    try:
        connection = connectDb()
        cursor = connection.cursor()
        with open(arquivo) as file:
            cursor.execute(file.read())
    
        connection.commit()
        logger.info(f"Tabela do arquivo {arquivo} criada com sucesso.")
    except psycopg2.Error as e:
        logger.error(f"Erro: {e.pgerror}")   
        
    finally:
        cursor.close()
        connection.close()
        



schemas = ['schemas/ufSchema.sql','schemas/mesorregiaoSchema.sql','schemas/microrregiaoSchema.sql',
           'schemas/municipioSchema.sql','schemas/entidadeSchema.sql']
for schema in schemas:
    createTable(schema)


#python3 -m extratores.CreateTables para roda o arquivo