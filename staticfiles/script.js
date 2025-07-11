// Configuración de la API
const API_BASE_URL = 'http://localhost:8000';
const WS_BASE_URL = 'ws://localhost:8000';

// Estado global
let currentSection = 'notificaciones';
let websocket = null;
let authToken = null;
let notificationUpdateTimeout = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM cargado, iniciando aplicación...');
    initializeApp();
    setupNavigation();
    setupWebSocket();
    loadInitialData();
});

// Inicializar aplicación
function initializeApp() {
    console.log('🔧 Inicializando aplicación...');
    // Verificar si hay token guardado
    authToken = localStorage.getItem('authToken');
    
    if (!authToken) {
        // En producción, redirigir a login
        console.log('No hay token de autenticación');
        // Para desarrollo, usar token de prueba
        authToken = 'test-token';
    }
    
    // Mostrar sección inicial y activar el enlace correspondiente
    showSection('notificaciones');
    
    // Activar visualmente el enlace de notificaciones
    const notificationLink = document.querySelector('[data-section="notificaciones"]');
    if (notificationLink) {
        notificationLink.classList.add('active');
    }
    console.log('✅ Aplicación inicializada');
}

// Configurar navegación
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remover clase activa de todos los links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Agregar clase activa al link actual
            this.classList.add('active');
            
            // Obtener sección
            const section = this.dataset.section;
            
            // Limpiar timeout de notificaciones si existe
            if (notificationUpdateTimeout) {
                clearTimeout(notificationUpdateTimeout);
                notificationUpdateTimeout = null;
            }
            
            // Cambiar título
            updatePageTitle(section);
            
            // Mostrar sección
            showSection(section);
            
            // Cargar datos específicos de la sección
            loadSectionData(section);
        });
    });
}

// Actualizar título de página
function updatePageTitle(section) {
    const titleElement = document.querySelector('.page-title');
    const titles = {
        'dashboard': 'Dashboard Principal',
        'mapa': 'Mapa del Restaurante',
        'usuarios': 'Gestión de Usuarios',
        'notificaciones': 'Notificaciones y Llamadas',
        'ajustes': 'Configuración del Sistema'
    };
    
    titleElement.textContent = titles[section] || 'Vision Singularity';
}

// Mostrar sección específica
function showSection(sectionName) {
    // Ocultar todas las secciones
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    
    // Mostrar sección seleccionada
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    currentSection = sectionName;
}

// Cargar datos iniciales
function loadInitialData() {
    console.log('📊 Iniciando carga de datos iniciales...');
    console.log('📋 Llamando a loadNotifications...');
    loadNotifications(true); // Mostrar spinner en carga inicial
    console.log('🗺️ Llamando a loadTables...');
    loadTables();
    console.log('👥 Llamando a loadUsers...');
    loadUsers();
    console.log('📈 Llamando a loadStats...');
    loadStats();
    console.log('✅ Datos iniciales cargados');
}

// Cargar datos específicos de sección
function loadSectionData(section) {
    switch(section) {
        case 'notificaciones':
            loadNotifications(true); // Mostrar spinner al cambiar a esta sección
            break;
        case 'mapa':
            loadTables();
            break;
        case 'usuarios':
            loadUsers();
            break;
        case 'dashboard':
            loadStats();
            loadChart();
            break;
    }
}

// Configurar WebSocket
function setupWebSocket() {
    try {
        websocket = new WebSocket(`${WS_BASE_URL}/ws/events/`);
        
        websocket.onopen = function(event) {
            console.log('WebSocket conectado');
        };
        
        websocket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };
        
        websocket.onclose = function(event) {
            console.log('WebSocket desconectado');
            // Intentar reconectar después de 3 segundos
            setTimeout(() => {
                setupWebSocket();
            }, 3000);
        };
        
        websocket.onerror = function(error) {
            console.error('Error en WebSocket:', error);
        };
        
    } catch (error) {
        console.error('Error al conectar WebSocket:', error);
    }
}

// Manejar mensajes de WebSocket
function handleWebSocketMessage(data) {
    if (data.content) {
        const notification = data.content;
        
        // Mostrar notificación en tiempo real
        showNotificationAlert(notification);
        
        // Actualizar badge de notificaciones
        updateNotificationBadge();
        
        // Recargar notificaciones con debounce para evitar parpadeo
        if (currentSection === 'notificaciones') {
            // Limpiar timeout anterior si existe
            if (notificationUpdateTimeout) {
                clearTimeout(notificationUpdateTimeout);
            }
            
            // Establecer nuevo timeout para actualizar después de 1 segundo
            notificationUpdateTimeout = setTimeout(() => {
                loadNotifications();
                notificationUpdateTimeout = null;
            }, 1000);
        }
        
        // Actualizar mapa si estamos en esa sección
        if (currentSection === 'mapa') {
            loadTables();
        }
    }
}

// Mostrar alerta de notificación
function showNotificationAlert(notification) {
    const alert = document.createElement('div');
    alert.className = 'notification-alert';
    alert.innerHTML = `
        <strong>Nueva llamada!</strong><br>
        Mesa ${notification.table} - ${notification.event_type}
    `;
    
    document.body.appendChild(alert);
    
    // Remover después de 5 segundos
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Actualizar badge de notificaciones
function updateNotificationBadge() {
    fetchAPI('/events/?status=pending')
        .then(data => {
            const badge = document.querySelector('.notification-badge');
            if (badge) {
                badge.textContent = data.length;
            }
        });
}

// Cargar notificaciones
function loadNotifications(showLoading = false) {
    console.log('🔄 Iniciando carga de notificaciones...');
    const tbody = document.getElementById('notifications-table-body');
    console.log('📋 Tabla encontrada:', tbody);
    
    // Solo mostrar spinner si es la primera carga o se indica explícitamente
    if (showLoading || tbody.innerHTML.trim() === '') {
        tbody.innerHTML = '<tr><td colspan="6" class="loading"><div class="spinner"></div></td></tr>';
        console.log('⏳ Mostrando spinner...');
    }
    
    console.log('📡 Haciendo petición a /events/...');
    fetchAPI('/events/')
        .then(data => {
            console.log('✅ Datos recibidos:', data);
            console.log('📊 Número de notificaciones:', data.length);
            renderNotifications(data);
        })
        .catch(error => {
            console.error('❌ Error cargando notificaciones:', error);
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #dc3545;">Error cargando datos</td></tr>';
        });
}

// Renderizar notificaciones
function renderNotifications(notifications) {
    console.log('🎨 Renderizando notificaciones...', notifications);
    const tbody = document.getElementById('notifications-table-body');
    console.log('📋 Elemento tbody:', tbody);
    
    if (notifications.length === 0) {
        console.log('⚠️ No hay notificaciones para mostrar');
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #6c757d;">No hay notificaciones</td></tr>';
        return;
    }
    
    console.log('📝 Generando HTML para', notifications.length, 'notificaciones');
    const htmlContent = notifications.map(notification => `
        <tr>
            <td>${notification.id}</td>
            <td>Mesa ${notification.table}</td>
            <td>${formatEventType(notification.event_type)}</td>
            <td>${formatDateTime(notification.created_at)}</td>
            <td>
                <span class="status-badge ${notification.status === 'pending' ? 'status-pending' : 'status-handled'}">
                    ${notification.status === 'pending' ? 'Pendiente' : 'Atendida'}
                </span>
            </td>
            <td>
                ${notification.status === 'pending' ? `
                    <button class="btn btn-sm btn-success" onclick="markAsHandled(${notification.id})">
                        <i class="fas fa-check"></i> Atender
                    </button>
                ` : `
                    <button class="btn btn-sm btn-info" disabled>
                        <i class="fas fa-check-circle"></i> Atendida
                    </button>
                `}
            </td>
        </tr>
    `).join('');
    
    console.log('✅ HTML generado, aplicando a tabla');
    tbody.innerHTML = htmlContent;
    console.log('🎉 Notificaciones renderizadas exitosamente');
}

// Marcar como atendida
function markAsHandled(id) {
    fetchAPI(`/events/${id}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            status: 'handled'
        })
    })
    .then(() => {
        loadNotifications(); // Sin spinner, actualización suave
        updateNotificationBadge();
    })
    .catch(error => {
        console.error('Error actualizando estado:', error);
        alert('Error al actualizar el estado de la notificación');
    });
}

// Cargar mesas
function loadTables() {
    fetchAPI('/tables/')
        .then(data => {
            renderRestaurantMap(data);
        })
        .catch(error => {
            console.error('Error cargando mesas:', error);
        });
}

// Renderizar mapa del restaurante
function renderRestaurantMap(tables) {
    const mapGrid = document.getElementById('restaurant-map-grid');
    
    if (tables.length === 0) {
        mapGrid.innerHTML = '<p style="text-align: center; color: #6c757d;">No hay mesas configuradas</p>';
        return;
    }
    
    // Obtener estado de las mesas (llamadas pendientes)
    fetchAPI('/events/?status=pending')
        .then(pendingCalls => {
            const pendingTables = pendingCalls.map(call => call.table);
            
            mapGrid.innerHTML = tables.map(table => `
                <div class="table-item ${pendingTables.includes(table.id) ? 'pending' : ''}" 
                     onclick="selectTable(${table.id})">
                    <div class="table-number">Mesa ${table.number}</div>
                    <div class="table-status">
                        ${pendingTables.includes(table.id) ? 'Llamando' : 'Disponible'}
                    </div>
                </div>
            `).join('');
        });
}

// Seleccionar mesa
function selectTable(tableId) {
    // Remover selección anterior
    document.querySelectorAll('.table-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Agregar selección actual
    event.target.closest('.table-item').classList.add('active');
    
    console.log('Mesa seleccionada:', tableId);
    // Aquí podrías mostrar más detalles de la mesa
}

// Cargar usuarios
function loadUsers() {
    // Simulación de datos de usuarios (en producción vendría de la API)
    const users = [
        { id: 1, name: 'Juan Pérez', email: 'juan@restaurant.com', role: 'Camarero', status: 'Activo' },
        { id: 2, name: 'María González', email: 'maria@restaurant.com', role: 'Camarera', status: 'Activo' },
        { id: 3, name: 'Carlos Ruiz', email: 'carlos@restaurant.com', role: 'Gerente', status: 'Activo' },
        { id: 4, name: 'Ana López', email: 'ana@restaurant.com', role: 'Camarera', status: 'Inactivo' }
    ];
    
    renderUsers(users);
}

// Renderizar usuarios
function renderUsers(users) {
    const tbody = document.getElementById('users-table-body');
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.role}</td>
            <td>
                <span class="status-badge ${user.status === 'Activo' ? 'status-handled' : 'status-pending'}">
                    ${user.status}
                </span>
            </td>
            <td>
                <button class="btn btn-sm btn-info" onclick="editUser(${user.id})">
                    <i class="fas fa-edit"></i> Editar
                </button>
            </td>
        </tr>
    `).join('');
}

// Editar usuario
function editUser(id) {
    alert(`Función para editar usuario ${id} - En desarrollo`);
}

// Cargar estadísticas
function loadStats() {
    Promise.all([
        fetchAPI('/tables/'),
        fetchAPI('/events/?status=pending'),
        fetchAPI('/events/')
    ])
    .then(([tables, pendingCalls, allCalls]) => {
        updateStats({
            totalTables: tables.length,
            activeTables: tables.filter(table => 
                pendingCalls.some(call => call.table === table.id)
            ).length,
            pendingCalls: pendingCalls.length,
            totalWaiters: 5 // Valor fijo por ahora
        });
    })
    .catch(error => {
        console.error('Error cargando estadísticas:', error);
    });
}

// Actualizar estadísticas
function updateStats(stats) {
    const statCards = document.querySelectorAll('.stat-card');
    const values = [stats.totalTables, stats.activeTables, stats.pendingCalls, stats.totalWaiters];
    
    statCards.forEach((card, index) => {
        const valueElement = card.querySelector('.stat-value');
        if (valueElement) {
            valueElement.textContent = values[index] || 0;
        }
    });
}

// Cargar gráfico
function loadChart() {
    const ctx = document.getElementById('callsChart');
    if (!ctx) return;
    
    // Datos simulados para el gráfico
    const data = {
        labels: ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'],
        datasets: [{
            label: 'Nuevas Llamadas',
            data: [2, 4, 6, 8, 12, 10, 8, 6],
            backgroundColor: '#4ECDC4',
            borderColor: '#4ECDC4',
            borderWidth: 1
        }, {
            label: 'Atendidas',
            data: [2, 3, 5, 7, 11, 9, 7, 5],
            backgroundColor: '#FF6B6B',
            borderColor: '#FF6B6B',
            borderWidth: 1
        }]
    };
    
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Función auxiliar para hacer peticiones a la API
async function fetchAPI(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log('🌐 Haciendo petición a:', url);
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            // Temporalmente sin autenticación para desarrollo
            // ...(authToken && { 'Authorization': `Bearer ${authToken}` })
        }
    };
    
    console.log('📋 Opciones de petición:', { ...defaultOptions, ...options });
    
    try {
        const response = await fetch(url, { ...defaultOptions, ...options });
        console.log('📡 Respuesta recibida:', response.status, response.statusText);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('📦 Datos parseados:', data);
        return data;
    } catch (error) {
        console.error('❌ Error en fetchAPI:', error);
        throw error;
    }
}

// Formatear tipo de evento
function formatEventType(eventType) {
    const types = {
        'hand_raise': 'Mano Levantada',
        'wave': 'Saludo',
        'raise': 'Mano Levantada'
    };
    return types[eventType] || eventType;
}

// Formatear fecha y hora
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Configurar filtros
document.getElementById('status-filter')?.addEventListener('change', function() {
    const status = this.value;
    const url = status ? `/events/?status=${status}` : '/events/';
    
    fetchAPI(url)
        .then(data => {
            renderNotifications(data);
        })
        .catch(error => {
            console.error('Error filtrando notificaciones:', error);
        });
});

// Actualizar datos cada 30 segundos
setInterval(() => {
    if (currentSection === 'notificaciones') {
        loadNotifications();
    } else if (currentSection === 'mapa') {
        loadTables();
    }
    updateNotificationBadge();
}, 30000); 