from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
import os

from routes.auth import router as auth
from routes.user import router as user
from routes.my_classes import router as my_classes
from routes.event import router as event
from routes.history_outs import router as passes
from database import engine, get_db
from database import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # ← Явно укажите методы
    allow_headers=["*"],
)

# ✅ ПРАВИЛЬНОЕ ПОДКЛЮЧЕНИЕ РОУТЕРОВ С ПРЕФИКСОМ /api
app.include_router(auth)
app.include_router(user)
app.include_router(event)
app.include_router(my_classes)
app.include_router(passes)

# ✅ Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is working"}

# Монтируем статические файлы
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
app.mount("/static", StaticFiles(directory="dist/static"), name="static")

# Обслуживание статических файлов
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