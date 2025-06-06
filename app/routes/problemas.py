from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.problemas import Problema
from app.models.competencias import Competencia  # Asegúrate de importar Competencia
from app.models.schemas import ProblemaCreate, ProblemaResponse, SolucionResponse, SolucionCalificar
from typing import List
from fastapi.responses import FileResponse
import os
from app.routes.auth import get_current_user
from app.models.solucion import Solucion
from app.models.usuarios import Usuario


router = APIRouter(tags=["Problemas"])

@router.post("", response_model=ProblemaResponse, summary="Crear Problema")
def crear_problema(problema: ProblemaCreate, db: Session = Depends(get_db)):
    # Verificar que la competencia existe
    competencia = db.query(Competencia).filter(Competencia.id == problema.competencia_id).first()
    if not competencia:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")

    nuevo_problema = Problema(
        titulo=problema.titulo,
        descripcion=problema.descripcion,
        competencia_id=problema.competencia_id,
        puntos_problema=problema.puntos_problema
    )
    db.add(nuevo_problema)
    db.commit()
    db.refresh(nuevo_problema)
    return nuevo_problema

@router.get("/{competencia_id}", response_model=List[ProblemaResponse], summary="Ver Problemas")
def ver_problemas(competencia_id: int, db: Session = Depends(get_db)):
    # Verificar que la competencia existe
    competencia = db.query(Competencia).filter(Competencia.id == competencia_id).first()
    if not competencia:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")

    problemas = db.query(Problema).filter(Problema.competencia_id == competencia_id).all()
    return problemas or []

UPLOAD_PATH = "media/problemas"
SOLUCIONES_PATH = "media/soluciones"

@router.post("/subir_solucion/{problema_id}")
def subir_solucion(
    problema_id: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    os.makedirs(SOLUCIONES_PATH, exist_ok=True)

    extension = archivo.filename.split(".")[-1]
    if extension not in ["py", "cpp", "pdf"]:
        raise HTTPException(status_code=400, detail="Solo se permiten archivos .py, .cpp o .pdf")

    # Normaliza el nombre del archivo
    nombre_archivo = f"{problema_id}_{usuario.id}_{archivo.filename}".replace(" ", "_")
    ruta_relativa = f"soluciones/{nombre_archivo}"  # para guardar en la base de datos
    ruta_completa = os.path.join("media", ruta_relativa)

    # Guarda el archivo en disco
    with open(ruta_completa, "wb") as f:
        f.write(archivo.file.read())

    # Crea el registro en la base de datos
    nueva = Solucion(
        archivo=ruta_relativa,
        problema_id=problema_id,
        estudiante_id=usuario.id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return {"mensaje": "Solución subida correctamente", "archivo": ruta_relativa}


@router.get("/soluciones/{problema_id}", response_model=List[SolucionResponse])
def ver_soluciones_de_problema(
    problema_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    if not usuario.es_profesor:
        raise HTTPException(status_code=403, detail="Solo profesores pueden ver las soluciones.")

    soluciones = db.query(Solucion).filter(Solucion.problema_id == problema_id).all()
    return soluciones

@router.put("/calificar_solucion/{solucion_id}")
def calificar_solucion(
    solucion_id: int,
    datos: SolucionCalificar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    if not usuario.es_profesor:
        raise HTTPException(status_code=403, detail="Solo los profesores pueden calificar.")

    solucion = db.query(Solucion).filter(Solucion.id == solucion_id).first()
    if not solucion:
        raise HTTPException(status_code=404, detail="Solución no encontrada.")

    solucion.calificacion = datos.calificacion
    solucion.comentario = datos.comentario
    db.commit()
    db.refresh(solucion)

    return {"mensaje": "Solución calificada correctamente."}

@router.get("/mis_soluciones", response_model=List[SolucionResponse])
def ver_mis_soluciones(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    if usuario.es_profesor:
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden ver sus soluciones.")

    return db.query(Solucion).filter(Solucion.estudiante_id == usuario.id).all()
