# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from typing import List

Base = declarative_base()

class ConflictoMaceda(Base):
    __tablename__ = 'conflicto_maceda'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Nueva columna 'id'
    id_evento = Column(Integer, nullable=True)
    id_evento_relacionado = Column(Integer, nullable=True)
    año = Column(Integer, nullable=True)
    mes = Column(Integer, nullable=True)
    trimestre = Column(Integer, nullable=True)
    fecha_reportada = Column(String, nullable=True)  # Cambia a DateTime si estás usando datetime
    comuna = Column(String, nullable=True)
    provincia = Column(String, nullable=True)
    region = Column(String, nullable=True)
    ubicacion_tipo = Column(String, nullable=True)
    rural = Column(String, nullable=True)
    evento_tipo_maceda = Column(String, nullable=True)
    evento_especifico = Column(String, nullable=True)
    actor_tipo_1 = Column(String, nullable=True)
    actor_tipo_1_nombre = Column(String, nullable=True)
    actor_especifico_1 = Column(String, nullable=True)
    actor_especifico_1_num = Column(String, nullable=True)
    actor_especifico_1_armas = Column(String, nullable=True)
    actor_relacionado_1 = Column(String, nullable=True)
    actor_tipo_2 = Column(String, nullable=True)
    actor_tipo_2_nombre = Column(String, nullable=True)
    actor_especifico_2 = Column(String, nullable=True)
    actor_especifico_2_num = Column(String, nullable=True)
    actor_especifico_2_armas = Column(String, nullable=True)
    actor_relacionado_2 = Column(String, nullable=True)
    actor_mapuche = Column(String, nullable=True)
    mapuche_identificado = Column(String, nullable=True)
    confrontacion = Column(String, nullable=True)
    iniciador = Column(String, nullable=True)
    descripcion = Column(String, nullable=True)
    propiedad_destruida = Column(String, nullable=True)
    propiedad_dañada = Column(String, nullable=True)
    propiedad_robada = Column(String, nullable=True)
    perdida_estimada = Column(Float, nullable=True)
    arrestos = Column(Integer, nullable=True)
    heridos = Column(Integer, nullable=True)
    muertos = Column(Integer, nullable=True)
    mercurio = Column(Float, nullable=True)
    mella = Column(Float, nullable=True)
    osal = Column(Float, nullable=True)
    ciudadano = Column(String, nullable=True)
    biobio = Column(String, nullable=True)

class TierrasTitulomerced(Base):
    __tablename__ = 'tierras_titulomerced'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Nueva columna 'id'
    region_id = Column(Integer)
    region_nombre = Column(String)
    provincia_id = Column(Integer)
    provincia_nombre = Column(String)
    comuna_id = Column(Integer)
    comuna_nombre = Column(String)
    lugar = Column(String)
    tdm_beneficiario = Column(String)
    tdm_año = Column(Integer)
    tdm_original = Column(String)
    tdm_numero = Column(String)
    tdm_letra = Column(String)
    tdm_area = Column(String)
    tdm_geoarea = Column(String)
    tdm_perim = Column(String)
    longitud_W = Column(Float)
    latitud_S = Column(Float)

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./mdp.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)
