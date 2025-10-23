#!/bin/sh
set -e

echo "Entorno actual: $ENVIRONMENT"

if [ "$ENVIRONMENT" = "production" ]; then
  echo "Producción detectada: aplicando migraciones en Supabase..."
  alembic upgrade head
else
  echo 'Esperando a que PostgreSQL esté listo...'
  sleep 5

  echo 'Aplicando migraciones de Alembic...'
  alembic upgrade head

  echo 'Verificando si necesitamos poblar la base de datos...'
  TABLE_EXISTS=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -tAc \
  "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'persona');")

  if [ "$TABLE_EXISTS" = "t" ]; then
      HAS_DATA=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -tAc "SELECT COUNT(*) FROM persona;")
      if [ "$HAS_DATA" -gt 0 ]; then
          echo "✅ Base de datos ya tiene datos, omitiendo seed..."
      else
          echo "⚠️ Tabla 'persona' vacía, ejecutando seed.sql..."
          PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -f /app/seed.sql
      fi
  else
      echo "⚠️ Tabla 'persona' no existe, ejecutando seed.sql..."
      PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -f /app/seed.sql
  fi
fi
echo 'Iniciando servidor FastAPI...'
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
