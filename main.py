from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
import os

from routes.auth import router as auth
from routes.user import router as user
from routes.my_classes import router as my_classes
from routes.event import router as event
from routes.history_outs import router as passes
from database import engine, get_db
from database import Base

app = FastAPI()

# Создаем под-приложение для API с префиксом /api
api_app = FastAPI(title="API", version="1.0.0")

# Подключаем все роутеры к api_app
api_app.include_router(auth, prefix="/auth", tags=["auth"])
api_app.include_router(user, prefix="/user", tags=["user"])
api_app.include_router(event, prefix="/event", tags=["event"])
api_app.include_router(my_classes, prefix="/my-classes", tags=["my_classes"])
api_app.include_router(passes, prefix="/passes", tags=["passes"])

# Монтируем API приложение под префиксом /api
app.mount("/api", api_app)

# Middleware
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Статические файлы
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
app.mount("/static", StaticFiles(directory="dist/static"), name="static")

# Health check endpoint
@api_app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working"}

# Обслуживание статических файлов из dist
@app.get("/{filename:path}")
async def serve_root_files(filename: str):
    file_path = os.path.join("dist", filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse("dist/index.html")

# React app routing
@app.get("/app/{catchall:path}")
async def serve_react_app(catchall: str):
    return FileResponse("dist/index.html")

@app.get("/")
async def root_redirect():
    return RedirectResponse(url='/app')