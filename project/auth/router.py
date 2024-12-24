from fastapi import APIRouter, HTTPException, status, Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from asgiref.sync import sync_to_async
from .schemas import SUserRegister, SUserAuth
from .auth_service import create_access_token

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post("/register/")
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

@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    user = await sync_to_async(User.objects.filter(email=user_data.email).first)()
    if not user or not check_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )
    
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token}

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'User successfully logged out'}
