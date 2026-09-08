import xml.etree.ElementTree as Et
import pandas as pd
import glob


dados = []

for arquivo in glob.glob("Dados_extraidos/BASE Distritos sanitários shapefile/*.shp.xml"):
    raiz = Et.parse(arquivo).getroot()

    for elem in raiz.iter():
        dados.append({
            "arquivo": arquivo.split("\\")[-1],
            "tag":elem.tag,
            "texto": (elem.text or "").strip(),
            "atributos": str(elem.attrib)
        })

df = pd.DataFrame(dados)


pd.set_option('display.max_rows', None)

pd.set_option('display.max_columns', None)

pd.set_option('display.max_colwidth', None)


## df.to_csv("xml_tabela_csv", index=False, encoding="utf-8-sig")


print(df)