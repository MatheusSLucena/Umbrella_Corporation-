import re
import unicodedata
import pandas as pd

from config import BASE, PATH_2026, PATH_ANTIGOS, DSS

COLUNAS_DESCARTAR_2026 = [
    "QT", "DT_COLETA", "DT_ENTREGA_APOIO", "DT_ENTREGA_LAB",
    "DT_LEITURA", "NM_TEC_LAB", "DT_DIG", "DT_ENVIO_DS",
]

def _norm_nome(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().upper()

_RE_MAT = re.compile(r"\d{2,3}\.\d{3}-\d")

def _tem_matricula(txt):
    return len(re.findall(r"\d", str(txt))) >= 5

def _nome_agente(texto):
    t = _RE_MAT.sub("", str(texto))
    t = re.sub(r"S\s*/?\s*M\b", "", t, flags=re.I)
    return _norm_nome(t.replace("/", " "))

def mapa_matriculas(ref):
    achados = {}
    for txt in ref["AGENTE / MATRICULA"].dropna().astype(str).str.strip().unique():
        m = _RE_MAT.search(txt)
        if m:
            achados.setdefault(_nome_agente(txt), {})[m.group()] = txt
    return {n: list(v.values())[0] for n, v in achados.items() if len(v) == 1}

def completar_matricula(df, ref):
    mapa = mapa_matriculas(ref)
    ag = df["AGENTE / MATRICULA"].astype("string")
    sem = ag.notna() & ~ag.map(
        lambda t: _tem_matricula(t) if pd.notna(t) else True
    ).astype(bool)
    novo = ag.where(~sem, ag.map(
        lambda t: mapa.get(_nome_agente(t)) if pd.notna(t) else None
    ))
    df = df.copy()
    df["AGENTE / MATRICULA"] = novo.fillna(ag).astype(object)
    return df

def tratar_ovt_antigo(path, ds, ano, ref=None):
    """Converte planilhas antigas (abas por bairro/ciclos em colunas) para formato longo."""
    abas = pd.read_excel(path, sheet_name=None, header=None)
    partes = []
    for nome_aba, raw in abas.items():
        hdr = raw.index[raw[0].astype(str).str.strip().eq("BAIRRO")][0]
        cab = raw.loc[hdr].astype(str).str.strip()
        c_id = cab[cab.str.upper().str.startswith("ID")].index[0]
        corpo = raw.loc[hdr + 1:]
        corpo = corpo[corpo[c_id].astype(str).str.strip().str.match(r"^[A-Za-z]{2,4}\s*/?\s*\d+$")]
        ids = corpo[c_id].astype(str).str.replace(r"[\s/]", "", regex=True).str.upper()
        rot = raw.loc[hdr - 1].fillna("").astype(str).str.strip().str.upper()
        ciclos = {
            c: int(re.search(r"\d+", t).group())
            for c, t in rot.items() if re.match(r"^CICLO\s*\d+", t)
        }
        for c, n in ciclos.items():
            c_obs = c + 2 if c + 2 in raw.columns else None
            partes.append(pd.DataFrame({
                "Ano": ano, "CICLOS": n, "DS": ds,
                "BAIRRO": nome_aba.strip().upper(),
                "AGENTE / MATRICULA": corpo[1].astype("string").str.strip().values,
                "ID_OVT": ids.values,
                "N_OVOS": pd.to_numeric(corpo[c + 1], errors="coerce").values,
                "OBS": (corpo[c_obs].astype(str).str.strip().str.upper().values
                        if c_obs is not None else None),
                "DATA": pd.to_datetime(corpo[c], errors="coerce").values,
            }))
    if not partes:
        return pd.DataFrame(columns=[
            "Ano", "CICLOS", "DS", "BAIRRO", "BAIRRO_AREA",
            "AGENTE / MATRICULA", "ID_OVT", "N_OVOS", "OBS", "DATA"
        ])
    df = pd.concat(partes, ignore_index=True)
    df["OBS"] = df["OBS"].replace({"NAN": pd.NA, "NONE": pd.NA, "": pd.NA})
    df.loc[~df["OBS"].isin(["E", "F", "REC", "R", "D"]), "OBS"] = pd.NA
    df = (df.sort_values("AGENTE / MATRICULA", na_position="last", kind="stable")
          .drop_duplicates(["ID_OVT", "CICLOS", "N_OVOS", "OBS", "DATA"], keep="first")
          .sort_index())
    df = df[~(df["DATA"].isna() & df["N_OVOS"].isna() & df["OBS"].isna())]
    df["BAIRRO_AREA"] = df["BAIRRO"]
    if ref is not None:
        mapa = ref.drop_duplicates("ID_OVT").set_index("ID_OVT")[["BAIRRO", "BAIRRO_AREA"]]
        df["BAIRRO"] = df["ID_OVT"].map(mapa["BAIRRO"]).fillna(df["BAIRRO"])
        df["BAIRRO_AREA"] = df["ID_OVT"].map(mapa["BAIRRO_AREA"]).fillna(df["BAIRRO_AREA"])
        df = completar_matricula(df, ref)
    ordem = ["Ano", "CICLOS", "DS", "BAIRRO", "BAIRRO_AREA",
             "AGENTE / MATRICULA", "ID_OVT", "N_OVOS", "OBS", "DATA"]
    return df[ordem].reset_index(drop=True)

def extrair_transformar_ovitrampas():
    """Executa a extração e transformação dos dados de 2026, 2025 e 2024."""
    ovitrampas2026 = pd.read_excel(PATH_2026, 0, header=0)
    ovitrampas2026 = ovitrampas2026.drop(columns=COLUNAS_DESCARTAR_2026, errors="ignore")
    tabelas = {}
    for ano, template in PATH_ANTIGOS.items():
        lista = []
        for ds in DSS:
            caminho = template.format(ds=ds)
            df = tratar_ovt_antigo(caminho, ds=ds, ano=ano, ref=ovitrampas2026)
            print(f"{ano} DS-{ds}: {len(df)} linhas, {df['ID_OVT'].nunique()} ovitrampas")
            lista.append(df)
        tabelas[ano] = pd.concat(lista, ignore_index=True)
    tabelas_ovt = {
        "ovitrampas_2026": ovitrampas2026,
        "ovitrampas_2025": tabelas[2025],
        "ovitrampas_2024": tabelas[2024],
    }
    for ano, df in tabelas.items():
        print(ano, df.shape)
        print("  Duplicados (ID_OVT, CICLOS):", df.duplicated(["ID_OVT", "CICLOS"]).sum())
        print("  Colunas só em 2026:", set(ovitrampas2026.columns) - set(df.columns))
        print(f"  Colunas só em {ano}:", set(df.columns) - set(ovitrampas2026.columns))
        print("  Ovitrampas fora de 2026:",
              (~df["ID_OVT"].isin(ovitrampas2026["ID_OVT"])).groupby(df["ID_OVT"]).first().sum())
    return tabelas_ovt
