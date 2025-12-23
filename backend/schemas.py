"""Pydantic schemas for Japan Inside API."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict



class VilleBase(BaseModel):
    """Define common fields for a city (Ville).

    Attributes:
        nom (str): Name of the city.
        position (Optional[int]): Order in the itinerary.
        description (Optional[str]): Description of the city.
        latitude (Optional[float]): Latitude coordinate.
        longitude (Optional[float]): Longitude coordinate.
        population (Optional[int]): Population of the city.
        meilleure_saison (Optional[str]): Best season to visit.
        climat (Optional[str]): Climate description.
    """

    nom: str
    position: Optional[int] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None
    meilleure_saison: Optional[str] = None
    climat: Optional[str] = None


class AttractionBase(BaseModel):
    """Define common fields for an attraction.

    Attributes:
        nom (str): Name of the attraction.
        description (Optional[str]): Description of the attraction.
        longitude (Optional[float]): Longitude coordinate.
        latitude (Optional[float]): Latitude coordinate.
        ville_id (int): ID of the associated city.
    """

    nom: str
    description: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    ville_id: int


class RecetteBase(BaseModel):
    """Define common fields for a culinary recipe.

    Attributes:
        nom (str): Name of the recipe.
        description (Optional[str]): Description of the recipe.
        ingredients (Optional[str]): Ingredients of the recipe.
    """

    nom: str
    description: Optional[str] = None
    ingredients: Optional[str] = None




class Ville(VilleBase):
    """Define Ville schema for output with ID.

    Attributes:
        id (int): Unique identifier of the city.
    """

    id: int
    model_config = ConfigDict(from_attributes=True)


class Attraction(AttractionBase):
    """Define Attraction schema for output with ID.

    Attributes:
        id (int): Unique identifier of the attraction.
    """

    id: int
    model_config = ConfigDict(from_attributes=True)


class Recette(RecetteBase):
    """Define Recette schema for output with ID.

    Attributes:
        id (int): Unique identifier of the recipe.
    """

    id: int
    model_config = ConfigDict(from_attributes=True)



class AttractionCreate(AttractionBase):
    """Define Attraction creation schema."""

    pass


class RecetteCreate(RecetteBase):
    """Define Recette creation schema."""

    pass


class VilleCreate(VilleBase):
    """Define Ville creation schema including nested attractions and recipes.

    Attributes:
        attractions (Optional[List[AttractionCreate]]): List of attractions.
        recettes (Optional[List[RecetteCreate]]): List of recipes.
    """

    attractions: Optional[List[AttractionCreate]] = []
    recettes: Optional[List[RecetteCreate]] = []



class AttractionOut(AttractionBase):
    """Define Attraction output schema for nested relations.

    Attributes:
        id (int): Unique identifier of the attraction.
    """

    id: int
    model_config = ConfigDict(from_attributes=True)


class RecetteOut(RecetteBase):
    """Define Recette output schema for nested relations.

    Attributes:
        id (int): Unique identifier of the recipe.
    """

    id: int
    model_config = ConfigDict(from_attributes=True)


class VilleOut(VilleBase):
    """Define Ville output schema including nested attractions and recipes.

    Attributes:
        id (int): Unique identifier of the city.
        attractions (List[AttractionOut]): List of nested attractions.
        recettes (List[RecetteOut]): List of nested recipes.
    """

    id: int
    attractions: List[AttractionOut] = []
    recettes: List[RecetteOut] = []
    model_config = ConfigDict(from_attributes=True)



class VilleOrder(BaseModel):
    """Define schema to reorder cities in the itinerary.

    Attributes:
        id (int): ID of the city.
        position (int): New position in the itinerary.
    """

    id: int
    position: int
