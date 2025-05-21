import requests
import sqlite3


def extrator(url):
    requisicao = requests.get(url)
    requisicaoJson = requisicao.json() 
    return requisicaoJson

def armazenarDados(dados):

    ufsList = [(uf['id'], uf["nome"], uf['sigla']) for uf  in dados]
    try:
        connection = sqlite3.connect('entidades.db')
        cursor = connection.cursor()
        with open('schemas/ufSchema.sql') as file:
            cursor.executescript(file.read())

        cursor.executemany("""INSERT INTO UF(CO_UF ,NO_UF, SG_UF)VALUES(? ,? ,?);""",ufsList)
        
        connection.commit()
    except sqlite3.Error as e:
        return e 
    finally: 
        connection.close()
    return len(ufsList)

     


if __name__ == "__main__":
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/regioes/2/estados'
    dados = extrator(url)
    totalUfs = armazenarDados(dados)
    print(f"{totalUfs} UFs adicionadas")