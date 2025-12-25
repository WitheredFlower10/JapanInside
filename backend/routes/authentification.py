from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
router = APIRouter()

# Mot de passe admin
ADMIN_PASSWORD = "Tajini"
security = HTTPBasic()

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    return True

@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    verify_password(credentials)
    return {"success": True, "admin": True, "message": "Connexion réussie"}

@router.get("/admin/data")
async def get_admin_data(auth: bool = Depends(verify_password)):
    return {"data": "Données admin"}

