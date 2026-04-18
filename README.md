# Finance Organizer

Aplicação de gestão financeira pessoal com IA. Envie mensagens em linguagem natural via Telegram e a IA registra suas transações automaticamente.

---

## Stack

- **Backend:** FastAPI + SQLAlchemy + PostgreSQL
- **IA:** Groq API (llama-3.1-8b-instant)
- **Frontend:** Next.js + TypeScript + Recharts
- **Infra local:** Docker Compose
- **Mensageria:** Telegram Bot API

---

## Como rodar localmente

### Pré-requisitos
- Docker e Docker Compose
- Python 3.9+
- Node.js 18+

### Variáveis de ambiente

Crie um `.env` na raiz baseado no `.env.example`:

```
DATABASE_URL=postgresql://finance_user:finance_pass@localhost:5432/finance_db
GROQ_API_KEY=sua_chave_aqui
TELEGRAM_BOT_TOKEN=seu_token_aqui
```

### Backend

```bash
# Subir o banco de dados
docker-compose up -d

# Instalar dependências
pip install -r requirements.txt

# Rodar migrations
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Telegram (desenvolvimento local)

```bash
# Expor servidor local com ngrok
ngrok http 8000

# Registrar URL no Telegram
curl "https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://sua-url.ngrok.io/webhook/telegram"
```

---

## Documentação

Veja a pasta [`docs/`](docs/) para o roadmap detalhado de cada fase do projeto.
