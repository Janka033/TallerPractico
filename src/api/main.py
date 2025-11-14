from fastapi import FastAPI
from src.infrastructure.database.base import init_db
from src.application.routes.event_routes import router as event_router
from src.application.routes.participant_routes import router as participant_router
from src.application.routes.attendance_routes import router as attendance_router

app = FastAPI(title="Eventia Core API")

# Inicializa tablas al iniciar
init_db()

# Rutas
app.include_router(event_router)
app.include_router(participant_router)
app.include_router(attendance_router)

@app.get("/health")
def health():
    return {"status": "ok"}



