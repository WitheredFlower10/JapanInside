"""Database models for Japan Inside API."""

from database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

ville_recette = Table(
    "ville_recette",
    Base.metadata,
    Column("ville_id", Integer, ForeignKey("villes.id"), primary_key=True),
    Column("recette_id", Integer, ForeignKey("recettes.id"), primary_key=True),
)


class Ville(Base):
    """Represent a city (ville) in Japan.

    Attributes:
        id (int): Primary key.
        nom (str): Name of the ville.
        position (int): Order in the itinerary.
        description (str): Description of the ville.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
        population (int): Population of the ville.
        meilleure_saison (str): Best season to visit.
        climat (str): Climate description.
        attractions (list[Attraction]): List of related attractions.
        recettes (list[Recette]): List of related recettes.
    """

    __tablename__ = "villes"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    position = Column(Integer)
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    population = Column(Integer)
    meilleure_saison = Column(String(100))
    climat = Column(Text)

    attractions = relationship(
        "Attraction", back_populates="ville", cascade="all, delete"
    )
    recettes = relationship(
        "Recette", secondary=ville_recette, back_populates="villes"
    )


class Attraction(Base):
    """Represent an attraction linked to a ville.

    Attributes:
        id (int): Primary key.
        nom (str): Name of the attraction.
        description (str): Description of the attraction.
        longitude (float): Longitude coordinate.
        latitude (float): Latitude coordinate.
        ville_id (int): Foreign key to associated Ville.
        ville (Ville): Relationship to parent Ville.
    """

    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    longitude = Column(Float)
    latitude = Column(Float)

    ville_id = Column(Integer, ForeignKey("villes.id"), nullable=False)
    ville = relationship("Ville", back_populates="attractions")


class Recette(Base):
    """Represent a culinary recipe (recette) in Japan.

    Attributes:
        id (int): Primary key.
        nom (str): Name of the recette.
        description (str): Description of the recette.
        ingredients (str): Ingredients of the recette.
        villes (list[Ville]): List of villes linked to this recette.
    """

    __tablename__ = "recettes"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    ingredients = Column(Text)

    villes = relationship(
        "Ville", secondary=ville_recette, back_populates="recettes"
    )
