import re

import pandas as pd
import requests
from pymongo import MongoClient
from requests.adapters import HTTPAdapter
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.dialects.postgresql import JSONB
from urllib3.util.retry import Retry

from config import cfg

NEON_SCHEMA = cfg("NEON_SCHEMA", "public")

def url_sqlalchemy(url):
    for prefixo in ("postgres://", "postgresql://"):
        if url.startswith(prefixo):
            return "postgresql+psycopg2://" + url[len(prefixo):]
    return url

def conectar_neon():
    engine = create_engine(
        url_sqlalchemy(cfg("NEON_DATABASE_URL", obrigatorio=True)),
        pool_pre_ping=True, pool_recycle=300, connect_args={"connect_timeout": 30},
    )
    with engine.begin() as con:
        if NEON_SCHEMA != "public":
            con.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{NEON_SCHEMA}"'))
        banco, versao = con.execute(text("select current_database(), version()")).fetchone()
    print("Conectado ao Neon:", banco, "|", versao.split(",")[0])
    return engine

def _snake(nome):
    import unicodedata
    s = unicodedata.normalize("NFKD", str(nome)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^0-9a-zA-Z]+", "_", s).strip("_").lower()
    return ("c_" + s if s[:1].isdigit() else s) or "coluna"

def normalizar_colunas(df):
    novos, usados = [], set()
    for c in df.columns:
        n = base = _snake(c)
        i = 2
        while n in usados:
            n, i = f"{base}_{i}", i + 1
        usados.add(n)
        novos.append(n)
    df = df.copy()
    df.columns = novos
    return df

def enviar_neon(df, tabela, engine, modo="replace", chave=None, indices=(), inteiros=(), lote=5000):
    d = normalizar_colunas(df)
    for c in inteiros:
        if c in d.columns:
            try:
                d[c] = pd.to_numeric(d[c], errors="coerce").astype("Int64")
            except (TypeError, ValueError):
                print(f"  aviso: '{c}' tem valores não inteiros; mantido como decimal")
    tipos = {c: JSONB for c in d.columns if d[c].map(lambda v: isinstance(v, (list, dict))).any()}
    alvo = f'"{NEON_SCHEMA}"."{tabela}"'
    opcoes = dict(schema=NEON_SCHEMA, index=False, dtype=tipos, method="multi", chunksize=lote)
    if modo in ("replace", "append"):
        d.to_sql(tabela, engine, if_exists=modo, **opcoes)
    elif modo == "upsert":
        if not chave:
            raise ValueError("modo='upsert' exige chave=[...]")
        chave = [_snake(c) for c in chave]
        d = d.drop_duplicates(chave, keep="last")
        col_chave = ", ".join(f'"{c}"' for c in chave)
        if not inspect(engine).has_table(tabela, schema=NEON_SCHEMA):
            d.to_sql(tabela, engine, if_exists="fail", **opcoes)
        with engine.begin() as con:
            nome_idx = ("ux_" + tabela + "_" + "_".join(chave))[:63]
            con.execute(text(f'CREATE UNIQUE INDEX IF NOT EXISTS "{nome_idx}" ON {alvo} ({col_chave})'))
        stg = f"_stg_{tabela}"[:63]
        d.to_sql(stg, engine, if_exists="replace", **opcoes)
        cols = ", ".join(f'"{c}"' for c in d.columns)
        sets = ", ".join(f'"{c}" = EXCLUDED."{c}"' for c in d.columns if c not in chave)
        acao = f"DO UPDATE SET {sets}" if sets else "DO NOTHING"
        with engine.begin() as con:
            con.execute(text(f'INSERT INTO {alvo} ({cols}) SELECT {cols} FROM "{NEON_SCHEMA}"."{stg}" ON CONFLICT ({col_chave}) {acao}'))
            con.execute(text(f'DROP TABLE "{NEON_SCHEMA}"."{stg}"'))
    else:
        raise ValueError("modo deve ser 'replace', 'append' ou 'upsert'")
    with engine.begin() as con:
        for cols_idx in indices:
            cols_idx = [_snake(c) for c in cols_idx if _snake(c) in d.columns]
            if cols_idx and not (modo == "upsert" and cols_idx == chave):
                nome_idx = ("ix_" + tabela + "_" + "_".join(cols_idx))[:63]
                lista = ", ".join(f'"{c}"' for c in cols_idx)
                con.execute(text(f'CREATE INDEX IF NOT EXISTS "{nome_idx}" ON {alvo} ({lista})'))
        return con.execute(text(f"SELECT COUNT(*) FROM {alvo}")).scalar()

def _sessao():
    s = requests.Session()
    retry = Retry(total=4, backoff_factor=1.5, status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=("GET", "POST"))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    return s

def _resolver_segredos(obj):
    if isinstance(obj, str):
        return re.sub(r"\{\{(\w+)\}\}", lambda m: cfg(m.group(1), obrigatorio=True), obj)
    if isinstance(obj, dict):
        return {k: _resolver_segredos(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_resolver_segredos(v) for v in obj]
    return obj

def _extrair(obj, caminho):
    for parte in (caminho.split(".") if caminho else []):
        obj = obj[int(parte)] if isinstance(obj, list) else obj[parte]
    return obj

def colunas_para_registros(d):
    n = len(next(iter(d.values())))
    return [{k: v[i] for k, v in d.items()} for i in range(n)]

def buscar_api(api, sessao=None):
    sessao = sessao or _sessao()
    url = api["url"]
    params = _resolver_segredos(dict(api.get("params", {})))
    headers = _resolver_segredos(dict(api.get("headers", {})))
    pag = api.get("paginacao") or {}
    tipo, pagina, registros = pag.get("tipo"), pag.get("inicio", 1), []
    for n_req in range(pag.get("max_paginas", 100) if tipo else 1):
        p = dict(params) if (n_req == 0 or tipo != "proximo") else None
        if tipo == "pagina":
            p[pag.get("param", "page")] = pagina
        resp = sessao.request(api.get("metodo", "GET"), url, params=p, headers=headers,
                              json=api.get("body"), timeout=api.get("timeout", 60))
        resp.raise_for_status()
        corpo = resp.json()
        dados = _extrair(corpo, api.get("caminho_dados"))
        if api.get("transformar"):
            dados = api["transformar"](dados)
        if isinstance(dados, dict):
            dados = [dados]
        if not dados:
            break
        registros.extend(dados)
        if tipo == "pagina":
            if pag.get("tamanho") and len(dados) < pag["tamanho"]:
                break
            pagina += 1
        elif tipo == "proximo":
            try:
                url = _extrair(corpo, pag.get("campo", "next"))
            except (KeyError, IndexError, TypeError):
                url = None
            if not url:
                break
        else:
            break
    extra = api.get("extra", {})
    return [{**r, **extra} for r in registros]

def rodar_apis(apis, enviar):
    resumo = {}
    for nome, api in apis.items():
        if not api.get("ativo", True):
            print(f"[pulado] {nome}")
            continue
        try:
            resumo[nome] = enviar(nome, api)
            print(f"[ok] {nome}: {resumo[nome]} registros no destino")
        except Exception as e:
            resumo[nome] = f"ERRO: {e}"
            print(f"[ERRO] {nome}: {e}")
    if not resumo:
        print("Nenhuma API ativa (defina 'ativo': True na configuração).")
    return resumo

def conectar_mongo():
    user = cfg("MONGO_USER", obrigatorio=True)
    password = cfg("MONGO_PASSWORD", obrigatorio=True)
    host = cfg("MONGO_HOST", obrigatorio=True)
    db_name = cfg("MONGO_DB", "gevacz")
    client = MongoClient(f"mongodb+srv://{host}/", username=user, password=password,
                         authSource="admin", serverSelectionTimeoutMS=15000)
    client.admin.command("ping")
    print("Conectado ao MongoDB, banco:", db_name)
    return client, client[db_name]
