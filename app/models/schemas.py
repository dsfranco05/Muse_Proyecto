from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# ------------------------------
# Modelos para Usuarios
# ------------------------------
class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    es_profesor: bool = False

class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    password: str
    es_profesor: bool = False
    
class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True  
# ------------------------------
# Modelos para Maratones
# ------------------------------
class ProblemaMaratonBase(BaseModel):
    descripcion: str
    puntos_problema: int

class ProblemaMaratonCreate(ProblemaMaratonBase):
    pass

class ProblemaMaratonResponse(ProblemaMaratonBase):
    id: int
    maraton_id: int
    
    class Config:
        from_attributes = True

class MaratonBase(BaseModel):
    nombre: str
    descripcion: str
    tiempo_limite: int
    fecha_inicio: datetime
    fecha_fin: datetime

class MaratonCreate(MaratonBase):
    problemas: list[ProblemaMaratonCreate] = []

class MaratonResponse(MaratonBase):
    id: int
    problemas: list[ProblemaMaratonResponse] = []
    
    class Config:
        from_attributes = True
# ------------------------------
# Modelos para Competencias
# ------------------------------
class CompetenciaBase(BaseModel):
    nombre: str
    descripcion: str

class CompetenciaCreate(CompetenciaBase):
    pass

class CompetenciaResponse(CompetenciaBase):
    id: int

    class Config:
        from_attributes = True  

# ------------------------------
# Modelos para Avances
# ------------------------------
class AvanceBase(BaseModel):
    estudiante_id: int
    competencia: str  
    porcentaje_avance: float  

class AvanceCreate(AvanceBase):
    pass

class AvanceUpdate(BaseModel):
    porcentaje_avance: float  

class AvanceResponse(AvanceBase):
    id: int

    class Config:
        from_attributes = True  

# ------------------------------
# Modelos para Problemas
# ------------------------------
class ProblemaBase(BaseModel):
    id: int
    titulo: str
    descripcion: str
    puntos_problema: int
    competencia_id: int
    archivo_pdf: Optional[str] = None  # ✅ nuevo campo
    
class ProblemaCreate(ProblemaBase):
    pass

class ProblemaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    puntos_problema: int
    competencia_id: int
    archivo_pdf: Optional[str] = None

    class Config:
        orm_mode = True


# ------------------------------
# Modelos para Premios
# ------------------------------
class PremioBase(BaseModel):
    estudiante_id: int
    descripcion: str
    fecha_otorgado: date  

class PremioCreate(PremioBase):
    nombre: str  

class PremioResponse(PremioBase):
    id: int  

    class Config:
        from_attributes = True

# ------------------------------
# Modelos para Soluciones
# ------------------------------
class SolucionBase(BaseModel):
    problema_id: int
    estudiante_id: int
    archivo: str
    calificacion: Optional[int] = None
    comentario: Optional[str] = None
    fecha_subida: Optional[datetime] = None

class SolucionCreate(BaseModel):
    problema_id: int
    estudiante_id: int
    archivo: str

class SolucionCalificar(BaseModel):
    calificacion: int
    comentario: Optional[str] = None

class SolucionResponse(SolucionBase):
    id: int

    class Config:
        from_attributes = True

