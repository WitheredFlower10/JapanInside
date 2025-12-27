from fastapi import APIRouter

router = APIRouter()

@router.get("/health", response_model=dict)
async def health_check():
    """Return the API health status."""
    return {
        "status": "healthy",
        "service": "Japan Inside API",
        "version": "1.0.0",
        "description": "Consulter les villes, attractions et recettes japonaises",
        "endpoints": {
            "hello": "/api/hello",
            "villes": "/api/villes",
            "ville_detail": "/api/villes/{nom_ville}",
            "recettes": "/api/recettes",
            "create_ville": "/api/villes [POST]",
            "create_recette": "/api/recettes [POST]",
            "flush_db": "/api/flushDB [POST]",
            "setup_db": "/api/createDB [POST]",
            "insert_data": "/api/insertDATA [POST]",
        },
    }

