import pandas as pd
import json
import os

def conversorCsvJson(csv_file,filtroCol,filtro,colList):
    if os.path.exists(csv_file):
        data = pd.read_csv(csv_file, encoding='latin-1',delimiter=';', usecols=colList)
        filtro_data =data[data[filtroCol]==(filtro)].fillna(0)
        filtro_data.sort_values('CO_ENTIDADE', ascending=True, inplace=True)
        
        dados = filtro_data.to_dict(orient='records')
       
        with open("json_data.json", 'w', encoding='utf-8') as jsonFile:
            json.dump(dados, jsonFile,indent=4, ensure_ascii=False)
            
        print(f"Conversão concluída! Foram criados {len(dados)} objetos JSON.")
    else:
        print(f"Arquivo não encontrado: {csv_file}")
    

csv_file ="C:/Users/Jefferson/Documents/microdados_ed_basica_2024.csv"

cols = ['CO_ENTIDADE','NO_REGIAO','NO_UF','SG_UF','NO_MUNICIPIO','CO_MESORREGIAO','NO_MESORREGIAO','CO_MICRORREGIAO','NO_MICRORREGIAO','NO_ENTIDADE',
        'QT_MAT_BAS','QT_MAT_INF','QT_MAT_FUND','QT_MAT_MED','QT_MAT_MED_CT','QT_MAT_MED_NM',
        'QT_MAT_PROF','QT_MAT_PROF_TEC','QT_MAT_EJA','QT_MAT_EJA_FUND','QT_MAT_EJA_MED','QT_MAT_ESP']

if __name__ == "__main__": 
    conversorCsvJson(csv_file,"SG_UF",'PB',cols) 