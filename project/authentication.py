import httpx
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

import logging
logger = logging.getLogger(__name__)


class CookieTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("users_access_token")
        if not token:
            raise AuthenticationFailed("Authentication credentials were not provided.")

        try:

            response = httpx.get(
                "http://localhost:8001/auth/validate-token",
                headers={"Cookie": f"users_access_token={token}"},
                timeout=5.0  # Таймаут для запроса
            )
            logger.info(f"{response.status_code} RESUUUUUUUUUUUUUUUUUUUUUUUUULTTTTTTTTTTTTTTTTTTTTTTTTT {response.text}")
            if response.status_code == 200:

                payload = response.json()
                user_data = payload.get("user") 
                
                if not user_data:
                    raise AuthenticationFailed("Invalid response from the authentication server.")
                logger.info(f"USER {user_data}")
                user = self.get_or_create_user(user_data)
                return user, token
                
            else:
                raise AuthenticationFailed("Invalid or expired token.")
        except httpx.RequestError as exc:
            raise AuthenticationFailed(f"Token validation service unavailable: {exc}")

        return None

    def get_or_create_user(self, user_data):
        user_info = user_data.get("user")
        logger.info(f"US    ER {user_data}")

        try:
            user, created = User.objects.update_or_create(
                id=user_data.get("id"),
                defaults={
                    "username": user_data.get("username"),
                    "email": user_data.get("email"),
                    "is_staff": user_data.get("is_staff", False),
                    "is_active": user_data.get("is_active", True),
                    "is_superuser": user_data.get('is_superuser',False),
                },
            )
            return user
        except Exception as e:
            raise AuthenticationFailed(f"Error while creating user: {e}")
