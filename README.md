# Eventia Core API

Backend para gestión de eventos, participantes y asistencia con FastAPI, MySQL y caché (Redis). Incluye pruebas (unitarias, integración, sistema) y CI con GitHub Actions.

## Arquitectura (Clean Architecture)
```
src/
  domain/
    entities/
    interfaces/
    services/
  infrastructure/
    database/
      models/
    repositories/
    cache/
    config/
  application/
    dtos/
    controllers/
    routes/
  api/
tests/
  unit/
  integration/
  system/
```

## Tecnologías
- Python 3.11+
- FastAPI, Uvicorn
- SQLAlchemy + PyMySQL (MySQL/MariaDB)
- Redis (opcional local; requerido en CI, con fallback en memoria)
- PyTest (unit, integration, system)
- Bandit (análisis estático)
- GitHub Actions (CI)

## Requisitos
- Python 3.11+
- XAMPP (MySQL/phpMyAdmin) o MySQL local
- Opcional: Redis local
- pip

## Instalación (Windows + PowerShell + XAMPP)
```powershell
# Clona o descarga el proyecto, luego:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Edita `.env` y ajusta tu conexión (root sin contraseña en XAMPP):
```
APP_ENV=dev
DB_URL=mysql+pymysql://root@127.0.0.1:3306/eventia
REDIS_URL=
CACHE_TTL_SECONDS=60
```

Crea la base `eventia` en phpMyAdmin:
- Nueva → Nombre: eventia (sin espacios) → utf8mb4_unicode_ci → Crear
- Las tablas se crean automáticamente al iniciar la API (init_db()).

## Ejecutar en local
```powershell
uvicorn src.api.main:app --reload
```
- Health: http://127.0.0.1:8000/health
- Docs: http://127.0.0.1:8000/docs

## Pruebas
Usa una base separada para pruebas de sistema: `eventia_test`.

1) Crea `eventia_test` en phpMyAdmin (utf8mb4_unicode_ci).
2) En PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
# Unitarias
python -m pytest -q -m unit

# Integración (usa DB_URL de .env -> apunta a eventia)
python -m pytest -q -m integration

# Sistema/E2E (usa BD de pruebas)
$env:DB_URL = "mysql+pymysql://root@127.0.0.1:3306/eventia_test"
python -m pytest -q -m system
```

## Análisis estático (Bandit)
```powershell
bandit -r src -q
```

## CI con GitHub Actions
El workflow:
1. Instala dependencias
2. Levanta MySQL y Redis como servicios
3. Ejecuta pruebas unitarias, integración y sistema
4. Ejecuta Bandit
5. Imprime “OK” si todo pasa

Variables de entorno del job:
- `DB_URL`: mysql+pymysql://test:testpass@127.0.0.1:3306/eventia_test
- `REDIS_URL`: redis://127.0.0.1:6379/0
- `PYTHONPATH`: src

## Docker (opcional, +0.5)
Requiere Docker Desktop.
```bash
docker compose up -d --build
# API: http://127.0.0.1:8000/health y /docs
docker compose down -v
```

## Justificación de tecnologías
- FastAPI: rendimiento, tipado, OpenAPI.
- SQLAlchemy: ORM maduro, compatible con MySQL.
- Redis: mejora de rendimiento (caché de estadísticas), con fallback en memoria para desarrollo.
- PyTest: facilidad para unit, integration y system tests.
- Bandit: análisis estático de seguridad.
- GitHub Actions: CI integrado y reproducible.

## Troubleshooting
- “No module named 'src'” al correr pytest:
  - Ejecuta pytest desde la raíz del proyecto y/o define PYTHONPATH=src o usa `tests/conftest.py` (ya incluido).
- Error 400 al crear participantes en tests de sistema:
  - Usa la BD `eventia_test` o limpia tablas (TRUNCATE) o usa emails únicos (ver test actualizado).
- XAMPP MySQL sin contraseña:
  - Usa: `mysql+pymysql://root@127.0.0.1:3306/eventia` (sin `:password`).
