"""
Módulo de configuración y gestión de base de datos.
Proporciona conexión singleton y dependency injection para FastAPI.
"""

import logging
from contextlib import contextmanager
from typing import Callable, Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlmodel import Session

from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

Base = declarative_base()


class DatabaseManager:
    """
    Gestor singleton para la conexión a base de datos.
    Maneja el ciclo de vida del engine y la factory de sesiones.
    """

    def __init__(self) -> None:
        self._engine: Engine | None = None
        self._session_factory: Callable[[], Session] | None = None

    @property
    def engine(self) -> Engine:
        """Retorna el engine de SQLAlchemy."""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._engine

    @property
    def session_factory(self) -> Callable[[], Session]:
        """Retorna la factory de sesiones."""
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._session_factory

    def initialize(self) -> None:
        """
        Inicializa la conexión a la base de datos.
        Debe llamarse al iniciar la aplicación (lifespan startup).
        """
        logger.info("Initializing database connection...")

        self._engine = create_engine(
            settings.DATABASE_URI,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=20,
            max_overflow=0,
            echo=False,
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            class_=Session,
        )

        self._verify_connection()
        logger.info("✓ Database connection established successfully.")

    def _verify_connection(self) -> None:
        """Verifica que la conexión a la base de datos funcione."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except Exception as e:
            logger.error("✗ Database connection failed: %s", e)
            raise

    def close(self) -> None:
        """
        Cierra la conexión a la base de datos.
        Debe llamarse al cerrar la aplicación (lifespan shutdown).
        """
        if self._engine:
            logger.info("Closing database connection...")
            self._engine.dispose()
            self._engine = None
            self._session_factory = None
            logger.info("✓ Database connection closed.")

    @contextmanager
    def get_session_context(self) -> Generator[Session, None, None]:
        """
        Context manager para obtener una sesión de base de datos.
        Uso:
            with db_manager.get_session_context() as session:
                # usar session
        """
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# Instancia global del gestor de base de datos
db_manager = DatabaseManager()


# Funciones de conveniencia para FastAPI lifespan
def init_db() -> None:
    """Inicializa la base de datos (para usar en lifespan startup)."""
    db_manager.initialize()


def close_db() -> None:
    """Cierra la base de datos (para usar en lifespan shutdown)."""
    db_manager.close()


# Dependency para FastAPI
def get_session() -> Generator[Session, None, None]:
    """
    Dependency de FastAPI para obtener una sesión de base de datos.

    Uso en endpoints:
        @app.get("/users")
        def get_users(db: Session = Depends(get_session)):
            return db.query(User).all()
    """
    session = db_manager.session_factory()
    try:
        yield session
    finally:
        session.close()
