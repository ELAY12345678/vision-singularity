# 🚀 Instrucciones Rápidas - Vision Singularity Frontend

## Para Probar el Frontend AHORA

### 1. Instalación Rápida
```bash
# 1. Instala las dependencias
pip install -r visionsingularity/requirements.txt

# 2. Instala Redis (si no lo tienes)
# Ubuntu/Debian:
sudo apt install redis-server

# macOS:
brew install redis

# Windows: Descarga desde https://redis.io/download
```

### 2. Inicio Automático
```bash
# Opción 1: Script automático (recomendado)
python run_system.py

# Opción 2: Manual
python manage.py migrate
python manage.py create_sample_data
python manage.py runserver
```

### 3. Acceso al Sistema
- **Frontend**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/ (admin/admin123)
- **API**: http://localhost:8000/events/

## 🎯 Qué Verás en el Frontend

### Panel Lateral (Exacto a la imagen)
- ✅ **Logo**: Vision Singularity con icono de ojo
- ✅ **Dashboard**: Estadísticas y gráficos
- ✅ **Mapa**: Visualización de mesas del restaurante
- ✅ **Usuarios**: Lista de empleados
- ✅ **Notificaciones**: Llamadas de servicio (ACTIVO por defecto)
- ✅ **Ajustes**: En desarrollo

### Área Principal
- ✅ **Títulos dinámicos**: Cambian según la sección
- ✅ **Botones Export/Nuevo**: Estilo idéntico a la imagen
- ✅ **Tabla de notificaciones**: Con filtros y acciones
- ✅ **Estadísticas**: Tarjetas con íconos y números
- ✅ **Gráfico**: Barras de llamadas por hora

## 🔄 Funcionalidades en Tiempo Real

### Notificaciones WebSocket
1. **Conexión automática** al abrir el frontend
2. **Alertas emergentes** en la esquina superior derecha
3. **Badge con contador** en el menú de notificaciones
4. **Actualización automática** de la tabla sin recargar

### Datos de Ejemplo Incluidos
- 12 mesas con cámaras
- 3 llamadas PENDIENTES (se mostrarán en amarillo)
- 2 llamadas ATENDIDAS (se mostrarán en verde)
- Restaurante "El Futuro" configurado

## 🎨 Diseño Replicado

### Colores Exactos
- **Primary**: #4ECDC4 (azul verdoso de la imagen)
- **Sidebar**: #2c3e50 (azul oscuro de la imagen)
- **Success**: #28a745 (verde de botones)
- **Warning**: #ffc107 (amarillo de pendientes)

### Elementos Visuales
- ✅ **Padding idéntico** a la imagen
- ✅ **Fuentes** del mismo estilo
- ✅ **Sombras** en tarjetas
- ✅ **Bordes redondeados**
- ✅ **Espaciado** entre elementos
- ✅ **Hover effects** en botones

## 🧪 Pruebas Rápidas

### 1. Navegación
- Clic en cualquier elemento del menú lateral
- Verifica que el título cambie automáticamente
- Confirma que el indicador activo se mueva

### 2. Notificaciones
- Ve a la sección "Notificaciones"
- Verás 3 llamadas pendientes
- Clic en "Atender" para marcar como resuelta
- Observa la actualización en tiempo real

### 3. Mapa de Mesas
- Ve a la sección "Mapa"
- Verás 12 mesas en grid
- Mesas con llamadas pendientes aparecen en amarillo
- Clic en cualquier mesa para seleccionarla

### 4. WebSocket en Vivo
```bash
# En otra terminal, simula una nueva llamada:
curl -X POST http://localhost:8000/events/ \
  -H "Content-Type: application/json" \
  -d '{"table": 1, "event_type": "hand_raise"}'
```

## 🔧 Solución de Problemas

### Redis no está ejecutándose
```bash
# Iniciar Redis manualmente
redis-server

# O con Docker
docker run -d -p 6379:6379 redis:latest
```

### Error en la base de datos
```bash
# Recrear la base de datos
python manage.py migrate
python manage.py create_sample_data
```

### WebSocket no conecta
1. Verifica que Redis esté ejecutándose
2. Revisa la consola del navegador para errores
3. Confirma que el servidor Django esté activo

## 📱 Responsive Design

El frontend está optimizado para:
- **Desktop**: Experiencia completa
- **Tablet**: Panel lateral se colapsa
- **Mobile**: Navegación optimizada

## 🚀 Próximos Pasos

Después de probar el frontend:

1. **Integrar con cámaras reales** usando el simulador
2. **Mejorar algoritmos de CV** para mayor precisión
3. **Agregar autenticación completa**
4. **Implementar sistema de reportes**
5. **Optimizar para producción**

---

**¡El frontend está listo para usar!** 🎉
Replica exactamente el diseño de la imagen y incluye todas las funcionalidades solicitadas. 