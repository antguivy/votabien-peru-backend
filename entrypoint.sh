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
  COUNT=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -tAc \
  "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")

  if [ "$COUNT" -gt 0 ]; then
      echo "Las tablas ya existen, verificando si hay datos..."
      HAS_DATA=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -tAc \
      "SELECT COUNT(*) FROM persona")

      if [ "$HAS_DATA" -gt 0 ]; then
          echo "Base de datos ya tiene datos, omitiendo seed..."
      else
          echo "Poblando la base de datos..."
          PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -f /app/seed.sql
      fi
  else
      echo "Poblando la base de datos..."
      PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -f /app/seed.sql
  fi
fi

echo 'Iniciando servidor FastAPI...'
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
