from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, ConflictoMaceda as ConflictoMacedaModel, TierrasTitulomerced as TierrasTitulomercedModel
from schemas import ConflictoMaceda, TierrasTitulomerced, ConflictoFiltroOpciones, TierrasFiltroOpciones
from typing import List, Dict, Any
from sqlalchemy import func

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/conflicto/all", response_model=List[ConflictoMaceda])
def read_all_conflicto(db: Session = Depends(get_db)):
    items = db.query(ConflictoMacedaModel).all()
    return [ConflictoMaceda.from_orm(item) for item in items]

@app.get("/tierras/all", response_model=List[TierrasTitulomerced])
def read_all_tierras(db: Session = Depends(get_db)):
    items = db.query(TierrasTitulomercedModel).all()
    return [TierrasTitulomerced.from_orm(item) for item in items]

@app.get("/conflicto/", response_model=List[ConflictoMaceda])
def read_conflicto(
    skip: int = 0, 
    limit: int = 100, 
    año: int = None, 
    comuna: str = None, 
    provincia: str = None, 
    region: str = None, 
    tipo_evento: str = None, 
    actor: str = None, 
    propiedad_dañada: str = None, 
    actor_tipo_1: str = None,
    actor_tipo_2: str = None,
    actor_mapuche: str = None,
    mapuche_identificado: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(ConflictoMacedaModel)
    if año:
        query = query.filter(ConflictoMacedaModel.año == año)
    if comuna:
        query = query.filter(ConflictoMacedaModel.comuna == comuna)
    if provincia:
        query = query.filter(ConflictoMacedaModel.provincia == provincia)
    if region:
        query = query.filter(ConflictoMacedaModel.region == region)
    if tipo_evento:
        query = query.filter(ConflictoMacedaModel.evento_tipo_maceda == tipo_evento)
    if actor:
        query = query.filter((ConflictoMacedaModel.actor_tipo_1_nombre == actor) | (ConflictoMacedaModel.actor_tipo_2_nombre == actor))
    if propiedad_dañada:
        query = query.filter(ConflictoMacedaModel.propiedad_dañada == propiedad_dañada)
    if actor_tipo_1:
        query = query.filter(ConflictoMacedaModel.actor_tipo_1 == actor_tipo_1)
    if actor_tipo_2:
        query = query.filter(ConflictoMacedaModel.actor_tipo_2 == actor_tipo_2)
    if actor_mapuche:
        query = query.filter(ConflictoMacedaModel.actor_mapuche == actor_mapuche)
    if mapuche_identificado:
        query = query.filter(ConflictoMacedaModel.mapuche_identificado == mapuche_identificado)
    
    items = query.offset(skip).limit(limit).all()
    return [ConflictoMaceda.from_orm(item) for item in items]

@app.get("/tierras/", response_model=List[TierrasTitulomerced])
def read_tierras(
    skip: int = 0, 
    limit: int = 100, 
    region: str = None, 
    provincia: str = None, 
    comuna: str = None, 
    beneficiario: str = None, 
    año: int = None, 
    area_min: float = None, 
    area_max: float = None, 
    tdm_numero: str = None,
    tdm_letra: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(TierrasTitulomercedModel)
    if region:
        query = query.filter(TierrasTitulomercedModel.region_nombre == region)
    if provincia:
        query = query.filter(TierrasTitulomercedModel.provincia_nombre == provincia)
    if comuna:
        query = query.filter(TierrasTitulomercedModel.comuna_nombre == comuna)
    if beneficiario:
        query = query.filter(TierrasTitulomercedModel.tdm_beneficiario == beneficiario)
    if año:
        query = query.filter(TierrasTitulomercedModel.tdm_año == año)
    if area_min:
        query = query.filter(TierrasTitulomercedModel.tdm_area >= area_min)
    if area_max:
        query = query.filter(TierrasTitulomercedModel.tdm_area <= area_max)
    if tdm_numero:
        query = query.filter(TierrasTitulomercedModel.tdm_numero == tdm_numero)
    if tdm_letra:
        query = query.filter(TierrasTitulomercedModel.tdm_letra == tdm_letra)
    
    items = query.offset(skip).limit(limit).all()
    return [TierrasTitulomerced.from_orm(item) for item in items]

@app.get("/conflicto/count_by/{campo}", response_model=List[Dict[str, int]])
def count_conflicto_by(campo: str, db: Session = Depends(get_db)):
    if campo not in ["año", "tipo_evento", "region"]:
        raise HTTPException(status_code=400, detail="Campo no válido")
    results = db.query(getattr(ConflictoMacedaModel, campo), func.count(ConflictoMacedaModel.id).label('count')).group_by(getattr(ConflictoMacedaModel, campo)).all()
    return [{campo: r[0], 'count': r[1]} for r in results]

@app.get("/tierras/area_by/{campo}", response_model=List[Dict[str, float]])
def area_tierras_by(campo: str, db: Session = Depends(get_db)):
    if campo not in ["region", "provincia", "comuna"]:
        raise HTTPException(status_code=400, detail="Campo no válido")
    results = db.query(getattr(TierrasTitulomercedModel, campo), func.sum(TierrasTitulomercedModel.tdm_area).label('total_area')).group_by(getattr(TierrasTitulomercedModel, campo)).all()
    return [{campo: r[0], 'total_area': r[1]} for r in results]

@app.get("/cross_data/by/{campo}", response_model=List[Dict[str, Any]])
def read_cross_data_by(campo: str, db: Session = Depends(get_db)):
    if campo not in ["comuna", "provincia", "region"]:
        raise HTTPException(status_code=400, detail="Campo no válido")
    conflicto_data = db.query(ConflictoMacedaModel).all()
    tierras_data = db.query(TierrasTitulomercedModel).all()
    cross_data = []
    for conflicto in conflicto_data:
        for tierra in tierras_data:
            if getattr(conflicto, campo) == getattr(tierra, f"{campo}_nombre"):
                cross_data.append({
                    "conflicto_id": conflicto.id,
                    "conflicto_comuna": conflicto.comuna,
                    "tierra_id": tierra.id,
                    "tierra_comuna": tierra.comuna_nombre
                })
    return cross_data

@app.get("/summary/by/{campo}", response_model=Dict[str, Any])
def summary_by(campo: str, db: Session = Depends(get_db)):
    if campo not in ["año", "comuna", "region"]:
        raise HTTPException(status_code=400, detail="Campo no válido")
    conflicto_count = db.query(func.count(ConflictoMacedaModel.id)).group_by(getattr(ConflictoMacedaModel, campo)).all()
    tierras_area = db.query(func.sum(TierrasTitulomercedModel.tdm_area)).group_by(getattr(TierrasTitulomercedModel, campo)).all()
    return {'conflicto_count': conflicto_count, 'total_area': tierras_area}

@app.get("/conflicto/{conflicto_id}", response_model=ConflictoMaceda)
def read_conflicto_by_id(conflicto_id: int, db: Session = Depends(get_db)):
    conflicto = db.query(ConflictoMacedaModel).filter(ConflictoMacedaModel.id == conflicto_id).first()
    if not conflicto:
        raise HTTPException(status_code=404, detail="Conflicto not found")
    return ConflictoMaceda.from_orm(conflicto)

@app.get("/tierras/{tierra_id}", response_model=TierrasTitulomerced)
def read_tierras_by_id(tierra_id: int, db: Session = Depends(get_db)):
    tierra = db.query(TierrasTitulomercedModel).filter(TierrasTitulomercedModel.id == tierra_id).first()
    if not tierra:
        raise HTTPException(status_code=404, detail="Tierra not found")
    return TierrasTitulomerced.from_orm(tierra)

@app.get("/filtro_opciones/conflicto", response_model=ConflictoFiltroOpciones, response_model_exclude_unset=True)
def get_conflicto_filtro_opciones(db: Session = Depends(get_db)):
    años = db.query(ConflictoMacedaModel.año).distinct().all()
    comunas = db.query(ConflictoMacedaModel.comuna).distinct().all()
    provincias = db.query(ConflictoMacedaModel.provincia).distinct().all()
    regiones = db.query(ConflictoMacedaModel.region).distinct().all()
    tipos_evento = db.query(ConflictoMacedaModel.evento_tipo_maceda).distinct().all()
    actores_1 = db.query(ConflictoMacedaModel.actor_tipo_1_nombre).distinct().all()
    actores_2 = db.query(ConflictoMacedaModel.actor_tipo_2_nombre).distinct().all()
    actor_tipo_1 = db.query(ConflictoMacedaModel.actor_tipo_1).distinct().all()
    actor_tipo_2 = db.query(ConflictoMacedaModel.actor_tipo_2).distinct().all()
    actor_mapuche = db.query(ConflictoMacedaModel.actor_mapuche).distinct().all()
    mapuche_identificado = db.query(ConflictoMacedaModel.mapuche_identificado).distinct().all()
    ubicacion_tipo = db.query(ConflictoMacedaModel.ubicacion_tipo).distinct().all()
    rural = db.query(ConflictoMacedaModel.rural).distinct().all()
    evento_especifico = db.query(ConflictoMacedaModel.evento_especifico).distinct().all()
    actor_especifico_1 = db.query(ConflictoMacedaModel.actor_especifico_1).distinct().all()
    actor_especifico_1_num = db.query(ConflictoMacedaModel.actor_especifico_1_num).distinct().all()
    actor_especifico_1_armas = db.query(ConflictoMacedaModel.actor_especifico_1_armas).distinct().all()
    actor_relacionado_1 = db.query(ConflictoMacedaModel.actor_relacionado_1).distinct().all()
    actor_especifico_2 = db.query(ConflictoMacedaModel.actor_especifico_2).distinct().all()
    actor_especifico_2_num = db.query(ConflictoMacedaModel.actor_especifico_2_num).distinct().all()
    actor_especifico_2_armas = db.query(ConflictoMacedaModel.actor_especifico_2_armas).distinct().all()
    actor_relacionado_2 = db.query(ConflictoMacedaModel.actor_relacionado_2).distinct().all()
    confrontacion = db.query(ConflictoMacedaModel.confrontacion).distinct().all()
    iniciador = db.query(ConflictoMacedaModel.iniciador).distinct().all()
    descripcion = db.query(ConflictoMacedaModel.descripcion).distinct().all()
    propiedad_destruida = db.query(ConflictoMacedaModel.propiedad_destruida).distinct().all()
    propiedad_dañada = db.query(ConflictoMacedaModel.propiedad_dañada).distinct().all()
    propiedad_robada = db.query(ConflictoMacedaModel.propiedad_robada).distinct().all()
    perdida_estimada = db.query(ConflictoMacedaModel.perdida_estimada).distinct().all()
    arrestos = db.query(ConflictoMacedaModel.arrestos).distinct().all()
    heridos = db.query(ConflictoMacedaModel.heridos).distinct().all()
    muertos = db.query(ConflictoMacedaModel.muertos).distinct().all()
    
    # Convertir los resultados a listas simples y asegurarse de que los valores sean válidos
    def convertir_a_int(valor):
        try:
            return int(valor)
        except (TypeError, ValueError):
            return None

    def convertir_a_float(valor):
        try:
            return float(valor)
        except (TypeError, ValueError):
            return None

    años = [convertir_a_int(item[0]) for item in años if item[0] is not None and item[0] != '']
    comunas = [item[0] for item in comunas if item[0] is not None]
    provincias = [item[0] for item in provincias if item[0] is not None]
    regiones = [item[0] for item in regiones if item[0] is not None]
    tipos_evento = [item[0] for item in tipos_evento if item[0] is not None]
    actores = list(set([item[0] for item in actores_1 if item[0] is not None] + [item[0] for item in actores_2 if item[0] is not None]))
    actor_tipo_1 = [item[0] for item in actor_tipo_1 if item[0] is not None]
    actor_tipo_2 = [item[0] for item in actor_tipo_2 if item[0] is not None]
    actor_mapuche = [item[0] for item in actor_mapuche if item[0] is not None]
    mapuche_identificado = [item[0] for item in mapuche_identificado if item[0] is not None]
    ubicacion_tipo = [item[0] for item in ubicacion_tipo if item[0] is not None]
    rural = [item[0] for item in rural if item[0] is not None]
    evento_especifico = [item[0] for item in evento_especifico if item[0] is not None]
    actor_especifico_1 = [item[0] for item in actor_especifico_1 if item[0] is not None]
    actor_especifico_1_num = [item[0] for item in actor_especifico_1_num if item[0] is not None]
    actor_especifico_1_armas = [item[0] for item in actor_especifico_1_armas if item[0] is not None]
    actor_relacionado_1 = [item[0] for item in actor_relacionado_1 if item[0] is not None]
    actor_especifico_2 = [item[0] for item in actor_especifico_2 if item[0] is not None]
    actor_especifico_2_num = [item[0] for item in actor_especifico_2_num if item[0] is not None]
    actor_especifico_2_armas = [item[0] for item in actor_especifico_2_armas if item[0] is not None]
    actor_relacionado_2 = [item[0] for item in actor_relacionado_2 if item[0] is not None]
    confrontacion = [item[0] for item in confrontacion if item[0] is not None]
    iniciador = [item[0] for item in iniciador if item[0] is not None]
    descripcion = [item[0] for item in descripcion if item[0] is not None]
    propiedad_destruida = [item[0] for item in propiedad_destruida if item[0] is not None]
    propiedad_dañada = [item[0] for item in propiedad_dañada if item[0] is not None]
    propiedad_robada = [item[0] for item in propiedad_robada if item[0] is not None]
    perdida_estimada = [convertir_a_float(item[0]) for item in perdida_estimada if item[0] is not None and item[0] != '' and convertir_a_float(item[0]) is not None]
    arrestos = [convertir_a_int(item[0]) for item in arrestos if item[0] is not None and item[0] != '' and convertir_a_int(item[0]) is not None]
    heridos = [convertir_a_int(item[0]) for item in heridos if item[0] is not None and item[0] != '' and convertir_a_int(item[0]) is not None]
    muertos = [convertir_a_int(item[0]) for item in muertos if item[0] is not None and item[0] != '' and convertir_a_int(item[0]) is not None]
    
    return ConflictoFiltroOpciones(
        años=años,
        comunas=comunas,
        provincias=provincias,
        regiones=regiones,
        tipos_evento=tipos_evento,
        actores=actores,
        actor_tipo_1=actor_tipo_1,
        actor_tipo_2=actor_tipo_2,
        actor_mapuche=actor_mapuche,
        mapuche_identificado=mapuche_identificado,
        ubicacion_tipo=ubicacion_tipo,
        rural=rural,
        evento_especifico=evento_especifico,
        actor_especifico_1=actor_especifico_1,
        actor_especifico_1_num=actor_especifico_1_num,
        actor_especifico_1_armas=actor_especifico_1_armas,
        actor_relacionado_1=actor_relacionado_1,
        actor_especifico_2=actor_especifico_2,
        actor_especifico_2_num=actor_especifico_2_num,
        actor_especifico_2_armas=actor_especifico_2_armas,
        actor_relacionado_2=actor_relacionado_2,
        confrontacion=confrontacion,
        iniciador=iniciador,
        descripcion=descripcion,
        propiedad_destruida=propiedad_destruida,
        propiedad_dañada=propiedad_dañada,
        propiedad_robada=propiedad_robada,
        perdida_estimada=perdida_estimada,
        arrestos=arrestos,
        heridos=heridos,
        muertos=muertos
    )

@app.get("/filtro_opciones/tierras", response_model=TierrasFiltroOpciones, response_model_exclude_unset=True)
def get_tierras_filtro_opciones(db: Session = Depends(get_db)):
    regiones = db.query(TierrasTitulomercedModel.region_nombre).distinct().all()
    provincias = db.query(TierrasTitulomercedModel.provincia_nombre).distinct().all()
    comunas = db.query(TierrasTitulomercedModel.comuna_nombre).distinct().all()
    beneficiarios = db.query(TierrasTitulomercedModel.tdm_beneficiario).distinct().all()
    años = db.query(TierrasTitulomercedModel.tdm_año).distinct().all()
    numeros = db.query(TierrasTitulomercedModel.tdm_numero).distinct().all()
    letras = db.query(TierrasTitulomercedModel.tdm_letra).distinct().all()
    areas = db.query(TierrasTitulomercedModel.tdm_area).distinct().all()
    geoareas = db.query(TierrasTitulomercedModel.tdm_geoarea).distinct().all()
    perimetros = db.query(TierrasTitulomercedModel.tdm_perim).distinct().all()
    lugar = db.query(TierrasTitulomercedModel.lugar).distinct().all()
    provincia_id = db.query(TierrasTitulomercedModel.provincia_id).distinct().all()
    comuna_id = db.query(TierrasTitulomercedModel.comuna_id).distinct().all()
    tdm_original = db.query(TierrasTitulomercedModel.tdm_original).distinct().all()
    longitud_W = db.query(TierrasTitulomercedModel.longitud_W).distinct().all()
    latitud_S = db.query(TierrasTitulomercedModel.latitud_S).distinct().all()
    
    # Convertir los resultados a listas simples y asegurarse de que los valores sean válidos
    def convertir_a_int(valor):
        try:
            return int(valor)
        except (TypeError, ValueError):
            return None

    def convertir_a_float(valor):
        try:
            return float(valor)
        except (TypeError, ValueError):
            return None

    regiones = [item[0] for item in regiones if item[0] is not None]
    provincias = [item[0] for item in provincias if item[0] is not None]
    comunas = [item[0] for item in comunas if item[0] is not None]
    beneficiarios = [item[0] for item in beneficiarios if item[0] is not None]
    años = [convertir_a_int(item[0]) for item in años if item[0] is not None and item[0] != '']
    numeros = [item[0] for item in numeros if item[0] is not None]
    letras = [item[0] for item in letras if item[0] is not None]
    areas = [convertir_a_float(item[0]) for item in areas if item[0] is not None and item[0] != '' and convertir_a_float(item[0]) is not None]
    geoareas = [convertir_a_float(item[0]) for item in geoareas if item[0] is not None and item[0] != '' and convertir_a_float(item[0]) is not None]
    perimetros = [convertir_a_float(item[0]) for item in perimetros if item[0] is not None and item[0] != '' and convertir_a_float(item[0]) is not None]
    lugar = [item[0] for item in lugar if item[0] is not None]
    provincia_id = [convertir_a_int(item[0]) for item in provincia_id if item[0] is not None and item[0] != '']
    comuna_id = [convertir_a_int(item[0]) for item in comuna_id if item[0] is not None and item[0] != '']
    tdm_original = [item[0] for item in tdm_original if item[0] is not None]
    longitud_W = [convertir_a_float(item[0]) for item in longitud_W if item[0] is not None and item[0] != '' and convertir_a_float(item[0]) is not None]
    latitud_S = [convertir_a_float(item[0]) for item in latitud_S if item[0] is not None and item[0] != '' and convertir_a_float(item[0]) is not None]
    
    return TierrasFiltroOpciones(
        regiones=regiones,
        provincias=provincias,
        comunas=comunas,
        beneficiarios=beneficiarios,
        años=años,
        numeros=numeros,
        letras=letras,
        areas=areas,
        geoareas=geoareas,
        perimetros=perimetros,
        lugar=lugar,
        provincia_id=provincia_id,
        comuna_id=comuna_id,
        tdm_original=tdm_original,
        longitud_W=longitud_W,
        latitud_S=latitud_S
    )