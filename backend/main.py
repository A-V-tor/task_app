from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
from api import router


def create_app():
    app = FastAPI(docs_url="/docs")
    origins = [
        "http://localhost:5000",
        "http://localhost:5173",  # Vite's default port
        "http://127.0.0.1:5173",  # Vite's default port (alternative)
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app

if __name__ == "__main__":
    uvicorn.run("main:create_app", host="0.0.0.0", port=5000)  # Порты теперь совпадают