from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Solucion(Base):
    __tablename__ = "soluciones"

    id = Column(Integer, primary_key=True, index=True)
    problema_id = Column(Integer, ForeignKey("problemas.id"), nullable=False)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    archivo = Column(String, nullable=False)
    calificacion = Column(Integer, nullable=True)
    comentario = Column(String, nullable=True)
    fecha_subida = Column(DateTime, default=datetime.utcnow)

    problema = relationship("Problema")
    estudiante = relationship("Usuario")
