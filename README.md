# 🇵🇪 Vota Bien Peru - Backend API

API REST para consultar información política del Perú: candidatos, legisladores, partidos políticos, proyectos de ley y más.

## 📋 Requisitos Previos

- Docker Desktop (Windows/Mac) o Docker Engine + Docker Compose (Linux)
- Git

## 🚀 Inicio Rápido con Docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/votabien-peru-backend.git
cd votabien-peru-backend
```

### 2. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y cambiar al menos estas variables:
# - JWT_SECRET_KEY (genera uno seguro con: openssl rand -hex 32)
```

**Importante**: El archivo `.env` ya está configurado para funcionar con Docker. Solo necesitas cambiar el `JWT_SECRET_KEY` por seguridad.

### 3. Generar un JWT_SECRET_KEY seguro

```bash
# En Linux/Mac
openssl rand -hex 32

# O con Python
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copia el resultado y reemplaza el valor de `JWT_SECRET_KEY` en tu archivo `.env`.

### 4. Levantar los servicios

```bash
# Construir e iniciar todos los contenedores
docker-compose up --build

# O en modo detached (segundo plano)
docker-compose up -d --build
```

Esto hará automáticamente:
- ✅ Levantar PostgreSQL
- ✅ Crear la base de datos `politics_db`
- ✅ Cargar datos de ejemplo (seed.sql)
- ✅ Aplicar migraciones de Alembic
- ✅ Iniciar el servidor FastAPI
- ✅ Iniciar Adminer (UI para la base de datos)

### 5. Verificar que todo funciona

Abre tu navegador y visita:

- **API**: http://localhost:8000
- **Documentación interactiva (Swagger)**: http://localhost:8000/docs
- **Adminer (DB Manager)**: http://localhost:8080
  - Sistema: `PostgreSQL`
  - Servidor: `db`
  - Usuario: `politics_user`
  - Contraseña: `politics_pass_dev`
  - Base de datos: `politics_db`

## 📊 Datos de Ejemplo

El proyecto incluye datos de ejemplo basados en el contexto político peruano real:

- 5 partidos políticos (Fuerza Popular, Perú Libre, Acción Popular, APP, Renovación Popular)
- 8 distritos electorales
- 6 personas políticas conocidas
- 3 legisladores activos
- 4 candidaturas (Elecciones 2021)
- 3 proyectos de ley
- 8 registros de asistencia
- 2 denuncias

## 🛠️ Comandos Útiles

### Ver logs de los servicios

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver solo logs de la API
docker-compose logs -f api

# Ver solo logs de la base de datos
docker-compose logs -f db
```

### Detener los servicios

```bash
# Detener contenedores (mantiene los datos)
docker-compose stop

# Detener y eliminar contenedores (mantiene los datos en volúmenes)
docker-compose down

# Detener, eliminar contenedores Y volúmenes (elimina TODOS los datos)
docker-compose down -v
```

### Reiniciar servicios

```bash
# Reiniciar todos
docker-compose restart

# Reiniciar solo la API
docker-compose restart api
```

### Ejecutar comandos dentro de los contenedores

```bash
# Acceder a shell de la API
docker-compose exec api bash

# Ejecutar migraciones manualmente
docker-compose exec api alembic upgrade head

# Crear una nueva migración
docker-compose exec api alembic revision --autogenerate -m "descripcion"

# Acceder a PostgreSQL
docker-compose exec db psql -U politics_user -d politics_db
```

### Ver base de datos desde terminal

```bash
# Conectarse a PostgreSQL
docker-compose exec db psql -U politics_user -d politics_db

# Dentro de psql, puedes ejecutar:
\dt                          # Listar tablas
\d persona                   # Ver estructura de tabla 'persona'
SELECT * FROM persona;       # Consultar datos
\q                          # Salir
```

## 🔄 Recargar datos de prueba

Si quieres volver a cargar los datos de ejemplo desde cero:

```bash
# 1. Detener y eliminar contenedores y volúmenes
docker-compose down -v

# 2. Volver a levantar (recargará seed.sql automáticamente)
docker-compose up -d --build
```

## 🏗️ Estructura del Proyecto

```
.
├── app/
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── models/              # Modelos SQLModel
│   │   ├── auth.py
│   │   └── politics.py
│   ├── routers/             # Endpoints de la API
│   ├── core/                # Configuración y seguridad
│   │   └── settings.py
│   └── utils/               # Utilidades
├── alembic/                 # Migraciones de base de datos
│   └── versions/
├── database/
│   └── seed.sql            # Datos de ejemplo
├── docker-compose.yml       # Configuración de servicios
├── Dockerfile              # Imagen de la API
├── alembic.ini             # Configuración de Alembic
├── .env                    # Variables de entorno (no versionar)
├── .env.example            # Ejemplo de variables de entorno
└── README.md               # Este archivo
```

## 🧪 Desarrollo

### Hot Reload

El código se monta como volumen, por lo que los cambios se reflejan automáticamente sin reiniciar:

```bash
# Edita cualquier archivo en app/
# El servidor se recargará automáticamente
```

### Crear nuevas migraciones

```bash
# 1. Modifica tus modelos en app/models/

# 2. Genera la migración
docker-compose exec api alembic revision --autogenerate -m "agregar campo x a tabla y"

# 3. Revisa el archivo generado en alembic/versions/

# 4. Aplica la migración
docker-compose exec api alembic upgrade head
```

## 🐛 Solución de Problemas

### Error: "port is already allocated"

Otro servicio está usando el puerto 5432, 8000 u 8080. Opciones:

```bash
# Opción 1: Detener el servicio conflictivo
# En Windows: busca "Servicios" y detén PostgreSQL
# En Linux/Mac: sudo systemctl stop postgresql

# Opción 2: Cambiar puertos en docker-compose.yml
# db:
#   ports:
#     - "5433:5432"  # Cambiar primer número
```

### Error: "no such file or directory: .env"

```bash
# Crear archivo .env desde el ejemplo
cp .env.example .env
```

### La base de datos no tiene datos

```bash
# Recargar datos
docker-compose down -v
docker-compose up -d --build
```

### Error de migraciones de Alembic

```bash
# Ver estado de migraciones
docker-compose exec api alembic current

# Ver historial
docker-compose exec api alembic history

# Aplicar todas las migraciones pendientes
docker-compose exec api alembic upgrade head

# Volver a una migración específica
docker-compose exec api alembic downgrade <revision_id>
```

### Contenedor API no inicia

```bash
# Ver logs detallados
docker-compose logs api

# Reconstruir la imagen desde cero
docker-compose build --no-cache api
docker-compose up -d
```

## 📝 Variables de Entorno

| Variable | Descripción | Requerido | Default |
|----------|-------------|-----------|---------|
| `DATABASE_URI` | Conexión a PostgreSQL | ✅ | - |
| `JWT_SECRET_KEY` | Clave secreta para JWT | ✅ | - |
| `APP_NAME` | Nombre de la aplicación | ❌ | "Backend" |
| `ENVIRONMENT` | Entorno (development/staging/production) | ❌ | development |
| `DEBUG` | Modo debug | ❌ | False |
| `FRONTEND_HOST` | URL del frontend | ❌ | http://localhost:3000 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración token acceso | ❌ | 15 |
| `REFRESH_TOKEN_EXPIRE_MINUTES` | Duración token refresh | ❌ | 10080 |
| `RESEND_API_KEY` | API key de Resend | ❌ | - |
| `EMAIL_FROM` | Email remitente | ❌ | auto-generado |

## 🌐 Endpoints Principales

Una vez levantado el proyecto, puedes probar estos endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Listar partidos políticos
curl http://localhost:8000/api/v1/partidos

# Listar legisladores activos
curl http://localhost:8000/api/v1/legisladores

# Ver documentación completa
# http://localhost:8000/docs
```

## 📦 Producción

Para desplegar en producción:

1. **Cambia las variables de entorno**:
   - `ENVIRONMENT=production`
   - `DEBUG=False`
   - `JWT_SECRET_KEY` con un secret fuerte (64+ caracteres)
   - `DATABASE_URI` con tu base de datos de producción

2. **Usa un servicio de PostgreSQL gestionado**:
   - AWS RDS
   - Google Cloud SQL
   - Supabase
   - Railway
   - Render

3. **Despliega la API**:
   - Railway (recomendado para empezar)
   - Render
   - AWS ECS/Fargate
   - Google Cloud Run
   - DigitalOcean App Platform

4. **No uses `docker-compose` en producción directamente**. Usa orquestadores como:
   - Kubernetes
   - Docker Swarm
   - O servicios gestionados (Railway, Render, etc.)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- Tu Nombre - [@tu_usuario](https://github.com/tu_usuario)

## 🙏 Agradecimientos

- Datos basados en información pública del Jurado Nacional de Elecciones (JNE)
- Congreso de la República del Perú

---

**¿Problemas?** Abre un [issue](https://github.com/tu-usuario/votabien-peru-backend/issues)