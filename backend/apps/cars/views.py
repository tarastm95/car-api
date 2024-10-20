from django.forms import model_to_dict
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializer, CarPhotoSerializer

from .filters import CarFilter

@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class CarListView(ListCreateAPIView):
    """
        get:
            Get car by id
        put:
            Full Update car by id
        patch:
            Partial Update car by id
        delete:
            Delete car by id
    """
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    filterset_class = CarFilter
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(auto_park_id=1)
        super().perform_create(serializer)


class CarRetrieveUpdateDestroyView(GenericAPIView):
    """
        get:
            Get car by id
        put:
            Full Update car by id
        patch:
            Partial Update car by id
        delete:
            Delete car by id
    """
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer  # Added serializer_class
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        car = self.get_object()
        serializer = CarSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, *args, **kwargs):
        data = self.request.data
        car = self.get_object()
        serializer = CarSerializer(car, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(model_to_dict(car), status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        car = self.get_object()
        serializer = CarSerializer(car, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CarAddPhotosView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CarPhotoSerializer  # Added serializer_class
    queryset = CarModel.objects.all()

    def put(self, *args, **kwargs):
        files = self.request.FILES
        car = self.get_object()
        for index in files:
            serializer = CarPhotoSerializer(data={'photo': files[index]})
            serializer.is_valid(raise_exception=True)
            serializer.save(car=car)
        car_serializer = CarSerializer(car)
        return Response(car_serializer.data, status=status.HTTP_200_OK)
