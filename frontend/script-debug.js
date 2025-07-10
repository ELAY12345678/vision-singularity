// DEBUG: Script simplificado para probar navegación
console.log('🔍 DEBUG: Script iniciado');

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 DEBUG: DOM cargado');
    
    // Probar navegación básica
    setupSimpleNavigation();
    
    // Mostrar sección inicial
    showSection('notificaciones');
    console.log('🔍 DEBUG: Sección inicial mostrada');
});

function setupSimpleNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    console.log('🔍 DEBUG: Enlaces encontrados:', navLinks.length);
    
    navLinks.forEach((link, index) => {
        console.log(`🔍 DEBUG: Enlace ${index}:`, link.dataset.section);
        
        link.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('🔍 DEBUG: Click en enlace:', this.dataset.section);
            
            // Remover clase activa
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Agregar clase activa
            this.classList.add('active');
            console.log('🔍 DEBUG: Clase activa agregada');
            
            // Obtener sección
            const section = this.dataset.section;
            console.log('🔍 DEBUG: Cambiando a sección:', section);
            
            // Mostrar sección
            showSection(section);
            
            // Cambiar título
            const titleElement = document.querySelector('.page-title');
            if (titleElement) {
                titleElement.textContent = `Sección: ${section}`;
                console.log('🔍 DEBUG: Título cambiado');
            }
        });
    });
}

function showSection(sectionName) {
    console.log('🔍 DEBUG: Intentando mostrar sección:', sectionName);
    
    // Ocultar todas las secciones
    const sections = document.querySelectorAll('.content-section');
    console.log('🔍 DEBUG: Secciones encontradas:', sections.length);
    
    sections.forEach((section, index) => {
        section.style.display = 'none';
        console.log(`🔍 DEBUG: Sección ${index} (${section.id}) ocultada`);
    });
    
    // Mostrar sección seleccionada
    const targetSection = document.getElementById(`${sectionName}-section`);
    console.log('🔍 DEBUG: Sección objetivo:', targetSection);
    
    if (targetSection) {
        targetSection.style.display = 'block';
        console.log('🔍 DEBUG: Sección mostrada exitosamente');
    } else {
        console.error('🔍 DEBUG: ERROR - Sección no encontrada:', `${sectionName}-section`);
    }
}

// Test manual
window.testNavigation = function() {
    console.log('🔍 DEBUG: Test manual de navegación');
    const sections = ['dashboard', 'mapa', 'usuarios', 'notificaciones', 'ajustes'];
    
    sections.forEach(section => {
        console.log(`🔍 DEBUG: Probando sección: ${section}`);
        showSection(section);
    });
};

console.log('🔍 DEBUG: Script debug cargado. Ejecuta testNavigation() en consola para probar manualmente.'); 