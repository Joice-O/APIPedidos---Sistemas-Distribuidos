from decimal import Decimal, ROUND_HALF_UP

from app.models.pedido import Pedido, StatusPedido
from app.repositories.pedido_repository import PedidoRepository
from app.schemas.pedido import PedidoCreate


class PedidoNaoEncontradoError(Exception):
    pass


class PedidoService:
    def __init__(self, repository: PedidoRepository):
        self.repository = repository

    def criar(self, dados: PedidoCreate) -> Pedido:
        valor_total = (
            Decimal(dados.quantidade) * dados.valor_unitario
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        pedido = Pedido(
            cliente=dados.cliente,
            produto=dados.produto,
            quantidade=dados.quantidade,
            valor_unitario=dados.valor_unitario,
            valor_total=valor_total,
            status=StatusPedido.CRIADO,
        )
        return self.repository.criar(pedido)

    def buscar_por_id(self, pedido_id: int) -> Pedido:
        pedido = self.repository.buscar_por_id(pedido_id)
        if pedido is None:
            raise PedidoNaoEncontradoError(pedido_id)
        return pedido

    def listar(self) -> list[Pedido]:
        return self.repository.listar()

    def alterar_status(self, pedido_id: int, novo_status: StatusPedido) -> Pedido:
        pedido = self.buscar_por_id(pedido_id)
        return self.repository.alterar_status(pedido, novo_status)
