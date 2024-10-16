from django.forms import model_to_dict

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser,IsAuthenticatedOrReadOnly
from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializer, CarPhotoSerializer

from .filters import CarFilter

# Використовуємо дженеріки для роботи з вбудованими методами GenericAPIView

# Клас для роботи зі списком машин (отримання та створення)
class CarListView(ListAPIView):
    queryset = CarModel.objects.all()  # Базовий queryset
    serializer_class = CarSerializer  # Серіалізатор для обробки даних
    filterset_class = CarFilter
    permission_classes = (AllowAny,)

# Клас для роботи з конкретним записом про машину (отримання, оновлення, видалення)
class CarRetrieveUpdateDestroyView(GenericAPIView):
    queryset = CarModel.objects.all()  # Вказуємо кверісет для отримання запису

    # Отримуємо конкретний запис про машину за ID (GET запит)
    def get(self, *args, **kwargs):
        car = self.get_object()  # Отримуємо об'єкт за ID з бази даних
        serializer = CarSerializer(car)  # Серіалізуємо дані
        return Response(serializer.data, status=status.HTTP_200_OK)  # Відправляємо відповідь зі статусом 200

    # Оновлюємо конкретний запис про машину (PUT запит)
    def put(self, *args, **kwargs):
        data = self.request.data  # Отримуємо нові дані для оновлення
        car = self.get_object()  # Отримуємо об'єкт за ID
        serializer = CarSerializer(car, data)  # Передаємо об'єкт та нові дані до серіалізатора
        serializer.is_valid(raise_exception=True)  # Перевіряємо валідність даних
        serializer.save()  # Зберігаємо зміни в базу даних
        return Response(model_to_dict(car), status=status.HTTP_200_OK)  # Відправляємо відповідь зі статусом 200

    # Видаляємо конкретний запис про машину (DELETE запит)
    def delete(self, *args, **kwargs):
        self.get_object().delete()  # Видаляємо об'єкт з бази даних
        return Response(status=status.HTTP_204_NO_CONTENT)  # Відправляємо відповідь зі статусом 204

    # Часткове оновлення запису (PATCH запит)
    def patch(self, request, *args, **kwargs):
        car = self.get_object()  # Отримуємо конкретний об'єкт
        serializer = CarSerializer(car, data=request.data, partial=True)  # Передаємо часткові дані до серіалізатора
        serializer.is_valid(raise_exception=True)  # Перевіряємо валідність даних
        serializer.save()  # Зберігаємо зміни
        return Response(serializer.data, status=status.HTTP_200_OK)  # Відправляємо відповідь зі статусом 200

class CarAddPhotosView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    # serializer_class = CarPhotoSerializer
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