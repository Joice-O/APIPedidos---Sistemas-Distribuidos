from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.pedidos import router as pedidos_router
from app.database import inicializar_banco


@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_banco()
    yield


app = FastAPI(
    title="API de Pedidos",
    version="1.0.0",
    description="Trabalho 1 - Desenvolvimento de Sistemas Distribuídos",
    lifespan=lifespan,
)

app.include_router(pedidos_router)


@app.get("/health", tags=["Saúde"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {
        "mensagem": "API de Pedidos em execução",
        "documentacao": "/docs",
    }
