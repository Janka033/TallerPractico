# Eventia Core API

Backend para gestionar eventos, participantes y asistencia.

## Requisitos
- Python 3.11+
- MySQL (por ejemplo XAMPP / MariaDB)
- (Opcional) Redis
- Pip

## Instalación
```bash
git clone https://github.com/Janka033/TallerPractico.git
cd TallerPractico
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux / Mac
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración (.env)
Crea `.env` (puedes copiar de `.env.example`):
```
APP_ENV=dev
DB_URL=mysql+pymysql://root@127.0.0.1:3306/eventia
REDIS_URL=
CACHE_TTL_SECONDS=60
```
Crear las bases `eventia` y (para pruebas) `eventia_test` en MySQL.

## Ejecutar API
```bash
uvicorn src.api.main:app --reload
```
Verificación:
- Health: http://127.0.0.1:8000/health
- Docs: http://127.0.0.1:8000/docs

## Pruebas
Usa una BD separada para pruebas de sistema (eventia_test).

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q -m unit
python -m pytest -q tests/integration
$env:DB_URL="mysql+pymysql://root@127.0.0.1:3306/eventia_test"
python -m pytest -q tests/system
```

Linux / Mac:
```bash
source .venv/bin/activate
python -m pytest -q -m unit
python -m pytest -q tests/integration
DB_URL="mysql+pymysql://root@127.0.0.1:3306/eventia_test" python -m pytest -q tests/system
```

## Limpieza rápida BD de pruebas (si repites tests)
```sql
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE attendance;
TRUNCATE TABLE participants;
TRUNCATE TABLE events;
SET FOREIGN_KEY_CHECKS=1;
```

## Caché
Si defines `REDIS_URL` (ej: `redis://127.0.0.1:6379/0`) se usa Redis; si no, caché en memoria.

## Comandos útiles

Entorno virtual (Windows):
.\.venv\Scripts\Activate.ps1

Entorno virtual (Linux / Mac):
source .venv/bin/activate

Instalar dependencias:
pip install -r requirements.txt

Levantar la API (modo desarrollo):
uvicorn src.api.main:app --reload

Pruebas unitarias:
python -m pytest -q -m unit

Pruebas de integración:
python -m pytest -q tests/integration

Pruebas de sistema (usar base eventia_test):
# Windows PowerShell
$env:DB_URL="mysql+pymysql://root@127.0.0.1:3306/eventia_test"
python -m pytest -q tests/system
# Linux / Mac
DB_URL="mysql+pymysql://root@127.0.0.1:3306/eventia_test" python -m pytest -q tests/system

Análisis estático (Bandit):
bandit -r src -q

Limpieza rápida de BD de pruebas (SQL):
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE attendance;
TRUNCATE TABLE participants;
TRUNCATE TABLE events;
SET FOREIGN_KEY_CHECKS=1;

## Estructura mínima
```
src/
  api/
  application/
  domain/
  infrastructure/
tests/
```

## Checklist rápido
- .env creado
- Dependencias instaladas
- BD `eventia` creada
- uvicorn levantado
- Tests pasan
