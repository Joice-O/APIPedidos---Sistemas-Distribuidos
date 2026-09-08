from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pedido import Pedido, StatusPedido


class PedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Pedido | None:
        return self.db.get(Pedido, pedido_id)

    def listar(self) -> list[Pedido]:
        stmt = select(Pedido).order_by(Pedido.id.asc())
        return list(self.db.scalars(stmt).all())

    def alterar_status(self, pedido: Pedido, novo_status: StatusPedido) -> Pedido:
        pedido.status = novo_status
        self.db.commit()
        self.db.refresh(pedido)
        return pedido
