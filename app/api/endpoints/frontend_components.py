from fastapi import FastAPI, APIRouter
from typing import List
from app.crud.workflow import get_panel_components
from app.schemas.frontend_schemas.components import Panel

router = APIRouter()

@router.get("/panel_components", response_model=List[Panel])
async def panel_components():
    response = await get_panel_components()
    return response