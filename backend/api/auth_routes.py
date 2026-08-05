from fastapi import APIRouter
from fastapi import Depends

from auth.auth_service import AuthService

from api.dependencies import get_auth_service

from schemas.user_register import UserRegister
from schemas.user_response import UserResponse

from schemas.api_success import APISuccess


router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)


@router.post(

    "/register",

    response_model=APISuccess[UserResponse]

)

def register(

    request: UserRegister,

    auth_service: AuthService = Depends(
        get_auth_service
    )

):

    user = auth_service.register(
        request
    )

    return APISuccess(
        data=user
    )