import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi

from typing import List
from pydantic import BaseModel

# Rutas
from app.routes.auth import router as auth_router
from app.routes.competencias import router as competencias_router
from app.routes.problemas import router as problemas_router
from app.routes.maratones import router as maratones_router
from app.routes.avances import router as avances_router
from app.routes.premios import router as premios_router
from app.routes.resolver_problemas import router as resolver_problema_router


# ✅ Define primero la ruta de MEDIA_DIR (fuera del app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "media")



# ✅ Crea la carpeta si no existe
os.makedirs(MEDIA_DIR, exist_ok=True)

# ✅ Crea instancia FastAPI
app = FastAPI(
    title="Mi API",
    version="1.0.0",
    description="API para gestionar autenticación, competencias, avances y problemas.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ✅ CORS
origins = ["http://localhost", "http://127.0.0.1:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Monta la carpeta /media
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# ✅ Monta assets estáticos
app.mount("/assets", StaticFiles(directory="app/frontend/assets"), name="assets")

# ✅ Routers
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(competencias_router, prefix="/competencias", tags=["Competencias"])
app.include_router(problemas_router, prefix="/problemas", tags=["Problemas"])
app.include_router(avances_router, prefix="/avances", tags=["Avances"])
app.include_router(maratones_router, prefix="/maratones", tags=["Maratones"])
app.include_router(premios_router, prefix="/premios", tags=["Premios"])
app.include_router(resolver_problema_router, prefix="/resolver", tags=["Resolver Problemas"])

# ✅ Ruta raíz
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

# ✅ Registro temporal
class RegistroUsuario(BaseModel):
    nombre: str
    email: str
    password: str
    is_profesor: bool

@app.post("/registro")
def registrar_usuario(datos: RegistroUsuario):
    return {"mensaje": f"Usuario {datos.nombre} registrado correctamente"}

# ✅ OpenAPI personalizado
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "auth/login",
                    "scopes": {},
                }
            },
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ✅ Servir HTMLs directos
@app.get("/maratonesEstudiantes", response_class=HTMLResponse)
def estudiante():
    with open("app/frontend/maratonEstudiantes.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/maratonesProfesores", response_class=HTMLResponse)
def profesor():
    with open("app/frontend/maratonProfesores.html", "r", encoding="utf-8") as f:
        return f.read()