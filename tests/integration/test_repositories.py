import os
import pytest
from sqlalchemy.orm import Session
from src.infrastructure.database.base import get_session_factory, init_db
from src.infrastructure.repositories.event_repository_impl import SQLEventRepository
from src.infrastructure.repositories.participant_repository_impl import SQLParticipantRepository
from src.infrastructure.repositories.attendance_repository_impl import SQLAttendanceRepository

pytestmark = pytest.mark.integration

def require_db():
    url = os.getenv("DB_URL")
    assert url and url.startswith("mysql+pymysql://"), "DB_URL debe apuntar a MySQL"
    init_db()

def test_event_repo_crud():
    require_db()
    SessionLocal = get_session_factory()
    with SessionLocal() as db:
        repo = SQLEventRepository(db)
        e = repo.create("Evento", "Desc", 10)
        assert e.id
        got = repo.get(e.id)
        assert got and got.name == "Evento"
        all_ = repo.list()
        assert len(all_) >= 1
        upd = repo.update(e.id, "Nuevo", "Desc2", 15)
        assert upd and upd.name == "Nuevo" and upd.capacity == 15
        assert repo.delete(e.id) is True
        assert repo.get(e.id) is None

def test_attendance_repo_counts():
    require_db()
    SessionLocal = get_session_factory()
    with SessionLocal() as db:
        erepo = SQLEventRepository(db)
        prepo = SQLParticipantRepository(db)
        arepo = SQLAttendanceRepository(db)
        e = erepo.create("Cap", None, 2)
        p1 = prepo.create("A", "a1@example.com")
        p2 = prepo.create("B", "b1@example.com")
        assert arepo.count_attendees(e.id) == 0
        arepo.register(e.id, p1.id)
        arepo.register(e.id, p2.id)
        assert arepo.count_attendees(e.id) == 2