from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.pedido_repository import PedidoRepository
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoStatusUpdate
from app.services.pedido_service import PedidoNaoEncontradoError, PedidoService


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def get_service(db: Session = Depends(get_db)) -> PedidoService:
    return PedidoService(PedidoRepository(db))


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    dados: PedidoCreate,
    service: PedidoService = Depends(get_service),
) -> PedidoResponse:
    return service.criar(dados)


@router.get("/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(
    pedido_id: int,
    service: PedidoService = Depends(get_service),
) -> PedidoResponse:
    try:
        return service.buscar_por_id(pedido_id)
    except PedidoNaoEncontradoError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(
    service: PedidoService = Depends(get_service),
) -> list[PedidoResponse]:
    return service.listar()


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def alterar_status_pedido(
    pedido_id: int,
    dados: PedidoStatusUpdate,
    service: PedidoService = Depends(get_service),
) -> PedidoResponse:
    try:
        return service.alterar_status(pedido_id, dados.status)
    except PedidoNaoEncontradoError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )
