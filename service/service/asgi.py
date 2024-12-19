"""
ASGI config for service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from service.auth.router import router as auth_router


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')
django_asgi_app = get_asgi_application()


def get_application() -> FastAPI:
    app = FastAPI(title="Book Service", version="1.0")

    # Добавление CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.mount("/auth", auth_app)
    app.mount("/django", WSGIMiddleware(django_asgi_app))
    app.include_router(auth_router)

    return app


# Combine Django and FastAPI

# Final application
application = get_application()
