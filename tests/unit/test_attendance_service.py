import pytest
from src.domain.services.attendance_service import AttendanceService
from src.infrastructure.cache.cache_client import CacheClient
from src.domain.entities.event import Event
from src.domain.entities.participant import Participant

pytestmark = pytest.mark.unit

class FakeEventRepo:
    def __init__(self):
        self.events = {}
        self.next_id = 1
    def create(self, name, description, capacity):
        e = Event(id=self.next_id, name=name, description=description, capacity=capacity)
        self.events[self.next_id] = e
        self.next_id += 1
        return e
    def get(self, event_id):
        return self.events.get(event_id)
    def list(self): return list(self.events.values())
    def update(self, event_id, name, description, capacity):
        e = self.events.get(event_id)
        if not e: return None
        e.name, e.description, e.capacity = name, description, capacity
        return e
    def delete(self, event_id):
        return self.events.pop(event_id, None) is not None

class FakeParticipantRepo:
    def __init__(self):
        self.participants = {}
        self.next_id = 1
    def create(self, name, email):
        p = Participant(id=self.next_id, name=name, email=email)
        self.participants[self.next_id] = p
        self.next_id += 1
        return p
    def get(self, participant_id): return self.participants.get(participant_id)
    def get_by_email(self, email):
        for p in self.participants.values():
            if p.email == email: return p
        return None
    def list(self): return list(self.participants.values())
    def update(self, participant_id, name, email):
        p = self.participants.get(participant_id)
        if not p: return None
        p.name, p.email = name, email
        return p
    def delete(self, participant_id):
        return self.participants.pop(participant_id, None) is not None

class FakeAttendanceRepo:
    def __init__(self):
        self.rows = set()
    def is_registered(self, event_id, participant_id):
        return (event_id, participant_id) in self.rows
    def register(self, event_id, participant_id):
        self.rows.add((event_id, participant_id))
    def count_attendees(self, event_id):
        return sum(1 for e, _ in self.rows if e == event_id)

class DummyCache(CacheClient):
    def __init__(self):
        self._memory_cache = {}
        self._client = None
        self.ttl = 60

def test_register_ok():
    er, pr, ar = FakeEventRepo(), FakeParticipantRepo(), FakeAttendanceRepo()
    e = er.create("Conf", None, 2)
    p1 = pr.create("Ana", "ana@example.com")
    svc = AttendanceService(ar, er, pr, DummyCache())
    res = svc.register(e.id, p1.id)
    assert res["status"] == "registered"
    stats = svc.event_stats(e.id)
    assert stats["registered"] == 1
    assert stats["available"] == 1

def test_avoid_duplicate():
    er, pr, ar = FakeEventRepo(), FakeParticipantRepo(), FakeAttendanceRepo()
    e = er.create("Conf", None, 1)
    p1 = pr.create("Ana", "ana@example.com")
    svc = AttendanceService(ar, er, pr, DummyCache())
    svc.register(e.id, p1.id)
    with pytest.raises(ValueError):
        svc.register(e.id, p1.id)

def test_capacity_validation():
    er, pr, ar = FakeEventRepo(), FakeParticipantRepo(), FakeAttendanceRepo()
    e = er.create("Conf", None, 1)
    p1 = pr.create("Ana", "ana@example.com")
    p2 = pr.create("Bob", "bob@example.com")
    svc = AttendanceService(ar, er, pr, DummyCache())
    svc.register(e.id, p1.id)
    with pytest.raises(ValueError):
        svc.register(e.id, p2.id)