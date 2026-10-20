from datetime import date, datetime, timedelta, timezone
import pandas as pd
from pymongo import ReplaceOne
from sqlalchemy import text

from common import (
    NEON_SCHEMA, enviar_neon,
    buscar_api, colunas_para_registros, rodar_apis
)


APIS_NEON = {
    "clima_recife_diario": {
        "ativo": False,
        "url": "https://archive-api.open-meteo.com/v1/archive",
        "params": {
            "latitude": -8.05, "longitude": -34.88,
            "start_date": "2024-01-01", "end_date": str(date.today() - timedelta(days=7)),
            "daily": "precipitation_sum,temperature_2m_mean,temperature_2m_max,temperature_2m_min",
            "timezone": "America/Recife",
        },
        "caminho_dados": "daily", "transformar": colunas_para_registros,
        "colunas_data": ["time"], "renomear": {"time": "data"},
        "tabela": "clima_recife_diario", "modo": "upsert", "chave": ["data"], "indices": [],
    },
    "exemplo_api_com_token": {
        "ativo": False, "url": "https://api.exemplo.gov.br/v1/registros",
        "headers": {"Authorization": "Bearer {{MINHA_API_TOKEN}}"},
        "params": {"per_page": 100},
        "paginacao": {"tipo": "pagina", "param": "page", "inicio": 1, "tamanho": 100, "max_paginas": 50},
        "caminho_dados": "results", "tabela": "exemplo_registros",
        "modo": "upsert", "chave": ["id"], "indices": [["data"]],
    },
}

# ---------------------------------------------------------------------------
# APIs EXTERNAS -> MongoDB (estrutura pronta; ative com "ativo": True)
# ---------------------------------------------------------------------------
APIS_MONGO = {
    "infodengue_recife": {
        "ativo": False, "url": "https://info.dengue.mat.br/api/alertcity",
        "params": {"geocode": 2611606, "disease": "dengue", "format": "json",
                   "ew_start": 1, "ew_end": 53, "ey_start": 2024, "ey_end": date.today().year},
        "extra": {"geocode": 2611606, "doenca": "dengue"},
        "colecao": "api_infodengue_recife", "modo": "upsert", "chave": ["geocode", "SE"],
    },
    "exemplo_api_json": {
        "ativo": False, "url": "https://api.exemplo.gov.br/v1/boletins",
        "headers": {"Authorization": "Bearer {{MINHA_API_TOKEN}}"},
        "paginacao": {"tipo": "proximo", "campo": "next"},
        "caminho_dados": "results", "colunas_data": ["data_publicacao"],
        "colecao": "api_boletins", "modo": "replace",
    },
}

# ---------------------------------------------------------------------------
# Neon
# ---------------------------------------------------------------------------
def carregar_ovitrampas_neon(tabelas, engine):
    for nome, df in tabelas.items():
        n = enviar_neon(df, nome, engine, modo="replace",
                        inteiros=["ano", "ciclos", "n_ovos"],
                        indices=[["id_ovt", "ciclos"], ["ds"]])
        print(f"{nome}: {n} linhas no Neon (DataFrame tem {len(df)})")
    print(pd.read_sql(text("SELECT table_name FROM information_schema.tables WHERE table_schema = :s ORDER BY 1"),
                      engine, params={"s": NEON_SCHEMA}))
    for nome in tabelas:
        print(nome, pd.read_sql(text(f'SELECT COUNT(*) AS linhas FROM "{NEON_SCHEMA}"."{nome}"'),
                                engine).iloc[0, 0])

def enviar_api_neon(nome, api, engine):
    registros = buscar_api(api)
    if not registros:
        print(f"[vazio] {nome}: a API não devolveu registros")
        return 0
    df = pd.json_normalize(registros, sep="_")
    for c in api.get("colunas_data", []):
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    df = df.rename(columns=api.get("renomear", {}))
    df["ingerido_em"] = datetime.now(timezone.utc)
    return enviar_neon(df, api["tabela"], engine, modo=api.get("modo", "replace"),
                       chave=api.get("chave"), indices=api.get("indices", ()),
                       inteiros=api.get("inteiros", ()))

def carregar_apis_neon(engine):
    return rodar_apis(APIS_NEON, lambda nome, api: enviar_api_neon(nome, api, engine))

# ---------------------------------------------------------------------------
# MongoDB (somente APIs)
# ---------------------------------------------------------------------------
def enviar_mongo_docs(docs, colecao, mongo_db, modo="replace", chave=None, indices=(), lote=5000):
    col = mongo_db[colecao]
    if modo == "replace":
        col.drop()
    if modo == "upsert":
        if not chave:
            raise ValueError("modo='upsert' exige chave=[...]")
        col.create_index([(c, 1) for c in chave], unique=True)
        for i in range(0, len(docs), lote):
            ops = [ReplaceOne({c: d.get(c) for c in chave}, d, upsert=True) for d in docs[i:i + lote]]
            col.bulk_write(ops, ordered=False)
    elif modo in ("replace", "append"):
        for i in range(0, len(docs), lote):
            col.insert_many(docs[i:i + lote])
    else:
        raise ValueError("modo deve ser 'replace', 'append' ou 'upsert'")
    for cols in indices:
        if modo == "upsert" and list(cols) == list(chave):
            continue
        col.create_index([(c, 1) for c in cols])
    return col.count_documents({})

def enviar_api_mongo(nome, api, mongo_db):
    registros = buscar_api(api)
    if not registros:
        print(f"[vazio] {nome}: a API não devolveu registros")
        return 0
    carimbo = datetime.now(timezone.utc)
    for r in registros:
        for c in api.get("colunas_data", []):
            if r.get(c):
                r[c] = pd.to_datetime(r[c]).to_pydatetime()
        r["_ingerido_em"] = carimbo
    return enviar_mongo_docs(registros, api["colecao"], mongo_db,
                             modo=api.get("modo", "replace"), chave=api.get("chave"),
                             indices=api.get("indices", ()))

def carregar_apis_mongo(mongo_db):
    return rodar_apis(APIS_MONGO, lambda nome, api: enviar_api_mongo(nome, api, mongo_db))
