import requests
import sqlite3


def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    municipiosList = [(municipio['id'], municipio["nome"], 
                       municipio['microrregiao']['mesorregiao']['UF']['id']) for municipio  in dados]
    try:
        connection = sqlite3.connect('entidades.db')
        cursor = connection.cursor()
        with open('schemas/municipioSchema.sql') as file:
            cursor.executescript(file.read())
        
        cursor.executemany("""INSERT INTO Municipio(CO_MUNICIPIO, NO_MUNICIPIO, CO_UF)VALUES(? ,?, ?);""",municipiosList)
        
        connection.commit()
    except sqlite3.Error as e:
        return e
    finally:
        connection.close()
    return len(municipiosList)

     


if __name__ == "__main__":
    url ='https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/municipios'
    dados = extrator(url)
    totalMunicipio =armazenarDados(dados)
    print(f"{totalMunicipio} Municipios adicionados")