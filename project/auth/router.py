from fastapi import APIRouter, HTTPException, status, Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from asgiref.sync import sync_to_async
from .schemas import SUserRegister, SUserAuth
from .auth_service import create_access_token,validate_and_decode_token
from fastapi import Request
from fastapi.encoders import jsonable_encoder

import logging
logger = logging.getLogger(__name__)


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register")
async def register_user(user_data: SUserRegister) -> dict:
    user_exists = await sync_to_async(User.objects.filter(email=user_data.email).exists)()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )

    await sync_to_async(User.objects.create)(
        username=user_data.username,
        email=user_data.email,
        password=make_password(user_data.password)
    )
    return {'message': 'Successfully registered!'}

@router.post("/login")
async def auth_user(response: Response, user_data: SUserAuth):
    user = await sync_to_async(User.objects.filter(email=user_data.email).first)()
    if not user or not check_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )

    access_token = create_access_token({"sub": str(user.id)})

    response.set_cookie(key="users_access_token", value=access_token, httponly=True)

    return {'ok': 200}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'User successfully logged out'}


@router.get("/validate-token")
async def validate_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing in cookies",
        )
    try:
    
        payload = validate_and_decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        
    
        user = await sync_to_async(User.objects.get)(id=user_id)

    
        return {
            "status": "ok",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
            }
        }
    except User.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

