from pydantic import BaseModel
import uuid

class Panel(BaseModel):
    node_id: uuid.UUID
    label: str
    header: str
    order: int
    asset_id: uuid.UUID
    header_order: int

    class Config:
        orm_mode = True


