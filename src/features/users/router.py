from fastapi import APIRouter

from .create.router import router as create_router
from .login.router import router as login_router
from .delete.router import router as delete_router
from .update.router import router as update_router
from .verify_email.router import router as verify_email_router

router = APIRouter(
    prefix="/users"
)

router.include_router(create_router)
router.include_router(login_router)
router.include_router(update_router)
router.include_router(delete_router)
router.include_router(verify_email_router)
