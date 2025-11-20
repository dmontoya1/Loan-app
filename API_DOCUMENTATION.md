# Documentación de la API REST

## Base URL
```
http://localhost:8001/api
```

## Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación. Incluye el token en el header:

```
Authorization: Bearer <access_token>
```

### Endpoints de Autenticación

#### POST /api/auth/login/
Login de usuario.

**Request Body:**
```json
{
  "username": "usuario@ejemplo.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "refresh": "refresh_token",
  "access": "access_token",
  "user": {
    "id": 1,
    "username": "usuario@ejemplo.com",
    "email": "usuario@ejemplo.com",
    "first_name": "Nombre",
    "last_name": "Apellido",
    "phone": "+1234567890",
    "tenant": 1,
    "tenant_name": "Mi Empresa",
    "is_tenant_admin": true,
    "date_joined": "2025-01-01T00:00:00Z"
  }
}
```

#### POST /api/auth/register/
Registro de nuevo tenant y usuario admin.

**Request Body:**
```json
{
  "name": "Mi Empresa",
  "email": "empresa@ejemplo.com",
  "phone": "+1234567890",
  "address": "Dirección",
  "password": "password123"
}
```

#### GET /api/auth/me/
Obtener información del usuario actual.

**Headers:**
```
Authorization: Bearer <access_token>
```

## Usuarios

### GET /api/users/profiles/
Listar perfiles de usuarios.

**Query Parameters:**
- `search`: Búsqueda por nombre, email, documento, teléfono
- `ordering`: Ordenar por `created_at`, `first_name`, `last_name`
- `is_active`: Filtrar por activo

### POST /api/users/profiles/
Crear nuevo perfil de usuario.

**Request Body:**
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan@ejemplo.com",
  "phone": "+1234567890",
  "document_type": "CEDULA",
  "document_number": "1234567890",
  "address": "Dirección",
  "codeudor": null
}
```

### GET /api/users/profiles/{id}/
Obtener detalle de un usuario.

### PUT /api/users/profiles/{id}/
Actualizar usuario.

### DELETE /api/users/profiles/{id}/
Eliminar usuario.

### GET /api/users/profiles/{id}/loans/
Obtener préstamos de un usuario.

## Préstamos

### GET /api/loans/loans/
Listar préstamos.

**Query Parameters:**
- `search`: Búsqueda por nombre, documento, email del usuario
- `status`: Filtrar por estado (ACTIVO, COMPLETADO, CANCELADO, VENCIDO)
- `payment_frequency`: Filtrar por frecuencia (SEMANAL, QUINCENAL, MENSUAL)
- `amount_min`: Monto mínimo
- `amount_max`: Monto máximo
- `date_from`: Fecha desde
- `date_to`: Fecha hasta
- `ordering`: Ordenar por `created_at`, `amount`, `start_date`

### POST /api/loans/loans/
Crear nuevo préstamo.

**Request Body:**
```json
{
  "user_profile": 1,
  "amount": 10000.00,
  "interest_rate": 5.5,
  "payment_frequency": "MENSUAL",
  "total_payments": 12,
  "start_date": "2025-01-01",
  "notes": "Notas opcionales",
  "template": null
}
```

### GET /api/loans/loans/{id}/
Obtener detalle de un préstamo (incluye pagos).

### PUT /api/loans/loans/{id}/
Actualizar préstamo.

### DELETE /api/loans/loans/{id}/
Eliminar préstamo.

### POST /api/loans/loans/{id}/import_loan/
Importar préstamo con pagos ya completados.

**Request Body:**
```json
{
  "payments_completed": 3,
  "last_payment_date": "2025-01-15"
}
```

### GET /api/loans/loans/{id}/payments/
Obtener pagos de un préstamo.

### Plantillas de Préstamos

### GET /api/loans/templates/
Listar plantillas.

### POST /api/loans/templates/
Crear plantilla.

**Request Body:**
```json
{
  "name": "Préstamo Mensual 12 Cuotas",
  "amount": 10000.00,
  "interest_rate": 5.5,
  "payment_frequency": "MENSUAL",
  "total_payments": 12,
  "notes": "Plantilla para préstamos mensuales",
  "is_active": true
}
```

## Pagos

### GET /api/payments/payments/
Listar pagos.

**Query Parameters:**
- `status`: Filtrar por estado
- `loan`: Filtrar por préstamo
- `overdue`: true/false para pagos vencidos
- `ordering`: Ordenar por `due_date`, `payment_date`, `payment_number`

### POST /api/payments/payments/{id}/process/
Procesar un pago (marcarlo como completado).

**Request Body:**
```json
{
  "payment_date": "2025-01-15",
  "notes": "Pago recibido"
}
```

### GET /api/payments/payments/overdue/
Obtener pagos vencidos.

### GET /api/payments/payments/upcoming/
Obtener pagos próximos a vencer (próximos 7 días).

## Reportes

### GET /api/reports/dashboard/
Obtener estadísticas del dashboard.

**Response:**
```json
{
  "total_loans": 50,
  "active_loans": 30,
  "completed_loans": 15,
  "overdue_loans": 5,
  "total_lent": 500000.00,
  "total_paid": 250000.00,
  "total_pending": 250000.00,
  "total_users": 25,
  "pending_payments": 100,
  "overdue_payments": 10,
  "completed_payments": 200,
  "loans_by_status": {
    "ACTIVO": 30,
    "COMPLETADO": 15,
    "CANCELADO": 0,
    "VENCIDO": 5
  },
  "payments_by_month": [...]
}
```

### GET /api/reports/loans/
Reporte de préstamos.

**Query Parameters:**
- `start_date`: Fecha inicio
- `end_date`: Fecha fin

### GET /api/reports/payments/
Reporte de pagos.

**Query Parameters:**
- `start_date`: Fecha inicio
- `end_date`: Fecha fin

