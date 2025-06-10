# ETL DataOps Example

Este projeto demonstra um pipeline simples de DataOps utilizando MinIO, ClickHouse e Streamlit. Ele serve como uma introdução prática a conceitos de DataOps e às boas práticas para orquestração de dados em ambientes controlados por código.

## Visão Geral

1. **MinIO** recebe arquivos CSV que serão processados.
2. **Python ETL** roda automaticamente e grava cada linha do CSV em uma tabela no ClickHouse.
3. **Streamlit** apresenta um painel com as métricas básicas de ingestão e os dados carregados.
4. Tudo é executado através de `docker-compose` para facilitar a reprodutibilidade.

## Estrutura

```
├── docker-compose.yml       # Infraestrutura completa
├── Dockerfile               # Imagem base para ETL e Streamlit
├── src/
│   ├── etl.py               # Script de ingestão
│   ├── streamlit_app.py     # Dashboard
│   └── requirements.txt     # Dependências Python
└── sample_data/
    └── sample.csv           # Exemplo de dataset
```

## Como Executar

1. **Pré‑requisitos**: docker e docker-compose instalados.
2. Execute `docker-compose up --build` para iniciar a stack.
3. Acesse:
   - MinIO Console em `http://localhost:9001` (usuário e senha `minioadmin`).
   - Streamlit em `http://localhost:8501`.
4. O serviço ETL cria automaticamente o bucket `data` e carrega `sample.csv`. Coloque novos CSVs neste bucket para novas ingestões.

## Funcionamento do ETL

O ETL monitora o bucket configurado e, a cada arquivo CSV encontrado, insere as linhas na tabela `ingestions` do ClickHouse com três colunas:

- `id`: identificador incremental
- `ingestion_date`: timestamp de ingestão
- `data_value`: JSON com o conteúdo da linha original do CSV

## Boas Práticas de DataOps

- **Infraestrutura como código**: todo o ambiente é descrito em `docker-compose.yml` e pode ser reproduzido em qualquer máquina.
- **Versionamento**: mantenha scripts e configurações sob controle de versão para garantir rastreabilidade.
- **Automação**: o ETL é executado automaticamente no start do container, reduzindo intervenções manuais.
- **Observabilidade**: o dashboard em Streamlit disponibiliza métricas simples para acompanhar a evolução das cargas.
- **Simplicidade e testes**: comece com processos enxutos e evolua conforme novas necessidades surgirem.

## Próximos Passos

- Expandir as métricas apresentadas pelo Streamlit (tempos de execução, volume por arquivo, etc.).
- Adicionar testes automatizados para os scripts de ETL.
- Integrar com ferramentas de CI/CD para implantar mudanças com segurança.

Este repositório busca ser um ponto de partida para estudos e experimentos em DataOps.
