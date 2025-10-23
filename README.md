# 🇵🇪 Vota Bien Peru - Backend API

API REST para consultar información política del Perú: candidatos, legisladores, partidos políticos, proyectos de ley y más.

## 📋 Requisitos Previos

- Docker Desktop (Windows/Mac) o Docker Engine + Docker Compose (Linux)
- Git

## 🚀 Inicio Rápido con Docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/antguivy/votabien-peru-backend.git
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

### 3. Levantar los servicios

```bash
# Construir e iniciar todos los contenedores
docker-compose up --build
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
- 10 personas políticas conocidas
- 3 legisladores activos
- 8 candidaturas
- 3 proyectos de ley
- 8 registros de asistencia
- 2 denuncias


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

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request




**¿Problemas?** Abre un [issue](https://github.com/tu-usuario/votabien-peru-backend/issues)