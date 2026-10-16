from extract_transform import extrair_transformar_ovitrampas
from common import conectar_neon, conectar_mongo
from load_destinations import (
    carregar_ovitrampas_neon, carregar_ovitrampas_mongo,
    carregar_apis_neon, carregar_apis_mongo,
)

def main():
    tabelas = extrair_transformar_ovitrampas()
    engine = None
    client = None
    try:
        engine = conectar_neon()
        carregar_ovitrampas_neon(tabelas, engine)
        carregar_apis_neon(engine)
        client, mongo_db = conectar_mongo()
        carregar_ovitrampas_mongo(tabelas, mongo_db)
        carregar_apis_mongo(mongo_db)
    finally:
        if client is not None:
            client.close()
        if engine is not None:
            engine.dispose()
        print("Conexões encerradas")

if __name__ == "__main__":
    main()
