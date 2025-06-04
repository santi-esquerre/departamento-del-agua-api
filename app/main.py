from fastapi import FastAPI, Depends
from .db import init_db
from app.deps import get_current_admin

# Importamos los routers directamente desde sus módulos
from app.routes.archivos import router as archivos_router
from app.routes.personal import router as personal_router
from app.routes.publicaciones import router as publicaciones_router
from app.routes.proyectos import router as proyectos_router
from app.routes.equipamiento import router as equipamiento_router
from app.routes.servicios import router as servicios_router
from app.routes.academico import router as academico_router
from app.routes.blog import router as blog_router
from app.routes import auth
from app.routes.subscribers import router as subscribers_router

# Configuración mejorada para Swagger
app = FastAPI(
    title="API Departamento del Agua",
    description="API para gestionar recursos del departamento del agua",
    version="0.1.1",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
async def on_startup():
    await init_db()


# Incluir routers de forma explícita
app.include_router(archivos_router)
app.include_router(personal_router)
app.include_router(publicaciones_router)
app.include_router(proyectos_router)
app.include_router(equipamiento_router)
app.include_router(servicios_router)
app.include_router(academico_router)
app.include_router(blog_router)
# Suscripciones (público)
app.include_router(subscribers_router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"status": "ok"}
