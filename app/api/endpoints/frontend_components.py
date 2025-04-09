from fastapi import FastAPI, APIRouter
from typing import List, Dict, Any
from app.crud.workflow import get_panel_components, get_configs
from app.schemas.frontend_schemas.components import Panel

router = APIRouter()

@router.get("/panel_components", response_model=List[Panel])
async def panel_components():
    response = await get_panel_components()
    return response

@router.get("/asset_configs", response_model= List)
async def configs(node_id):
    response = await get_configs(node_id)
    return response