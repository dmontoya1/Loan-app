# Sistema de Préstamos

Sistema completo de gestión de préstamos construido con Django, PostgreSQL (Supabase) y Tailwind CSS.

## Características

- ✅ **Multi-tenancy**: Soporte para múltiples empresas/usuarios
- ✅ **Gestión de Usuarios**: Registro y gestión de clientes
- ✅ **Gestión de Préstamos**: Crear préstamos con tasas de interés personalizadas
- ✅ **Sistema de Pagos**: Pagos semanales, quincenales o mensuales
- ✅ **Reportes**: Dashboard con estadísticas y reportes detallados
- ✅ **Autenticación**: Sistema de login y registro
- ✅ **Diseño Moderno**: Interfaz construida con Tailwind CSS

## Tecnologías

- **Backend**: Django 5.2.7
- **Base de Datos**: PostgreSQL (Local por defecto, configurable para Supabase)
- **Frontend**: Tailwind CSS (via CDN)
- **Python**: 3.8+

## Estructura del Proyecto

```
Loan-app/
├── apps/
│   ├── authentication/    # Autenticación y multi-tenancy
│   ├── users/              # Gestión de usuarios/clientes
│   ├── loans/              # Gestión de préstamos
│   ├── payments/           # Gestión de pagos
│   └── reports/            # Reportes y estadísticas
├── loanapp/               # Configuración del proyecto
├── templates/             # Templates HTML
├── static/                # Archivos estáticos
└── manage.py
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd Loan-app
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL Local

#### Opción A: PostgreSQL Local (Recomendado para desarrollo)

1. Asegúrate de tener PostgreSQL instalado:
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # Windows
   # Descarga desde https://www.postgresql.org/download/windows/
   ```

2. Crea la base de datos:
   ```bash
   # Accede a PostgreSQL
   psql postgres
   
   # Crea la base de datos
   CREATE DATABASE loan_app;
   
   # Crea un usuario (opcional, puedes usar el usuario 'postgres')
   CREATE USER loanapp_user WITH PASSWORD 'tu_password';
   ALTER DATABASE loan_app OWNER TO loanapp_user;
   ```

3. Crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:
   ```env
   SECRET_KEY=tu-secret-key-aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # PostgreSQL Local
   DB_NAME=loanapp
   DB_USER=postgres
   DB_PASSWORD=tu_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

#### Opción B: Usar Supabase (Para producción o cloud)

1. Crea un proyecto en [Supabase](https://supabase.com)
2. Ve a Settings > Database y obtén las credenciales
3. Actualiza el archivo `.env`:
   ```env
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=tu-supabase-password
   DB_HOST=db.tu-proyecto.supabase.co
   DB_PORT=5432
   ```

### 5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en `http://localhost:8000`

## Instalación con Docker (Recomendado)

### Prerrequisitos

- [Docker](https://www.docker.com/get-started) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

### Pasos de instalación con Docker

1. **Crear archivo `.env`**:
   ```env
   SECRET_KEY=tu-secret-key-aqui-muy-seguro
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # PostgreSQL (configurado automáticamente en Docker)
   DB_NAME=loanapp
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   DB_EXTERNAL_PORT=5433
   WEB_EXTERNAL_PORT=8001
   ```
   
   **Nota**: 
   - `DB_EXTERNAL_PORT=5433` se usa para evitar conflictos si tienes PostgreSQL local en el puerto 5432
   - `WEB_EXTERNAL_PORT=8001` se usa para evitar conflictos si tienes Django local corriendo en el puerto 8000
   - Los contenedores usan los puertos 5432 y 8000 internamente, pero se mapean a 5433 y 8001 en tu máquina

2. **Construir y ejecutar los contenedores**:
   ```bash
   # Para desarrollo
   docker-compose -f docker-compose.dev.yml up --build
   
   # Para producción
   docker-compose up --build
   ```

3. **Crear superusuario** (en otra terminal):
   ```bash
   # Para desarrollo
   docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
   
   # Para producción
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Acceder a la aplicación**:
   - La aplicación estará disponible en `http://localhost:8001` (o el puerto que hayas configurado en `WEB_EXTERNAL_PORT`)
   - La base de datos PostgreSQL estará disponible en `localhost:5433` (o el puerto que hayas configurado en `DB_EXTERNAL_PORT`)

### Comandos útiles de Docker

```bash
# Detener los contenedores (desarrollo)
docker-compose -f docker-compose.dev.yml down

# Detener y eliminar volúmenes (CUIDADO: elimina datos)
docker-compose -f docker-compose.dev.yml down -v

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f web

# Ejecutar comandos en el contenedor
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Entrar al shell del contenedor
docker-compose -f docker-compose.dev.yml exec web bash

# Reconstruir contenedores después de cambios
docker-compose -f docker-compose.dev.yml up --build
```

**Nota**: Todos los comandos usan `docker-compose.dev.yml` para desarrollo. Para producción, usa `docker-compose.yml`.

### Modo Desarrollo vs Producción

- **Desarrollo**: Usa `docker-compose.dev.yml` con hot-reload y herramientas de debug
- **Producción**: Usa `docker-compose.yml` con Gunicorn y optimizaciones

## Uso

### Registro de Empresa (Tenant)

1. Ve a `/register/tenant/`
2. Completa el formulario con la información de tu empresa
3. Se creará automáticamente un usuario administrador

### Iniciar Sesión

1. Ve a `/login/`
2. Ingresa tus credenciales
3. Serás redirigido al dashboard

### Crear un Usuario

1. Ve a **Usuarios** > **Nuevo Usuario**
2. Completa la información del cliente
3. Guarda el registro

### Crear un Préstamo

1. Ve a **Préstamos** > **Nuevo Préstamo**
2. Selecciona el usuario
3. Configura:
   - Monto del préstamo
   - Tasa de interés (%)
   - Frecuencia de pago (Semanal, Quincenal, Mensual)
   - Número de pagos
   - Fecha de inicio
4. El sistema creará automáticamente todos los pagos

### Procesar Pagos

1. Ve a **Pagos**
2. Busca el pago a procesar
3. Haz clic en **Procesar**
4. Actualiza el estado a "Completado"
5. El sistema actualizará automáticamente el estado del préstamo

## Principios SOLID y Patrones de Diseño

Este proyecto implementa:

- **Service Layer Pattern**: Servicios separados para lógica de negocio
- **Factory Pattern**: Creación de pagos automáticos
- **Repository Pattern**: Abstracción de acceso a datos
- **Mixin Pattern**: Reutilización de código en vistas
- **Decorator Pattern**: Validación de permisos y tenant
- **DRY (Don't Repeat Yourself)**: Código reutilizable y modular
- **Single Responsibility**: Cada clase tiene una responsabilidad única
- **Dependency Inversion**: Uso de interfaces y abstracciones

## Apps del Proyecto

### `authentication`
- Modelos: `Tenant`, `CustomUser`
- Funcionalidades: Login, registro, multi-tenancy

### `users`
- Modelos: `UserProfile`
- Funcionalidades: CRUD de usuarios/clientes

### `loans`
- Modelos: `Loan`
- Funcionalidades: CRUD de préstamos, cálculo automático de pagos

### `payments`
- Modelos: `Payment`
- Funcionalidades: Gestión de pagos, procesamiento automático

### `reports`
- Funcionalidades: Dashboard, reportes de préstamos y pagos

## Mejoras Futuras

- [ ] Integración con Supabase Auth para autenticación mejorada
- [ ] Notificaciones por email
- [ ] Exportar reportes a PDF/Excel
- [ ] API REST para integraciones
- [ ] Dashboard con gráficos interactivos
- [ ] App móvil

## Licencia

Este proyecto es privado y propietario.

## Soporte

Para soporte, contacta al equipo de desarrollo.
