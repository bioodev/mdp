from pydantic import BaseModel, Field, validator
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class ConflictoMacedaBase(BaseModel):
    id_evento_relacionado: Optional[int] = Field(default=None)
    año: Optional[int] = Field(default=None)
    mes: Optional[int] = Field(default=None)
    trimestre: Optional[int] = Field(default=None)
    fecha_reportada: Optional[str] = Field(default=None)
    comuna: Optional[str] = Field(default=None)
    provincia: Optional[str] = Field(default=None)
    region: Optional[str] = Field(default=None)
    ubicacion_tipo: Optional[str] = Field(default=None)
    rural: Optional[str] = Field(default=None)
    evento_tipo_maceda: Optional[str] = Field(default=None)
    evento_especifico: Optional[str] = Field(default=None)
    actor_tipo_1: Optional[str] = Field(default=None)
    actor_tipo_1_nombre: Optional[str] = Field(default=None)
    actor_especifico_1: Optional[str] = Field(default=None)
    actor_especifico_1_num: Optional[str] = Field(default=None)
    actor_especifico_1_armas: Optional[str] = Field(default=None)
    actor_relacionado_1: Optional[str] = Field(default=None)
    actor_tipo_2: Optional[str] = Field(default=None)
    actor_tipo_2_nombre: Optional[str] = Field(default=None)
    actor_especifico_2: Optional[str] = Field(default=None)
    actor_especifico_2_num: Optional[str] = Field(default=None)
    actor_especifico_2_armas: Optional[str] = Field(default=None)
    actor_relacionado_2: Optional[str] = Field(default=None)
    actor_mapuche: Optional[str] = Field(default=None)
    mapuche_identificado: Optional[str] = Field(default=None)
    confrontacion: Optional[str] = Field(default=None)
    iniciador: Optional[str] = Field(default=None)
    descripcion: Optional[str] = Field(default=None)
    propiedad_destruida: Optional[str] = Field(default=None)
    propiedad_dañada: Optional[str] = Field(default=None)
    propiedad_robada: Optional[str] = Field(default=None)
    perdida_estimada: Optional[float] = Field(default=None)
    arrestos: Optional[int] = Field(default=None)
    heridos: Optional[int] = Field(default=None)
    muertos: Optional[int] = Field(default=None)
    mercurio: Optional[float] = Field(default=None)
    mella: Optional[float] = Field(default=None)
    osal: Optional[float] = Field(default=None)
    ciudadano: Optional[str] = Field(default=None)
    biobio: Optional[str] = Field(default=None)

    @validator('id_evento_relacionado', 'año', 'mes', 'trimestre', 'arrestos', 'heridos', 'muertos', pre=True, always=True)
    def parse_int(cls, v):
        if v == '' or v is None:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @validator('perdida_estimada', 'mercurio', 'mella', 'osal', pre=True, always=True)
    def parse_float(cls, v):
        if v == '' or v is None:
            return None
        try:
            return float(v)
        except ValueError:
            return None

class ConflictoMaceda(ConflictoMacedaBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class TierrasTitulomercedBase(BaseModel):
    region_nombre: Optional[str]
    provincia_id: Optional[int]
    provincia_nombre: Optional[str]
    comuna_id: Optional[int]
    comuna_nombre: Optional[str]
    lugar: Optional[str]
    tdm_beneficiario: Optional[str]
    tdm_año: Optional[int]
    tdm_original: Optional[str]
    tdm_numero: Optional[str]
    tdm_letra: Optional[str]
    tdm_area: Optional[str]
    tdm_geoarea: Optional[str]
    tdm_perim: Optional[str]
    longitud_W: Optional[float]
    latitud_S: Optional[float]
    region_id: Optional[int]

    @validator('provincia_id', 'comuna_id', 'tdm_año', 'region_id', pre=True, always=True)
    def parse_int(cls, v):
        if v == '' or v is None:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @validator('longitud_W', 'latitud_S', 'tdm_area', 'tdm_geoarea', 'tdm_perim', pre=True, always=True)
    def parse_float(cls, v):
        if v == '' or v is None:
            return None
        try:
            return float(v)
        except ValueError:
            return None

class TierrasTitulomerced(TierrasTitulomercedBase):
    id: int
    
    class Config:
        orm_mode = True
        from_attributes = True

class ConflictoFiltroOpciones(BaseModel):
    años: List[int]
    comunas: List[str]
    provincias: List[str]
    regiones: List[str]
    tipos_evento: List[str]
    actores: List[str]
    actor_tipo_1: List[str]
    actor_tipo_2: List[str]
    actor_mapuche: List[str]
    mapuche_identificado: List[str]
    ubicacion_tipo: List[str]
    rural: List[str]
    evento_especifico: List[str]
    actor_especifico_1: List[str]
    actor_especifico_1_num: List[str]
    actor_especifico_1_armas: List[str]
    actor_relacionado_1: List[str]
    actor_especifico_2: List[str]
    actor_especifico_2_num: List[str]
    actor_especifico_2_armas: List[str]
    actor_relacionado_2: List[str]
    confrontacion: List[str]
    iniciador: List[str]
    descripcion: List[str]
    propiedad_destruida: List[str]
    propiedad_dañada: List[str]
    propiedad_robada: List[str]
    perdida_estimada: List[float]
    arrestos: List[int]
    heridos: List[int]
    muertos: List[int]

class TierrasFiltroOpciones(BaseModel):
    regiones: List[str]
    provincias: List[str]
    comunas: List[str]
    beneficiarios: List[str]
    años: List[int]
    numeros: List[str]
    letras: List[str]
    areas: List[str]
    geoareas: List[str]
    perimetros: List[str]
    lugar: List[str]
    provincia_id: List[int]
    comuna_id: List[int]
    tdm_original: List[str]
    longitud_W: List[float]
    latitud_S: List[float]