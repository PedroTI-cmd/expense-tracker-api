# 💸 Expense Tracker API

API REST para controle de gastos pessoais, construída com **FastAPI**, **PostgreSQL** e **Docker**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Tests](https://img.shields.io/badge/testes-11%20passando-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

## Funcionalidades

- **Autenticação JWT** — registro, login e proteção de rotas com Bearer token
- **Gastos** — criar, listar (com filtros por data, categoria e valor), editar, excluir
- **Categorias** — personalizáveis por usuário, com remoção segura (gastos viram "sem categoria")
- **Relatórios** — resumo mensal total e por categoria
- **Isolamento de dados** — cada usuário acessa somente seus próprios registros
- **Documentação automática** — Swagger UI disponível em `/docs`

## Stack

| Camada | Tecnologia |
|---|---|
| Framework | FastAPI |
| Banco de dados | PostgreSQL 16 |
| ORM | SQLAlchemy 2 (async-ready) |
| Migrations | Alembic |
| Autenticação | JWT via python-jose |
| Hash de senha | bcrypt via passlib |
| Validação | Pydantic v2 |
| Testes | pytest + httpx |
| Infraestrutura | Docker + Docker Compose |

## Arquitetura

```
app/
├── api/v1/routes/       # Endpoints HTTP (auth, categorias, gastos)
├── core/                # Config, segurança (JWT/bcrypt), banco, tipos customizados
├── models/              # Models SQLAlchemy (tabelas)
├── schemas/             # Schemas Pydantic (validação de entrada e saída)
├── services/            # Regras de negócio
├── repositories/        # Acesso ao banco de dados
tests/                   # Testes automatizados com pytest
migrations/              # Migrations Alembic
```

O projeto segue separação em camadas: **rota → serviço → repositório → banco**. Regras de negócio ficam nos serviços, nunca nas rotas ou repositórios.

## Rodando com Docker (recomendado)

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/) instalados

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/expense-tracker-api.git
cd expense-tracker-api

# 2. Crie o arquivo de variáveis de ambiente
cp .env.example .env
# Edite o .env e defina um SECRET_KEY seguro:
# openssl rand -hex 32

# 3. Suba os containers (a API já roda as migrations automaticamente)
docker compose up --build

# A API estará disponível em http://localhost:8000
# Documentação interativa: http://localhost:8000/docs
```

## Rodando localmente (sem Docker)

### Pré-requisitos
- Python 3.12+
- PostgreSQL rodando localmente

```bash
# 1. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure o .env
cp .env.example .env
# Ajuste DATABASE_URL para apontar pro seu Postgres local

# 4. Rode as migrations
alembic upgrade head

# 5. Suba a API
uvicorn app.main:app --reload
```

## Endpoints

### Autenticação

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/v1/auth/register` | Cadastrar usuário |
| POST | `/api/v1/auth/login` | Login e obter token JWT |

### Categorias *(requer autenticação)*

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/v1/categorias` | Listar categorias |
| POST | `/api/v1/categorias` | Criar categoria |
| PUT | `/api/v1/categorias/{id}` | Editar categoria |
| DELETE | `/api/v1/categorias/{id}` | Excluir categoria |

### Gastos *(requer autenticação)*

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/v1/gastos` | Listar gastos (filtros: `category_id`, `date_from`, `date_to`, `min_amount`, `max_amount`) |
| POST | `/api/v1/gastos` | Criar gasto |
| GET | `/api/v1/gastos/{id}` | Detalhar gasto |
| PATCH | `/api/v1/gastos/{id}` | Editar gasto |
| DELETE | `/api/v1/gastos/{id}` | Excluir gasto |
| GET | `/api/v1/gastos/resumo-mensal?year=2026&month=7` | Resumo mensal por categoria |

### Exemplo de uso

```bash
# Registrar
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "eu@exemplo.com", "password": "minhasenha123"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "eu@exemplo.com", "password": "minhasenha123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Criar gasto
curl -X POST http://localhost:8000/api/v1/gastos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": "Almoço", "amount": "35.50", "expense_date": "2026-07-20"}'

# Resumo do mês
curl "http://localhost:8000/api/v1/gastos/resumo-mensal?year=2026&month=7" \
  -H "Authorization: Bearer $TOKEN"
```

## Testes

```bash
# Roda toda a suíte (usa SQLite em memória, não precisa de Postgres)
pytest -v

# Com cobertura
pytest --cov=app --cov-report=term-missing
```

## Decisões técnicas relevantes

**Decimal em vez de float para valores monetários** — `float` causa erros de arredondamento (ex: `0.1 + 0.2 = 0.30000000000000004`). Valores monetários usam `Numeric(12, 2)` no banco e `Decimal` no Python.

**Tipo GUID portável** — UUID nativo do Postgres em produção; CHAR(32) em outros bancos. Isso permite rodar testes com SQLite sem precisar de Postgres.

**Separação rota/serviço/repositório** — regras de negócio ficam nos serviços, nunca nas rotas. Repositórios abstraem o acesso ao banco. Isso facilita testes unitários e futura troca de banco.

**Exceções de domínio customizadas** — `NotFoundError`, `AlreadyExistsError`, `InvalidCredentialsError` são lançadas pelos serviços e traduzidas para HTTP codes pelas rotas. A camada HTTP não vaza para o domínio.

## Contribuindo

Contribuições são bem-vindas! Veja o arquivo `CONTRIBUTING.md` para instruções.

## Licença

MIT — veja o arquivo [LICENSE](LICENSE).
