import os
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://pedidos:pedidos@postgres:5432/pedidos",
)

engine_options = {"pool_pre_ping": True}
if DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def inicializar_banco(max_tentativas: int = 30, intervalo_segundos: int = 2) -> None:
    # Importa os models antes do create_all para registrá-los no metadata.
    from app.models.pedido import Pedido  # noqa: F401

    ultima_excecao: Exception | None = None

    for _ in range(max_tentativas):
        try:
            with engine.connect() as conexao:
                conexao.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError as exc:
            ultima_excecao = exc
            time.sleep(intervalo_segundos)

    raise RuntimeError("Não foi possível conectar ao PostgreSQL.") from ultima_excecao
