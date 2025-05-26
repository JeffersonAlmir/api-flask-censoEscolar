import requests
import sqlite3

DATABASE = 'censoEscolar.db'

def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    mesorregiaoSet = {(municipio ['microrregiao']['mesorregiao']['id'], municipio ['microrregiao']['mesorregiao']['nome'],
                         municipio ['microrregiao']['mesorregiao']['UF']['id']) for municipio  in dados}
    
    try:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        with open('schemas/mesorregiaoSchema.sql') as file:
            cursor.executescript(file.read())
        
        cursor.executemany("""INSERT INTO Mesorregiao(CO_MESORREGIAO, NO_MESORREGIAO, CO_UF) VALUES (? ,?, ?);""",mesorregiaoSet)
        
        connection.commit()
    except sqlite3.Error as e:
        return e
    finally:
        connection.close()
    return len(mesorregiaoSet)
        


if __name__ == "__main__":
    url ='https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/municipios'
    dados = extrator(url)
    totalMesorregiao =armazenarDados(dados)
    print(f"{totalMesorregiao} Mesorregiao adicionadas")