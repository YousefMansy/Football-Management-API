from fastapi import APIRouter

from app.footballfantasyapi.api.api_v1.endpoints import team, player, auth, transfer_list

api_router = APIRouter()
api_router.include_router(team.router, prefix="/teams", tags=["Teams"])
api_router.include_router(player.router, prefix="/players", tags=["Players"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(transfer_list.router, prefix="/transfer_list", tags=["Transfer List"])
