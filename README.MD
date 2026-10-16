# Projeto Final: Pipeline de Dados IoT com Docker e Streamlit

Este repositório contém a entrega prática da disciplina **Disruptive Architectures: IoT, Big Data e IA**. O projeto consiste num pipeline completo de dados que processa leituras de temperatura de dispositivos IoT, armazena as informações num banco de dados relacional (PostgreSQL via Docker) e apresenta as métricas num dashboard interativo.

## 🛠️ Tecnologias Utilizadas
* **Python 3:** Linguagem principal para ingestão e processamento de dados.
* **Pandas & SQLAlchemy:** Bibliotecas para manipulação do ficheiro CSV e comunicação com o banco de dados.
* **Docker:** Utilizado para criar e isolar o ambiente do banco de dados PostgreSQL.
* **PostgreSQL:** Banco de dados relacional onde os dados processados e as *views* analíticas foram armazenados.
* **Streamlit & Plotly:** Frameworks utilizados para a construção do dashboard interativo e visualização gráfica dos dados.

## ⚙️ Configuração do Ambiente e Execução

### 1. Preparação do Banco de Dados (Docker)
Para iniciar o banco de dados PostgreSQL, certifique-se de que o Docker Desktop está a correr e execute o seguinte comando no terminal:
```bash
docker run --name postgres-iot -e POSTGRES_PASSWORD=sua_senha -p 5432:5432 -d postgres