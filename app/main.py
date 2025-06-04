from fastapi import FastAPI, APIRouter, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from pydantic import BaseModel

# Routers personalizados
from app.routes.auth import router as auth_router
from app.routes.competencias import router as competencias_router
from app.routes.problemas import router as problemas_router
from app.routes.maratones import router as maratones_router
from app.routes.avances import router as avances_router
from app.routes.premios import router as premios_router
from app.routes.resolver_problemas import router as resolver_problema_router

# ✅ Instancia única
app = FastAPI(
    title="Mi API",
    version="1.0.0",
    description="API para gestionar autenticación, competencias, avances y problemas.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ✅ CORS para permitir conexión desde Live Server u otros entornos
origins = [
    "http://localhost",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Incluir routers
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

# ✅ Registro de usuario (temporal, puedes moverlo a auth)
class RegistroUsuario(BaseModel):
    nombre: str
    email: str
    password: str
    is_profesor: bool

@app.post("/registro")
def registrar_usuario(datos: RegistroUsuario):
    print(f"Datos recibidos: {datos}")
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

# ✅ Servir archivos estáticos (css, js, imgs)
app.mount("/assets", StaticFiles(directory="app/frontend/assets"), name="assets")

# ✅ Servir archivos HTML directamente desde app/frontend
@app.get("/maratonesEstudiantes", response_class=HTMLResponse)
def estudiante():
    with open("app/frontend/maratonEstudiantes.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/maratonesProfesores", response_class=HTMLResponse)
def profesor():
    with open("app/frontend/maratonProfesores.html", "r", encoding="utf-8") as f:
        return f.read()




