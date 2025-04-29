# 📦 Tech Challenge FIAP Machine Learning API

Este projeto é uma **API REST** desenvolvida com **Flask**, utilizando **autenticação JWT** para proteger seus endpoints. A estrutura foi organizada seguindo boas práticas de modularidade, facilitando a manutenção e escalabilidade do sistema.

## ⚙️ Funcionalidades

### 🔐 Autenticação

- **Endpoint:** `POST /auth/login`  
- Gera tokens JWT com validade de **30 minutos** para autenticação de usuários.

### 🕷️ Execução do Crawler

- **Endpoint:** `POST /crawler/executar`  
- Realiza o download de arquivos CSV e armazena os dados na **camada bronze-layer**

## **1. Configuração Inicial**

### **1.1. Clonar o Repositório**
Certifique-se de que o repositório está clonado no seu ambiente local:

```bash
git clone <url-do-repositorio>
cd tech-challenge-fiap-machine-learning-api
```

### **1.2. Criar e Ativar o Ambiente Virtual**

#### **Windows**
```bash
python -m venv venv
.venv\Scripts\activate
```

#### **Linux/Mac**
```bash
python -m venv venv
source venv/bin/activate
```

### **1.3. Instalar Dependências**
Instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### **1.4. Configuração de Variáveis de Ambiente**
Crie um arquivo chamado `.env` na raiz do projeto e adicione a seguinte variável:

```bash
JWT_SECRET_KEY=<sua_chave_secreta>
```
---

## **2. Executar a API**

### **2.1. Iniciar o Servidor**
Execute o arquivo `app.py` para iniciar o servidor Flask:

```bash
python -m api.app
```

O servidor será iniciado em:  
`http://127.0.0.1:5000`

---

## **3. Autenticação**

### **3.1. Endpoint de Login**
Para acessar os endpoints protegidos, você precisa obter um token JWT. Use o endpoint `/auth/login`.

#### **Via Terminal**
```bash
curl -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}'
```

#### **Via Insomnia**
1. Crie uma nova requisição:
   - **Método**: `POST`
   - **URL**: `http://127.0.0.1:5000/auth/login`
2. Vá para a aba **Body** e selecione **JSON**.
3. Adicione o seguinte conteúdo:
   ```json
   {
     "username": "admin",
     "password": "admin"
   }
   ```
4. Envie a requisição.

**Resposta Esperada**  
Se as credenciais forem válidas, você receberá um token JWT:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Copie o valor de `access_token`.

---

## **4. Executar o Crawler**

### **4.1. Endpoint do Crawler**
O endpoint `/crawler/executar` baixa os arquivos CSV para a camada `bronze-layer`.

#### **Via Terminal**
```bash
curl -X POST http://127.0.0.1:5000/crawler/executar -H "Authorization: Bearer <seu_token_jwt>"
```

#### **Via Insomnia**
1. Crie uma nova requisição:
   - **Método**: `POST`
   - **URL**: `http://127.0.0.1:5000/crawler/executar`
2. Vá para a aba **Headers** e adicione:
   - **Key**: `Authorization`
   - **Value**: `Bearer <seu_token_jwt>`
3. Envie a requisição.

**Resposta Esperada**  
```json
{
  "mensagem": "Crawler executado com sucesso!"
}
```

Os arquivos CSV serão baixados na pasta `bronze-layer`.

---

## **5. Consultar Dados da Camada Gold**

### **5.1. Endpoint de Consulta**
O endpoint `/data/consulta/<tabela>` permite consultar os dados de uma tabela específica da camada `gold-layer`.

#### **Via Terminal**
```bash
curl -X GET http://127.0.0.1:5000/data/consulta/ExpEspumantes -H "Authorization: Bearer <seu_token_jwt>"
```

#### **Via Insomnia**
1. Crie uma nova requisição:
   - **Método**: `GET`
   - **URL**: `http://127.0.0.1:5000/data/consulta/ExpEspumantes`
2. Vá para a aba **Headers** e adicione:
   - **Key**: `Authorization`
   - **Value**: `Bearer <seu_token_jwt>`
3. Envie a requisição.

**Resposta Esperada**  
Se a tabela for encontrada:

```json
{
  "mensagem": "Tabela 'ExpEspumantes' acessada com sucesso!",
  "usuario": "admin",
  "dados": [
    {
      "pais": "africa_do_sul",
      "ano": 1970,
      "kilograms": 0,
      "dollars": 0
    },
    {
      "pais": "alemanha",
      "ano": 1970,
      "kilograms": 0,
      "dollars": 0
    }
  ]
}
```

---

## **6. Estrutura do Projeto**

Certifique-se de que a estrutura do projeto está organizada assim:

```
tech-challenge-fiap-machine-learning-api/
├── api/
│   ├── app.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── crawler_routes.py
│   │   └── data_routes.py
├── crawler/
│   ├── __init__.py
│   ├── config.py
│   ├── scraper/
│   │   ├── __init__.py
│   │   └── downloader.py
├── data/
│   ├── bronze-layer/
│   ├── gold-layer/
│   ├── silver-layer/
├── venv/
├── requirements.txt
├── README.md
```