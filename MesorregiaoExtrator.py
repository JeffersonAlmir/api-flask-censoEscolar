import requests
import sqlite3


def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    mesorregiaoSet = {(municipio ['microrregiao']['mesorregiao']['id'], municipio ['microrregiao']['mesorregiao']['nome'],
                         municipio ['microrregiao']['mesorregiao']['UF']['id']) for municipio  in dados}
    
    try:
        connection = sqlite3.connect('entidades.db')
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Mesorregiao(
                CO_MESORREGIAO INTEGER PRIMARY KEY,
                NO_MESORREGIAO TEXT NOT NULL,
                CO_UF INTEGER NOT NULL,
                FOREIGN KEY (CO_UF) REFERENCES UF(CO_UF) 
            );""")
        
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