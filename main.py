from fastapi import FastAPI, APIRouter
from views import gateway_router


app = FastAPI()
router = APIRouter()


app.include_router(router)
app.include_router(gateway_router)