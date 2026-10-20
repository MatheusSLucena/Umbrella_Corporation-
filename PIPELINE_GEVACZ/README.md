# ETL GEVACZ — estrutura em Python

## Arquivos
- `config.py`: caminhos e leitura do `.env`.
- `extract_transform.py`: extração das planilhas e transformação dos dados de 2024, 2025 e 2026.
- `common.py`: conexões e utilitários compartilhados (Neon/PostgreSQL, MongoDB e APIs).
- `load_destinations.py`: carga dos DataFrames (Neon) e das APIs (Neon e Mongo).
- `main.py`: orquestra a ETL completa.

## Destinos
- **Neon (PostgreSQL):** recebe todos os dados da pasta `INFORMAÇÕES - GEVACZ` (tabelas `ovitrampas_2024`, `ovitrampas_2025` e `ovitrampas_2026`) e as APIs configuradas em `APIS_NEON`.
- **MongoDB:** não recebe mais as ovitrampas. Fica reservado para APIs, configuradas em `APIS_MONGO` (`load_destinations.py`). O `main.py` só abre a conexão com o Mongo se alguma API de `APIS_MONGO` estiver com `"ativo": True`.

## Instalação
No ambiente virtual:
```bash
pip install pandas openpyxl xlrd python-dotenv requests pymongo sqlalchemy psycopg2-binary
```

## Configuração
1. Confira o caminho `GEVACZ_BASE` em `config.py` ou defina a variável de ambiente `GEVACZ_BASE`.
2. Crie o arquivo `.env` na pasta base com `NEON_DATABASE_URL` e, se necessário, `NEON_SCHEMA`. Para usar APIs no Mongo, inclua também `MONGO_USER`, `MONGO_PASSWORD`, `MONGO_HOST` e, se necessário, `MONGO_DB`.
3. Não compartilhe o `.env` nem coloque credenciais diretamente no código.
4. As APIs estão inicialmente com `ativo: False`.

## Adicionando uma API no Mongo
Inclua uma entrada em `APIS_MONGO` (`load_destinations.py`) com `url`, `colecao`, `modo` (`replace`, `append` ou `upsert`, este último exigindo `chave`) e `"ativo": True`.

## Execução
Com os cinco arquivos na mesma pasta:
```bash
python main.py
```

**Atenção:** a carga de ovitrampas usa modo `replace` e recria/substitui as tabelas de destino no Neon. Confirme o destino antes de executar.

## Nota

O ARQUIVO PIPELINE GEVACZ NO GITHUB NÃO POSSUI INCLUIDO A PASTA DE NOME "INFORMAÇÕES - GEVACZ". PARA A EXECUÇÃO DA PIPELINE, É NECESSÁRIO A INSERÇÃO DESSA PASTA NA PASTA DA PIPELINE.
