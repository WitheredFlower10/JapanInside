"""CRUD operations for Ville, Attraction, and Recette models."""

from typing import List, Optional

import models
import schemas
from sqlalchemy.orm import Session, joinedload

# ---------- Villes ----------


def create_ville(db: Session, ville: schemas.VilleCreate) -> models.Ville:
    """Create a new Ville in the database.

    Args:
        db (Session): SQLAlchemy database session.
        ville (schemas.VilleCreate): Ville data to create.

    Returns:
        models.Ville: The created Ville object.
    """
    db_ville = models.Ville(**ville.dict())
    db.add(db_ville)
    db.commit()
    db.refresh(db_ville)
    return db_ville


def get_villes(db: Session, limit: int = 100) -> List[models.Ville]:
    """Retrieve a list of Villes from the database.

    Args:
        db (Session): SQLAlchemy database session.
        limit (int, optional): Maximum number of Villes to return.
            Defaults to 100.

    Returns:
        List[models.Ville]: List of Ville objects.
    """
    return (
        db.query(models.Ville)
        .options(
            joinedload(models.Ville.attractions),
            joinedload(models.Ville.recettes),
        )
        .limit(limit)
        .all()
    )


def get_ville(db: Session, ville_id: int) -> Optional[models.Ville]:
    """Retrieve a single Ville by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        ville_id (int): ID of the Ville.

    Returns:
        Optional[models.Ville]: The Ville object or None if not found.
    """
    return db.query(models.Ville).filter(models.Ville.id == ville_id).first()


def update_ville(
    db: Session, ville_id: int, ville_data: schemas.VilleCreate
) -> Optional[models.Ville]:
    """Update an existing Ville.

    Args:
        db (Session): SQLAlchemy database session.
        ville_id (int): ID of the Ville to update.
        ville_data (schemas.VilleCreate): Data to update the Ville with.

    Returns:
        Optional[models.Ville]: Updated Ville object or None if not found.
    """
    db_ville = get_ville(db, ville_id)
    if db_ville:
        for key, value in ville_data.dict(exclude_unset=True).items():
            setattr(db_ville, key, value)
        db.commit()
        db.refresh(db_ville)
    return db_ville


def delete_ville(db: Session, ville_id: int) -> bool:
    """Delete a Ville by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        ville_id (int): ID of the Ville to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    db_ville = get_ville(db, ville_id)
    if db_ville:
        db.delete(db_ville)
        db.commit()
        return True
    return False


# ---------- Attractions ----------


def create_attraction(
    db: Session, attraction: schemas.AttractionCreate
) -> models.Attraction:
    """Create a new Attraction in the database.

    Args:
        db (Session): SQLAlchemy database session.
        attraction (schemas.AttractionCreate): Attraction data to create.

    Returns:
        models.Attraction: The created Attraction object.
    """
    db_attraction = models.Attraction(**attraction.dict())
    db.add(db_attraction)
    db.commit()
    db.refresh(db_attraction)
    return db_attraction


def get_attractions(
    db: Session, ville_id: Optional[int] = None
) -> List[models.Attraction]:
    """Retrieve a list of Attractions, optionally filtered by Ville.

    Args:
        db (Session): SQLAlchemy database session.
        ville_id (Optional[int], optional): Ville ID to filter attractions.
            Defaults to None.

    Returns:
        List[models.Attraction]: List of Attraction objects.
    """
    query = db.query(models.Attraction)
    if ville_id is not None:
        query = query.filter(models.Attraction.ville_id == ville_id)
    return query.all()


def get_attraction(
    db: Session, attraction_id: int
) -> Optional[models.Attraction]:
    """Retrieve a single Attraction by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        attraction_id (int): ID of the Attraction.

    Returns:
        Optional[models.Attraction]: The Attraction object.
            Or None if not found.
    """
    return (
        db.query(models.Attraction)
        .filter(models.Attraction.id == attraction_id)
        .first()
    )


def update_attraction(
    db: Session, attraction_id: int, attraction_data: schemas.AttractionCreate
) -> Optional[models.Attraction]:
    """Update an existing Attraction.

    Args:
        db (Session): SQLAlchemy database session.
        attraction_id (int): ID of the Attraction to update.
        attraction_data (AttractionCreate): Data to update the Attraction with.

    Returns:
        Optional[Attraction]: Updated Attraction object or None if not found.
    """
    db_attraction = get_attraction(db, attraction_id)
    if db_attraction:
        for key, value in attraction_data.dict(exclude_unset=True).items():
            setattr(db_attraction, key, value)
        db.commit()
        db.refresh(db_attraction)
    return db_attraction


def delete_attraction(db: Session, attraction_id: int) -> bool:
    """Delete an Attraction by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        attraction_id (int): ID of the Attraction to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    db_attraction = get_attraction(db, attraction_id)
    if db_attraction:
        db.delete(db_attraction)
        db.commit()
        return True
    return False


# ---------- Recettes ----------


def create_recette(
    db: Session,
    recette: schemas.RecetteCreate,
    ville_ids: Optional[List[int]] = None,
) -> models.Recette:
    """Create a new Recette and optionally link to Villes.

    Args:
        db (Session): SQLAlchemy database session.
        recette (schemas.RecetteCreate): Recette data to create.
        ville_ids (Optional, optional): List of Ville IDs to link.
            Defaults to None.

    Returns:
        models.Recette: The created Recette object.
    """
    db_recette = models.Recette(**recette.dict())
    db.add(db_recette)
    db.commit()
    db.refresh(db_recette)

    if ville_ids:
        villes = (
            db.query(models.Ville).filter(models.Ville.id.in_(ville_ids)).all()
        )
        for ville in villes:
            ville.recettes.append(db_recette)
        db.commit()

    return db_recette


def get_recettes(
    db: Session, ville_id: Optional[int] = None
) -> List[models.Recette]:
    """Retrieve a list of Recettes, optionally filtered by Ville.

    Args:
        db (Session): SQLAlchemy database session.
        ville_id (Optional, optional): Ville ID to filter recettes.
            Defaults to None.

    Returns:
        List[models.Recette]: List of Recette objects.
    """
    query = db.query(models.Recette)
    if ville_id is not None:
        query = query.join(models.Ville.recettes).filter(
            models.Ville.id == ville_id
        )
    return query.all()


def get_recette(db: Session, recette_id: int) -> Optional[models.Recette]:
    """Retrieve a single Recette by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        recette_id (int): ID of the Recette.

    Returns:
        Optional[models.Recette]: The Recette object or None if not found.
    """
    return (
        db.query(models.Recette)
        .filter(models.Recette.id == recette_id)
        .first()
    )


def update_recette(
    db: Session,
    recette_id: int,
    recette_data: schemas.RecetteCreate,
    ville_ids: Optional[List[int]] = None,
) -> Optional[models.Recette]:
    """Update an existing Recette and optionally update linked Villes.

    Args:
        db (Session): SQLAlchemy database session.
        recette_id (int): ID of the Recette to update.
        recette_data (schemas.RecetteCreate): Data to update the Recette with.
        ville_ids (Optional, optional): List of Ville IDs to link.
            Defaults to None.

    Returns:
        Optional[models.Recette]: Updated Recette object or None if not found.
    """
    db_recette = get_recette(db, recette_id)
    if db_recette:
        for key, value in recette_data.dict(exclude_unset=True).items():
            setattr(db_recette, key, value)
        if ville_ids is not None:
            db_recette.villes = (
                db.query(models.Ville)
                .filter(models.Ville.id.in_(ville_ids))
                .all()
            )
        db.commit()
        db.refresh(db_recette)
    return db_recette


def delete_recette(db: Session, recette_id: int) -> bool:
    """Delete a Recette by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        recette_id (int): ID of the Recette to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    db_recette = get_recette(db, recette_id)
    if db_recette:
        db.delete(db_recette)
        db.commit()
        return True
    return False
