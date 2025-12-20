from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any


class VilleBase(BaseModel):
    nom: str
    position: Optional[int] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None
    meilleure_saison: Optional[str] = None
    climat: Optional[str] = None
 

class AttractionBase(BaseModel):
    nom: str
    description: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    ville_id: int

class RecetteBase(BaseModel):
    nom: str
    description: Optional[str] = None
    ingredients: Optional[str] = None
    
class Ville(VilleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Attraction(AttractionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Recette(RecetteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AttractionCreate(BaseModel):
    nom: str
    description: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

class RecetteCreate(BaseModel):
    nom: str
    description: Optional[str] = None
    ingredients: Optional[str] = None

class VilleCreate(BaseModel):
    nom: str
    position: Optional[int] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None
    meilleure_saison: Optional[str] = None
    climat: Optional[str] = None

    attractions: Optional[List[AttractionCreate]] = []
    recettes: Optional[List[RecetteCreate]] = []



class AttractionOut(BaseModel):
    id: int
    nom: str
    description: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class RecetteOut(BaseModel):
    id: int
    nom: str
    description: Optional[str]
    ingredients: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class VilleOut(BaseModel):
    id: int
    nom: str
    position: Optional[int]
    description: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    population: Optional[int]
    meilleure_saison: Optional[str]
    climat: Optional[str]
    attractions: List[AttractionOut] = []
    recettes: List[RecetteOut] = []
    model_config = ConfigDict(from_attributes=True)