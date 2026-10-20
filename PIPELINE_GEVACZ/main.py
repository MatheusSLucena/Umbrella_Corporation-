from extract_transform import extrair_transformar_ovitrampas
from common import conectar_neon, conectar_mongo
from load_destinations import (
    APIS_MONGO, carregar_ovitrampas_neon,
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

        # Mongo fica pronto para APIs: só conecta se houver alguma ativa em APIS_MONGO.
        if any(api.get("ativo", True) for api in APIS_MONGO.values()):
            client, mongo_db = conectar_mongo()
            carregar_apis_mongo(mongo_db)
        else:
            print("[pulado] MongoDB: nenhuma API ativa em APIS_MONGO")
    finally:
        if client is not None:
            client.close()
        if engine is not None:
            engine.dispose()
        print("Conexões encerradas")

if __name__ == "__main__":
    main()
