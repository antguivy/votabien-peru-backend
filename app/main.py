import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.database import close_db, init_db
from app.config.logging_config import setup_logging
from app.config.settings import get_settings
from app.routes.api import api_router_v1

settings = get_settings()
setup_logging(debug=settings.DEBUG, environment=settings.ENVIRONMENT)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación.
    Inicializa recursos al arrancar y los cierra al apagar.
    """

    # ====== Startup ======
    logger.info("=" * 60)
    logger.info("🚀 Starting %s", settings.APP_NAME)
    logger.info("📝 Environment: %s", settings.ENVIRONMENT)
    logger.info("🐛 Debug mode: %s", settings.DEBUG)
    logger.info("=" * 60)

    try:
        init_db()
        # await init_embeddings()
        # await init_vector_store()
        # logger.info("=" * 60)
        # logger.info("✅ All systems initialized successfully!")
        # logger.info(f"📚 Docs available at: http://localhost:8000/docs")
        # logger.info("=" * 60)
    except (RuntimeError, ConnectionError, TimeoutError) as e:
        logger.error("Application startup failed due to runtime error: %s", e)
        raise
    except Exception as e:
        logger.error("Application startup failed due to unexpected error: %s", e)
        raise
    yield

    # ====== Shutdown ======
    logger.info("=" * 60)
    logger.info("Shutting down %s", settings.APP_NAME)
    logger.info("=" * 60)

    try:
        close_db()
        logger.info("✅ Cleanup completed successfully")
    except (RuntimeError, ConnectionError, TimeoutError) as e:
        logger.error("⚠️ Error during shutdown: %s", e)

    logger.info("=" * 60)
    logger.info("🛑 Application stopped")
    logger.info("=" * 60)


app = FastAPI(
    title=settings.APP_NAME, lifespan=lifespan, debug=settings.DEBUG, version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# 🔒 Root endpoint seguro
@app.get("/")
async def root():
    return {"message": "Marketing Intelligence Backend is running."}


@app.get("/health")
async def health_check():
    """
    Health check endpoint para verificar el estado de la aplicación.
    Usado por Docker, Kubernetes, load balancers, etc.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


# 🔒 Exception handler global
@app.exception_handler(Exception)
async def global_exception_handler(_request, exc):
    # Development
    if settings.DEBUG:
        return JSONResponse(
            status_code=500, content={"error": str(exc), "type": type(exc).__name__}
        )
    # Porduction
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


app.include_router(api_router_v1)
