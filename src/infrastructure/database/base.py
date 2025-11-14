from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from src.infrastructure.config.settings import get_settings

Base = declarative_base()
_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(settings.db_url, pool_pre_ping=True, pool_recycle=3600)
    return _engine

def get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal

def init_db():
    # Importar modelos para que SQLAlchemy conozca las tablas
    from src.infrastructure.database.models.event_model import EventModel
    from src.infrastructure.database.models.participant_model import ParticipantModel
    from src.infrastructure.database.models.attendance_model import AttendanceModel
    Base.metadata.create_all(bind=get_engine())