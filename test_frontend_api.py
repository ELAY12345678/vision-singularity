#!/usr/bin/env python3
"""
Script para verificar que el frontend y la API funcionen completamente
"""

import requests
import json
import sys

def test_api():
    """Probar todas las APIs del frontend"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Probando APIs de Vision Singularity...")
    print("=" * 50)
    
    # Test 1: Eventos
    try:
        response = requests.get(f"{base_url}/events/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Eventos: OK ({len(data)} eventos encontrados)")
            if data:
                event = data[0]
                print(f"   Ejemplo: Mesa {event['table']} - {event['event_type']} - {event['status']}")
        else:
            print(f"❌ API Eventos: ERROR {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Eventos: ERROR {e}")
        return False
    
    # Test 2: Mesas
    try:
        response = requests.get(f"{base_url}/tables/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Mesas: OK ({len(data)} mesas encontradas)")
            if data:
                table = data[0]
                print(f"   Ejemplo: Mesa {table['number']} - Cámara {table['camera_id']}")
        else:
            print(f"❌ API Mesas: ERROR {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Mesas: ERROR {e}")
        return False
    
    # Test 3: Frontend
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            if "Vision Singularity" in response.text:
                print("✅ Frontend: OK (página carga correctamente)")
            else:
                print("❌ Frontend: Página carga pero falta contenido")
                return False
        else:
            print(f"❌ Frontend: ERROR {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend: ERROR {e}")
        return False
    
    # Test 4: Archivos estáticos
    static_files = ["styles.css", "script.js"]
    for filename in static_files:
        try:
            response = requests.get(f"{base_url}/static/{filename}")
            if response.status_code == 200:
                print(f"✅ {filename}: OK")
            else:
                print(f"❌ {filename}: ERROR {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {filename}: ERROR {e}")
            return False
    
    print("\n🎉 ¡Todos los tests pasaron!")
    print("\n📋 Datos encontrados:")
    
    # Mostrar resumen de datos
    events_response = requests.get(f"{base_url}/events/")
    events = events_response.json()
    
    pending = [e for e in events if e['status'] == 'pending']
    handled = [e for e in events if e['status'] == 'handled']
    
    print(f"   📧 {len(pending)} llamadas PENDIENTES")
    print(f"   ✅ {len(handled)} llamadas ATENDIDAS")
    
    tables_response = requests.get(f"{base_url}/tables/")
    tables = tables_response.json()
    print(f"   🪑 {len(tables)} mesas configuradas")
    
    print("\n🚀 El frontend debería mostrar todos estos datos correctamente!")
    
    return True

def main():
    """Función principal"""
    print("🎯 Vision Singularity - Test Completo")
    print("Verificando que el frontend cargue datos correctamente...")
    print()
    
    if test_api():
        print("\n✨ ÉXITO: Todo funciona correctamente")
        print("\n📱 Instrucciones:")
        print("1. Abre http://localhost:8000/ en tu navegador")
        print("2. Deberías ver el diseño completo con estilos")
        print("3. La tabla de 'Notificaciones' debe mostrar datos")
        print("4. Navega entre secciones usando el menú lateral")
        print("5. En 'Mapa' verás las mesas del restaurante")
        print("6. Usa los botones 'Atender' para marcar llamadas como resueltas")
        
        print("\n🔄 Para probar en tiempo real:")
        print("   curl -X POST http://localhost:8000/events/ \\")
        print("        -H 'Content-Type: application/json' \\")
        print("        -d '{\"table\": 1, \"event_type\": \"hand_raise\"}'")
        
        sys.exit(0)
    else:
        print("\n❌ FALLO: Hay problemas que resolver")
        sys.exit(1)

if __name__ == "__main__":
    main() 