from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Problema(Base):
    __tablename__ = "problemas"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    puntos_problema = Column(Integer)
    competencia_id = Column(Integer, ForeignKey("competencias.id")) 
    archivo_pdf = Column(String, nullable=True)  # ✅ Añadir esto  
    
    competencia = relationship("Competencia", back_populates="problemas")