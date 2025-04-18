import logging
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, get_db, Base
from app.routes.api import router as api_router
from app.services.data_importer import import_f1_data
from sqlalchemy.orm import Session
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="PushPush API",
    description="API for Formula 1 statistics",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Add logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/")
def read_root():
    return {
        "message": "Welcome to PushPush API!",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/api/import-data/{season}")
async def trigger_data_import(
    season: int, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if season < 1950 or season > datetime.now().year:
        raise HTTPException(status_code=400, detail="Season must be between 1950 and 2025")
    
    # Run import in background to avoid timeout
    background_tasks.add_task(import_f1_data, season, db)
    return {"message": f"Data import for {season} season started in background"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)