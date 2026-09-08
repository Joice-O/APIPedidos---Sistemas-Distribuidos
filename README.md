# API de Pedidos — Trabalho 1

Projeto da disciplina **Desenvolvimento de Sistemas Distribuídos**. A solução implementa uma API de Pedidos em **FastAPI** com persistência em **PostgreSQL**, organizada em camadas de API, Service e Repository e executada integralmente com Docker Compose.

## Integrantes

Arthur Gomes Rodrigues de Lima | CC8Q13 | N284GB-8   
Repositório: https://github.com/ArthurR06/APIPedidos---Sistemas-Distribuidos

Joice Oliveira Jardim          | CC8Q13 | N284DJ-1           
Repositório: https://github.com/Joice-O/APIPedidos---Sistemas-Distribuidos

## Arquitetura

Cliente HTTP/JSON
       |
       v
+-------------------------------+
| Container: pedidos            |
| FastAPI                       |
|  API -> Service -> Repository |
+---------------+---------------+
                |
                | PostgreSQL
                v
+-------------------------------+
| Container: postgres           |
| PostgreSQL + volume persistente|
+-------------------------------+

A API, a camada de serviço e o repositório permanecem no mesmo processo/container. O PostgreSQL executa em um container separado.

## Estrutura do projeto

├── app/
│   ├── main.py
│   ├── database.py
│   ├── api/
│   │   └── pedidos.py
│   ├── services/
│   │   └── pedido_service.py
│   ├── repositories/
│   │   └── pedido_repository.py
│   ├── models/
│   │   └── pedido.py
│   └── schemas/
│       └── pedido.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

## Pré-requisitos

- Git
- Docker com Docker Compose

Não é necessário instalar Python, PostgreSQL ou dependências manualmente na máquina.

## Como executar exatamente a versão entregue

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
git checkout APIPedidos-1-final
docker compose up -d --build
```

Depois da inicialização:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- OpenAPI: http://localhost:8000/openapi.json

Para encerrar os containers sem apagar os dados:

```bash
docker compose down
```

Para encerrar e apagar também o volume do PostgreSQL:

```bash
docker compose down -v
```

## Modelo de Pedido

Cada pedido possui:

- `id`: identificador gerado pelo banco;
- `cliente`: identificação textual do cliente;
- `produto`: identificação textual do produto;
- `quantidade`: quantidade solicitada, maior que zero;
- `valor_unitario`: preço de uma unidade, maior que zero;
- `valor_total`: calculado automaticamente pela aplicação;
- `status`: `CRIADO`, `CONFIRMADO` ou `CANCELADO`;
- `data_criacao`: data e hora de registro do pedido.

O cliente **não envia** `valor_total`, `status` ou `data_criacao` na criação. Esses campos são definidos pela aplicação.

## Endpoints

### Saúde da aplicação

```http
GET /health
```

Resposta:

```json
{
  "status": "ok"
}
```

### Criar pedido

```http
POST /pedidos
Content-Type: application/json
```

Exemplo:

```json
{
  "cliente": "Maria Silva",
  "produto": "Teclado Mecânico",
  "quantidade": 2,
  "valor_unitario": 199.90
}
```

Resposta esperada: **201 Created**. O `valor_total` é calculado automaticamente e o status inicial é `CRIADO`.

### Consultar pedido por ID

```http
GET /pedidos/1
```

- **200 OK**: pedido encontrado;
- **404 Not Found**: pedido inexistente.

### Listar pedidos

```http
GET /pedidos
```

Retorna a coleção de pedidos persistidos.

### Alterar status

```http
PATCH /pedidos/1/status
Content-Type: application/json
```

Exemplo:

```json
{
  "status": "CONFIRMADO"
}
```

Status aceitos: `CRIADO`, `CONFIRMADO` e `CANCELADO`.

## Testes realizados

A aplicação foi testada pelo Swagger do FastAPI em:

```text
http://localhost:8000/docs
```

Foram validados:

- `GET /health`;
- criação de pedido com `POST /pedidos`;
- listagem com `GET /pedidos`;
- consulta individual com `GET /pedidos/{id}`;
- alteração de status com `PATCH /pedidos/{id}/status`;
- retorno **404 Not Found** para pedido inexistente;
- retorno **422 Unprocessable Entity** para quantidade inválida;
- cálculo automático do `valor_total`;
- persistência dos pedidos após reiniciar somente o container da aplicação.

Exemplo utilizado durante os testes:

```json
{
  "cliente": "Arthur",
  "produto": "Teclado",
  "quantidade": 2,
  "valor_unitario": 150
}
```

O pedido foi criado com valor total `300.00` e status inicial `CRIADO`.

## Teste rápido com curl

Criar:

```bash
curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente":"Maria Silva","produto":"Teclado Mecânico","quantidade":2,"valor_unitario":199.90}'
```

Listar:

```bash
curl http://localhost:8000/pedidos
```

Consultar:

```bash
curl http://localhost:8000/pedidos/1
```

Alterar status:

```bash
curl -X PATCH http://localhost:8000/pedidos/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"CONFIRMADO"}'
```

Saúde:

```bash
curl http://localhost:8000/health
```

## Persistência

O PostgreSQL usa o volume Docker `pedidos_postgres_data`. Assim, reiniciar apenas o container `pedidos` não apaga os pedidos já cadastrados.

Exemplo do experimento:

```bash
# 1. Crie um pedido
curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente":"Teste","produto":"Produto A","quantidade":1,"valor_unitario":10.00}'

# 2. Reinicie somente a aplicação
docker compose restart pedidos

# 3. Consulte novamente
curl http://localhost:8000/pedidos/1
```

## Configuração

O projeto funciona sem arquivo `.env`, usando valores padrão no `docker-compose.yml`. Se necessário, copie `.env.example` para `.env` e altere:

```env
POSTGRES_DB=pedidos
POSTGRES_USER=pedidos
POSTGRES_PASSWORD=pedidos
```

A aplicação recebe a conexão com o banco pela variável de ambiente `DATABASE_URL`; ela não fica fixa no código de negócio.

## Versão entregue

A versão final avaliada está identificada pela tag:
`APIPedidos-1-final`
