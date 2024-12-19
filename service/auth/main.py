import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.auth.router import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(title="Auth Service", version="1.0")

    # Добавление CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)

    return app

def main():
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )

if __name__ == "__main__":
    main()
