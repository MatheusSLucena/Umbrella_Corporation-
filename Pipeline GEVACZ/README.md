# ETL GEVACZ — estrutura em Python

## Arquivos
- `config.py`: caminhos e leitura do `.env`.
- `extract_transform.py`: extração das planilhas e transformação dos dados de 2024, 2025 e 2026.
- `common.py`: conexões e utilitários compartilhados (Neon/PostgreSQL, MongoDB e APIs).
- `load_destinations.py`: carga dos DataFrames e APIs nos destinos.
- `main.py`: orquestra a ETL completa.

## Instalação
No ambiente virtual:
```bash
pip install pandas openpyxl xlrd python-dotenv requests pymongo sqlalchemy psycopg2-binary
```

## Configuração
1. Confira o caminho `GEVACZ_BASE` em `config.py` ou defina a variável de ambiente `GEVACZ_BASE`.
2. Crie o arquivo `.env` na pasta base com `NEON_DATABASE_URL`, `MONGO_USER`, `MONGO_PASSWORD`, `MONGO_HOST` e, se necessário, `MONGO_DB` e `NEON_SCHEMA`.
3. Não compartilhe o `.env` nem coloque credenciais diretamente no código.
4. As APIs estão inicialmente com `ativo: False`, como no notebook original.

## Execução
Com os cinco arquivos na mesma pasta:
```bash
python main.py
```

**Atenção:** a carga de ovitrampas usa modo `replace` e recria/substitui as tabelas/coleções de destino. Confirme o destino antes de executar.

## Nota

O ARQUIVO PIPELINE GEVACZ NO GITHUB NÃO POSSUI INCLUIDO A PASTA DE NOME "INFORMAÇÕES - GEVACZ". PARA A EXECUÇÃO DA PIPELINE, É NECESSÁRIO A INSERÇÃO DESSA PASTA NO ARQUIVO DA PIPELINE.