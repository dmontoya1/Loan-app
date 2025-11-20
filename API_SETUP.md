# Configuración de la API REST

## Instalación de Dependencias

Las dependencias ya están agregadas en `requirements.txt`. Para instalarlas en Docker:

```bash
make build
make up
```

O manualmente:

```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

## Endpoints Disponibles

### Autenticación
- `POST /api/auth/login/` - Login
- `POST /api/auth/register/` - Registro
- `GET /api/auth/me/` - Usuario actual

### Usuarios
- `GET /api/users/profiles/` - Listar usuarios
- `POST /api/users/profiles/` - Crear usuario
- `GET /api/users/profiles/{id}/` - Detalle de usuario
- `PUT /api/users/profiles/{id}/` - Actualizar usuario
- `DELETE /api/users/profiles/{id}/` - Eliminar usuario
- `GET /api/users/profiles/{id}/loans/` - Préstamos del usuario

### Préstamos
- `GET /api/loans/loans/` - Listar préstamos
- `POST /api/loans/loans/` - Crear préstamo
- `GET /api/loans/loans/{id}/` - Detalle de préstamo
- `PUT /api/loans/loans/{id}/` - Actualizar préstamo
- `DELETE /api/loans/loans/{id}/` - Eliminar préstamo
- `POST /api/loans/loans/{id}/import_loan/` - Importar préstamo
- `GET /api/loans/loans/{id}/payments/` - Pagos del préstamo

### Plantillas
- `GET /api/loans/templates/` - Listar plantillas
- `POST /api/loans/templates/` - Crear plantilla
- `GET /api/loans/templates/{id}/` - Detalle de plantilla
- `PUT /api/loans/templates/{id}/` - Actualizar plantilla
- `DELETE /api/loans/templates/{id}/` - Eliminar plantilla

### Pagos
- `GET /api/payments/payments/` - Listar pagos
- `GET /api/payments/payments/{id}/` - Detalle de pago
- `POST /api/payments/payments/{id}/process/` - Procesar pago
- `GET /api/payments/payments/overdue/` - Pagos vencidos
- `GET /api/payments/payments/upcoming/` - Pagos próximos

### Reportes
- `GET /api/reports/dashboard/` - Estadísticas del dashboard
- `GET /api/reports/loans/` - Reporte de préstamos
- `GET /api/reports/payments/` - Reporte de pagos

## Autenticación

La API utiliza JWT (JSON Web Tokens). Después de hacer login, incluye el token en el header:

```
Authorization: Bearer <access_token>
```

El access token expira en 24 horas. Usa el refresh token para obtener uno nuevo.

## CORS

La configuración de CORS permite conexiones desde:
- `http://localhost:3000`
- `http://localhost:19006` (Expo)
- `http://127.0.0.1:19006`

Para agregar más orígenes, edita `CORS_ALLOWED_ORIGINS` en `settings.py`.

## Pruebas

Puedes probar la API usando:

1. **Postman/Insomnia**: Importa los endpoints y prueba con tokens
2. **curl**: 
```bash
curl -X POST http://localhost:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario","password":"password"}'
```

3. **Desde la app móvil**: Configura la URL base en `src/utils/constants.ts`

## Notas

- Todos los endpoints requieren autenticación excepto `/api/auth/login/` y `/api/auth/register/`
- Los datos se filtran automáticamente por tenant del usuario autenticado
- La paginación está habilitada (20 items por página por defecto)

