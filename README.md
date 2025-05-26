# 📦 Tech Challenge FIAP Machine Learning API

Este projeto é uma **API REST** desenvolvida com **Flask**, utilizando **autenticação JWT** para proteger seus endpoints. A estrutura foi organizada seguindo boas práticas de modularidade, facilitando a manutenção e escalabilidade do sistema. A API realiza **coleta automatizada de dados da Embrapa** e expõe os dados já tratados para consumo por aplicações externas ou modelos de machine learning.

## ⚙️ Funcionalidades

### 🔐 Autenticação

* **Endpoint:** `POST /auth/login`
* Gera tokens JWT com validade de **30 minutos** para autenticação de usuários.

### 🕷️ Coleta e Processamento de Dados (Crawler)

* **Endpoint:** `POST /crawler/executar`
* Realiza:

  1. Download dos dados brutos do site da Embrapa (camada Bronze)
  2. Limpeza e padronização (camada Silver)
  3. Curadoria final e dados prontos para uso (camada Gold)

### 📊 Consulta Pública de Dados

* **Endpoint:** `GET /<categoria>/<subcategoria>`
* Exemplo: `/exportacao/suco`, `/producao/default`
* Consulta os dados atualizados diretamente da camada Gold
* O crawler é executado automaticamente antes de servir os dados 💡

---

## **1. Configuração Inicial**

### **1.1. Clonar o Repositório**

```bash
git clone <url-do-repositorio>
cd tech-challenge-fiap-machine-learning-api
```

### **1.2. Criar e Ativar o Ambiente Virtual**

#### Windows

```bash
python -m venv venv
.venv\Scripts\activate
```

#### Linux/Mac

```bash
python -m venv venv
source venv/bin/activate
```

### **1.3. Instalar Dependências**

```bash
pip install -r requirements.txt
```

### **1.4. Configuração de Variáveis de Ambiente**

Crie um arquivo `.env` com:

```bash
JWT_SECRET_KEY=<sua_chave_secreta>
```

---

## **2. Executar a API**

### **2.1. Iniciar o Servidor**

```bash
python -m api.app
```

API disponível em: `http://127.0.0.1:5000`

Acesse a documentação Swagger UI: `http://127.0.0.1:5000/apidocs`

---

## **3. Autenticação**

### **3.1. Endpoint de Login**

```bash
POST /auth/login
```

#### Body (JSON):

```json
{
  "username": "user",
  "password": "user"
}
```

#### Exemplo de resposta:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## **4. Executar Crawler Manualmente**

### **4.1. Endpoint Protegido**

```bash
POST /crawler/executar
```

Requer header:

```http
Authorization: Bearer <seu_token>
```

---

## **5. Consultar Dados Tratados (Gold Layer)**

### **5.1. Exemplo de endpoint público:**

```bash
GET /exportacao/suco
GET /importacao/espumantes
GET /producao/default
```

#### Requer header:

```http
Authorization: Bearer <seu_token>
```

A cada consulta, o pipeline completo é executado automaticamente (para fins de demonstração do MVP).

#### Exemplo de resposta:

```json
{
  "mensagem": "Dados de exportacao/suco carregados com sucesso!",
  "usuario": "user",
  "dados": [
    {"pais": "alemanha", "ano": 1970, "kilograms": 0, "dollars": 0},
    {"pais": "brasil", "ano": 1971, "kilograms": 100, "dollars": 2000}
  ]
}
```

---

## **6. Estrutura do Projeto**

```
tech-challenge-fiap-machine-learning-api/
├── api/
│   ├── app.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── crawler.py
│   │   └── data.py
├── crawler/
│   ├── scraper/
│   │   └── downloader.py
│   └── __init__.py
├── pipelines/
│   ├── etl/
│   │   ├── bronze_to_silver/
│   │   │   └── main.py
│   │   └── silver_to_gold/
│   │       └── main.py
├── data/
│   ├── bronze-layer/
│   ├── silver-layer/
│   └── gold-layer/
├── requirements.txt
├── README.md
└── .env
```

---

## 🚀 Cenário de Aplicação com Machine Learning

Esta API pode alimentar modelos de previsão de:

* Exportações futuras de vinhos ou sucos
* Produção estimada para o próximo ano
* Análise de sazonalidade e demanda

Em cenários reais, a atualização automática do pipeline seria feita por agendamento (Jenkins, cron, Airflow), e não a cada consulta.

Para este MVP, **cada chamada executa o pipeline para garantir dados atualizados e demonstrar o fluxo completo.**

---


