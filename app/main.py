from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, transactions, summary, webhook

app = FastAPI(
    title="Finance Organizer API",
    description="API de gestão financeira com IA",
    version="0.1.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(transactions.router)
app.include_router(summary.router)
app.include_router(webhook.router)


@app.get("/")
def root():
    return {"message": "Finance Organizer API rodando!"}
