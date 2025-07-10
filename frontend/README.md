# Vision Singularity - Frontend

## Instalación y Configuración

### 1. Configurar el Backend

```bash
# Desde el directorio raíz del proyecto
cd vision-singularity

# Instalar dependencias
pip install -r visionsingularity/requirements.txt

# Configurar la base de datos
python manage.py makemigrations
python manage.py migrate

# Crear datos de ejemplo
python manage.py create_sample_data
```

### 2. Iniciar el Servidor

```bash
# Iniciar el servidor Django
python manage.py runserver

# El frontend estará disponible en:
# http://localhost:8000/
```

### 3. Iniciar Redis (para WebSockets)

```bash
# En una terminal separada
redis-server

# O usando Docker
docker run -d -p 6379:6379 redis:latest
```

## Características del Frontend

### 🎨 Diseño
- Replicación exacta del diseño de referencia
- Panel lateral con navegación
- Área principal responsiva
- Colores y espaciado idénticos a la imagen

### 📱 Secciones Disponibles

#### 1. **Dashboard**
- Estadísticas en tiempo real
- Gráfico de llamadas por hora
- Resumen de actividad

#### 2. **Mapa del Restaurante**
- Visualización de todas las mesas
- Estado en tiempo real (disponible/llamando)
- Interacción con mesas individuales

#### 3. **Notificaciones**
- Lista de todas las llamadas de servicio
- Filtros por estado (pendientes/atendidas)
- Acciones para marcar como atendidas

#### 4. **Usuarios**
- Gestión de personal del restaurante
- Lista de camareros/gerentes
- Funcionalidad de edición

#### 5. **Ajustes**
- Configuración del sistema (en desarrollo)

### 🔄 Funcionalidad en Tiempo Real

- **WebSockets**: Notificaciones instantáneas
- **Actualización Automática**: Cada 30 segundos
- **Alertas Visuales**: Notificaciones emergentes
- **Badge de Notificaciones**: Contador en tiempo real

### 🛡️ Seguridad

- Autenticación JWT
- Validación de permisos
- Protección CSRF

## Uso del Frontend

### Navegación
- Clic en cualquier elemento del panel lateral
- Cambio automático de título y contenido
- Indicador visual de sección activa

### Notificaciones
1. Las nuevas llamadas aparecen automáticamente
2. Alertas emergentes en la esquina superior derecha
3. Badge con contador en el menú "Notificaciones"
4. Botón "Atender" para marcar como resueltas

### Mapa de Mesas
- Mesas verdes: disponibles
- Mesas amarillas: con llamadas pendientes
- Clic para seleccionar mesa específica

### Datos de Ejemplo
El comando `create_sample_data` crea:
- 1 restaurante de ejemplo
- 12 mesas con cámaras
- 3 llamadas pendientes
- 2 llamadas atendidas
- 1 superusuario (admin/admin123)

## Integración con el Backend

### API Endpoints Utilizados:
- `GET /tables/` - Lista de mesas
- `GET /events/` - Lista de llamadas de servicio
- `PATCH /events/<id>/` - Actualizar estado de llamada
- `GET /restaurants/` - Lista de restaurantes

### WebSocket:
- `ws://localhost:8000/ws/events/` - Notificaciones en tiempo real

## Personalización

### Colores
Los colores principales están definidos en `styles.css`:
- Primary: `#4ECDC4` (azul verdoso)
- Secondary: `#2c3e50` (azul oscuro)
- Success: `#28a745` (verde)
- Warning: `#ffc107` (amarillo)
- Danger: `#dc3545` (rojo)

### Fuentes
- Font Family: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Iconos: Font Awesome 6.0

## Estructura de Archivos

```
frontend/
├── index.html      # Estructura HTML principal
├── styles.css      # Estilos CSS (replica del diseño)
├── script.js       # Funcionalidad JavaScript
└── README.md       # Este archivo
```

## Próximos Pasos

1. **Autenticación Completa**: Sistema de login/logout
2. **Gestión de Usuarios**: CRUD completo
3. **Configuración Avanzada**: Panel de ajustes funcional
4. **Reportes**: Análisis y métricas detalladas
5. **Mobile First**: Versión móvil optimizada

## Soporte

Para problemas o sugerencias:
1. Revisar la consola del navegador para errores
2. Verificar que Redis esté ejecutándose
3. Confirmar que el backend esté activo
4. Revisar logs de Django para errores de API 