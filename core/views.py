from django.http import JsonResponse
from .serializers import HelloSerializer  # ← import your new serializer clearly

def hello_world(request):
    data = {'message': 'Hello, Vision Singularity!'}
    serializer = HelloSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return JsonResponse(serializer.data)


