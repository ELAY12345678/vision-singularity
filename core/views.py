from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Restaurant, Table, ServiceCall
from .serializers import RestaurantSerializer, TableSerializer, ServiceCallSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

class RestaurantList(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RestaurantDetail(APIView):
    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TableList(generics.ListAPIView):                 # GET only
    queryset           = Table.objects.all()
    serializer_class   = TableSerializer
    permission_classes = [permissions.IsAuthenticated]

class ServiceCallListCreate(generics.ListCreateAPIView):
    queryset = ServiceCall.objects.all()
    serializer_class = ServiceCallSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']  # allow filtering by status

class ServiceCallDetail(generics.RetrieveUpdateAPIView):
    queryset = ServiceCall.objects.all()
    serializer_class = ServiceCallSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get('status', instance.status)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

