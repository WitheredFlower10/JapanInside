from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import HTMLResponse, JSONResponse
from utils.carte_gen import generate_map_html, villes_data, itineraire, generate_japan_map
from fastapi.staticfiles import StaticFiles
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Japan Inside API")
app.mount("/static", StaticFiles(directory="utils"), name="static")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/api/hello')
def hello_world():
    return {"message": "Hello World"}

@app.get('/')
def hello_world():
    DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///:memory:"
)
    print(DATABASE_URL)
    return {}, 200

@app.get("/api/articles", response_model=list[schemas.Article])
def read_articles(db: Session = Depends(get_db)):
    return crud.get_articles(db)

@app.get("/api/carte")
def get_carte():
    return HTMLResponse(content=generate_map_html())

# Route pour la carte interactive
@app.get("/carte", response_class=HTMLResponse)
async def get_carte():
    """Retourne la carte HTML interactive"""
    html_content = generate_map_html()
    return HTMLResponse(content=html_content)

# API pour les données des villes
@app.get("/api/villes")
async def get_all_villes():
    """Retourne toutes les villes disponibles"""
    return JSONResponse(content=villes_data)

@app.get("/api/villes/{nom_ville}")
async def get_ville(nom_ville: str):
    """Retourne les détails d'une ville spécifique"""
    ville_key = nom_ville.capitalize()
    if ville_key not in villes_data:
        raise HTTPException(status_code=404, detail=f"Ville {nom_ville} non trouvée")
    return villes_data[ville_key]

@app.get("/api/itineraire")
async def get_itineraire_complet():
    """Retourne l'itinéraire complet"""
    return {
        "itineraire": itineraire,
        "etapes": [
            {
                "ordre": i+1,
                "ville": ville,
                "coords": [villes_data[ville]["latitude"], villes_data[ville]["longitude"]]
            }
            for i, ville in enumerate(itineraire[:-1])  # Exclure le dernier Tokyo
        ]
    }

# Route pour générer une nouvelle carte
@app.post("/api/carte/generate")
async def generate_new_map():
    """Génère une nouvelle carte et la sauvegarde"""
    try:
        output_path = "static/carte_japon_latest.html"
        generate_japan_map(output_path)
        return {"message": "Carte générée avec succès", "path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


# Routes existantes de votre API
@app.get('/api/hello')
def hello_world():
    return {"message": "Bienvenue sur Japan Inside API!"}

@app.get("/api/articles", response_model=list[schemas.Article])
def read_articles(db: Session = Depends(get_db)):
    """Retourne tous les articles"""
    return crud.get_articles(db)

@app.post("/api/articles", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    """Crée un nouvel article"""
    return crud.create_article(db, article)

@app.get("/api/recettes", response_model=list[schemas.Recette])
def read_recettes(db: Session = Depends(get_db)):
    """Retourne toutes les recettes"""
    return crud.get_recettes(db)

@app.post("/api/recettes", response_model=schemas.Recette)
def create_recette(recette: schemas.RecetteCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle recette"""
    return crud.create_recette(db, recette)

# Route de santé de l'API
@app.get("/health")
async def health_check():
    """Vérifie l'état de l'API"""
    return {
        "status": "healthy",
        "service": "Japan Inside API",
        "version": "1.0.0",
        "endpoints": {
            "carte": "/carte",
            "villes": "/api/villes",
            "itineraire": "/api/itineraire",
            "articles": "/api/articles",
            "recettes": "/api/recettes"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
