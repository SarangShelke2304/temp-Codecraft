import uvicorn
from fastapi import FastAPI
from app.api.endpoints import workflows
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

origins = [
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allowed origins
    allow_credentials=True,           # Allow cookies, authorization headers, etc.
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)

app.include_router(workflows.router, prefix="/workflows")

@app.get("/")
async def root():
    return {"message": "Welcome to CodeCraft API"}

if __name__ == "__main__":
    # Script to run in develop mode
    uvicorn_args = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True
    }

    uvicorn.run(**uvicorn_args)
