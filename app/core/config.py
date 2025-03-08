from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_URL: str = "postgresql+asyncpg://lncn_user:Takemein121@axoma-dev-postgres.cr40weeiml48.ap-south-1.rds.amazonaws.com:5432/axoma-lcnc-manager"
settings = Settings()
