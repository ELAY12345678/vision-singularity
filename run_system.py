#!/usr/bin/env python3
"""
Script para iniciar el sistema completo de Vision Singularity
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_redis():
    """Verificar si Redis está ejecutándose"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        return True
    except:
        return False

def start_redis():
    """Intentar iniciar Redis"""
    print("🔄 Iniciando Redis...")
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['redis-server'])
        else:  # Unix/Linux/Mac
            subprocess.Popen(['redis-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        return check_redis()
    except:
        return False

def setup_database():
    """Configurar la base de datos"""
    print("🔄 Configurando base de datos...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_sample_data():
    """Crear datos de ejemplo"""
    print("🔄 Creando datos de ejemplo...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'create_sample_data'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_django():
    """Iniciar el servidor Django"""
    print("🚀 Iniciando servidor Django...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar Django: {e}")

def main():
    """Función principal"""
    print("🎯 Vision Singularity - Sistema de Gestión de Restaurantes")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path('manage.py').exists():
        print("❌ Error: No se encontró manage.py")
        print("   Asegúrate de ejecutar este script desde el directorio del proyecto")
        sys.exit(1)
    
    # Verificar Redis
    if not check_redis():
        print("⚠️  Redis no está ejecutándose")
        if not start_redis():
            print("❌ Error: No se pudo iniciar Redis")
            print("   Instala Redis o inicia manualmente con: redis-server")
            print("   O usa Docker: docker run -d -p 6379:6379 redis:latest")
            sys.exit(1)
    
    print("✅ Redis está ejecutándose")
    
    # Configurar base de datos
    if not setup_database():
        print("❌ Error al configurar la base de datos")
        sys.exit(1)
    
    print("✅ Base de datos configurada")
    
    # Crear datos de ejemplo
    if not create_sample_data():
        print("❌ Error al crear datos de ejemplo")
        sys.exit(1)
    
    print("✅ Datos de ejemplo creados")
    
    print("\n🌟 Sistema listo!")
    print("📱 Frontend: http://localhost:8000/")
    print("🛠️  Admin: http://localhost:8000/admin/ (admin/admin123)")
    print("🔌 API: http://localhost:8000/events/")
    print("\n⚠️  Para detener el servidor, presiona Ctrl+C")
    print("-" * 60)
    
    # Iniciar Django
    start_django()

if __name__ == "__main__":
    main() 