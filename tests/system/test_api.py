import os
import uuid
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.infrastructure.database.base import init_db

pytestmark = pytest.mark.system

def setup_module():
    # Asegurar BD creada
    assert os.getenv("DB_URL"), "DB_URL debe estar configurado para pruebas de sistema"
    init_db()

def test_full_flow():
    client = TestClient(app)

    # Crear evento
    r = client.post("/events", json={"name": "Summit", "description": "Tech", "capacity": 2})
    assert r.status_code == 201, r.text
    event_id = r.json()["id"]

    # Sufijo único para evitar duplicados entre corridas
    suf = uuid.uuid4().hex[:6]

    # Crear participantes con emails únicos por corrida
    p1 = client.post("/participants", json={"name": "Ana", "email": f"ana2_{suf}@example.com"})
    p2 = client.post("/participants", json={"name": "Bob", "email": f"bob2_{suf}@example.com"})
    assert p1.status_code == 201, p1.text
    assert p2.status_code == 201, p2.text
    pid1 = p1.json()["id"]
    pid2 = p2.json()["id"]

    # Registrar asistencia
    r1 = client.post("/attendance/register", json={"event_id": event_id, "participant_id": pid1})
    assert r1.status_code == 200, r1.text
    r2 = client.post("/attendance/register", json={"event_id": event_id, "participant_id": pid2})
    assert r2.status_code == 200, r2.text

    # No debe permitir sobrecupo (o duplicado)
    r3 = client.post("/attendance/register", json={"event_id": event_id, "participant_id": pid2})
    assert r3.status_code in (400, 409)

    # Stats con caché
    s = client.get(f"/attendance/events/{event_id}/stats")
    assert s.status_code == 200, s.text
    data = s.json()
    assert data["registered"] == 2
    assert data["capacity"] == 2
    assert data["available"] == 0
    assert data["occupancy_percent"] == 100.0