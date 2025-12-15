from pydantic import BaseModel

class ArticleBase(BaseModel):
    titre: str
    contenu: str

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class RecetteBase(BaseModel):
    nom: str
    description: str
    ingredients: str

class RecetteCreate(RecetteBase):
    pass

class Recette(RecetteBase):
    id: int
    model_config = {
        "from_attributes": True
    }