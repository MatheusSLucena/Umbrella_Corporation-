# Umbrella Corporation

Repositório do grupo com os trabalhos: pipeline de dados sobre dengue no Recife, formulário de visita às ovitrampas e o desafio do IBGE.

## Integrantes
1. Mateus Maximo
2. Matheus Lucena
3. Marcello Pragana
4. Apollo Henrique
5. João Carlos
6. Miguel Roberto

## Estrutura

```
.
├── docs/                    Documentos escritos (CRISP-DM do Grupo 5)
├── projeto-dengue/
│   ├── codigo/              Pipeline ETL em Python (Extract, Load, Transform, Main)
│   └── dados/
│       ├── json/            Dados extraídos em JSON
│       ├── csv/             Dados extraídos em CSV
│       └── consolidado/     Arquivo único consolidado (xlsx, json, csv)
├── formulario-ovitrampas/   Site do formulário de visita às ovitrampas (Flask + MongoDB)
└── desafio-ibge/            Desafio individual de consulta à API do IBGE
```

## Como usar cada parte

| Pasta | Como executar |
|---|---|
| `projeto-dengue/codigo` | `pip install -r requirements.txt` e depois `python Main.py` |
| `formulario-ovitrampas` | Copie `.env.example` para `.env`, preencha, e rode `python iniciar.py` (ou `Iniciar_Formulario.bat` no Windows). Detalhes no README da pasta. |
| `desafio-ibge` | `python mainX.py` (veja `Read_Me_Mateus_Maximo.txt`) |

> O arquivo `.env` guarda credenciais e **não** deve ser versionado.
