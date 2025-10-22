from fastapi import APIRouter

from .auth import auth_router, users_router
from .politics import politics_admin_router, politics_public_router

api_router_v1 = APIRouter(prefix="/api/v1")

# subrouters
api_router_v1.include_router(auth_router)
api_router_v1.include_router(users_router)
api_router_v1.include_router(politics_public_router)
api_router_v1.include_router(politics_admin_router)
