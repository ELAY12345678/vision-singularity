from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Restaurant, Table, ServiceCall

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para el frontend'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de ejemplo...')
        
        # Crear superusuario si no existe
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@visionsingularity.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Superusuario creado: admin/admin123'))
        
        # Crear restaurante de ejemplo
        restaurant, created = Restaurant.objects.get_or_create(
            name='Restaurante El Futuro',
            defaults={
                'address': 'Calle Tecnología 123, Ciudad',
                'phone': '+1-555-0123'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Restaurante creado: {restaurant.name}'))
        
        # Crear mesas de ejemplo
        for i in range(1, 13):  # 12 mesas
            table, created = Table.objects.get_or_create(
                restaurant=restaurant,
                number=i,
                defaults={
                    'camera_id': f'cam-{i:03d}'
                }
            )
            
            if created:
                self.stdout.write(f'Mesa {i} creada')
        
        # Crear algunas llamadas de servicio de ejemplo
        tables = Table.objects.all()[:5]  # Primeras 5 mesas
        
        # Limpiar ServiceCalls existentes para evitar duplicados
        ServiceCall.objects.all().delete()
        
        for i, table in enumerate(tables):
            if i < 3:  # Crear 3 llamadas pendientes
                ServiceCall.objects.create(
                    table=table,
                    event_type='hand_raise' if i % 2 == 0 else 'wave',
                    status='pending'
                )
                self.stdout.write(f'Llamada pendiente creada para Mesa {table.number}')
        
        # Crear algunas llamadas ya atendidas
        for i, table in enumerate(tables):
            if i >= 3:  # Crear 2 llamadas atendidas
                ServiceCall.objects.create(
                    table=table,
                    event_type='wave',
                    status='handled'
                )
                self.stdout.write(f'Llamada atendida creada para Mesa {table.number}')
        
        self.stdout.write(self.style.SUCCESS('¡Datos de ejemplo creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS('Puedes acceder al admin con: admin/admin123'))
        self.stdout.write(self.style.SUCCESS('Inicia el servidor con: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('Accede al frontend en: http://localhost:8000/')) 