#!/usr/bin/env python3
"""
Script para verificar que el frontend se esté cargando correctamente
"""

import requests
import sys

def check_frontend():
    """Verificar que el frontend y archivos estáticos se carguen correctamente"""
    
    base_url = "http://localhost:8000"
    
    print("🔍 Verificando el frontend de Vision Singularity...")
    print("=" * 50)
    
    # Verificar página principal
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Página principal: OK")
            if "Vision Singularity" in response.text:
                print("✅ Título encontrado: OK")
            else:
                print("❌ Título no encontrado")
        else:
            print(f"❌ Página principal: ERROR {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("   Asegúrate de que el servidor esté ejecutándose:")
        print("   python manage.py runserver")
        return False
    
    # Verificar archivos estáticos
    static_files = [
        ("styles.css", "text/css"),
        ("script.js", "text/javascript")
    ]
    
    for filename, content_type in static_files:
        try:
            response = requests.get(f"{base_url}/static/{filename}")
            if response.status_code == 200:
                print(f"✅ {filename}: OK")
                if content_type in response.headers.get('Content-Type', ''):
                    print(f"   Content-Type: {response.headers.get('Content-Type')}")
                else:
                    print(f"   ⚠️  Content-Type inesperado: {response.headers.get('Content-Type')}")
            else:
                print(f"❌ {filename}: ERROR {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ {filename}: ERROR {e}")
            return False
    
    print("\n🎉 Frontend funcionando correctamente!")
    print("\n📱 URLs disponibles:")
    print(f"   Frontend: {base_url}/")
    print(f"   Admin: {base_url}/admin/")
    print(f"   API: {base_url}/events/")
    
    print("\n🔄 Para probar:")
    print("   1. Abre el navegador en http://localhost:8000/")
    print("   2. Verifica que se vean los estilos CSS")
    print("   3. Abre DevTools (F12) y revisa la consola")
    print("   4. Navega entre las secciones del menú lateral")
    
    return True

if __name__ == "__main__":
    if check_frontend():
        sys.exit(0)
    else:
        sys.exit(1) 