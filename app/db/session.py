from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db.base import Base
from app.core.config import settings
from app.models.frontend_models import _Components, _PropertyTypes,_Assets, _Configs

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)