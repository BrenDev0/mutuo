from fastapi import APIRouter, Request, Body, Depends
from src.di import get_injector, Injector
from .schemas import VerifyEmailRequest
from .use_case import VerifyEmail

router = APIRouter(
    tags=["Users"]
)

@router.post("/verify-email", status_code=200)
async def verify_email(
    request: Request,
    data: VerifyEmailRequest = Body(...),
    injector: Injector = Depends(get_injector)
):
    use_case: VerifyEmail = injector.inject(VerifyEmail)
    return await use_case.execute(
        to=data.email
    )