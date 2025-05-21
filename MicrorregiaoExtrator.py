import requests
import sqlite3


def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    microrregiaoSet = {(municipio ['microrregiao']['id'], municipio ['microrregiao']['nome'],
                         municipio ['microrregiao']['mesorregiao']['UF']['id']) for municipio  in dados}
    try:
        connection = sqlite3.connect('entidades.db')
        cursor = connection.cursor()
        with open('schemas/microrregiaoSchema.sql') as file:
            cursor.executescript(file.read())
        
        cursor.executemany("""INSERT INTO Microrregiao(CO_MICRORREGIAO, NO_MICRORREGIAO, CO_UF) VALUES (? ,?, ?);""",microrregiaoSet)
        
        connection.commit()

    except sqlite3.Error as e:
        return e
    finally:
        connection.close()
    return len(microrregiaoSet)
        


if __name__ == "__main__":

    url ='https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/municipios'
    dados = extrator(url)
    totalMicrorregiao = armazenarDados(dados)
    print(f"{totalMicrorregiao} Microrregiao adicionadas")