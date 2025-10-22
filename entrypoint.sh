#!/bin/sh
set -e

echo "---------------------------------------"
echo "INICIANDO SCRIPT DE DEPURACIÓN..."
echo "---------------------------------------"

echo "Verificando variables clave:"
echo "ENVIRONMENT: [$ENVIRONMENT]"
echo "DATABASE_URI (primeros 20 chars): [${DATABASE_URI:0:20}]..."

echo "---------------------------------------"
echo "LISTA COMPLETA DE ENTORNO (printenv):"
printenv
echo "---------------------------------------"


echo "Entorno actual: $ENVIRONMENT"

# Chequeo de seguridad
if [ -z "$DATABASE_URI" ]; then
  echo "¡ERROR FATAL! DATABASE_URI está vacía o no definida."
  echo "El script se detendrá aquí."
  exit 1
fi

if [ "$ENVIRONMENT" = "production" ]; then
  echo "Producción detectada: aplicando migraciones en Supabase..."
  alembic upgrade head
else
  echo 'Esperando a que PostgreSQL esté listo...'
  sleep 5
  
  # ... (tu lógica 'else' para desarrollo) ...
  # Esta sección fallará de todos modos porque variables como
  # POSTGRES_PASSWORD no están definidas en tu .env
  
  echo 'Aplicando migraciones de Alembic...'
  alembic upgrade head
  
  # ... (resto de tu script 'else') ...
fi

echo 'Iniciando servidor FastAPI...'
exec uvicorn app.main:app --host 0.0.0.0 --port 8000