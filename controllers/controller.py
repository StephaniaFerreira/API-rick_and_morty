from fastapi import APIRouter, status
from services import service

router = APIRouter()

@router.get("/collect", status_code = status.HTTP_200_OK)
def importar():
    response = service.importar()
    return response

@router.get("/voice_actor/list", status_code = status.HTTP_200_OK)
def listar_dubladores():
    response = service.listar_dubladores()
    return response

@router.get("/voice_actor/{voice_actor_id}/acted_in", status_code = status.HTTP_200_OK)
def listar_episodios(voice_actor_id: int):
    retorno = service.listar_episodios(voice_actor_id)
    return retorno




