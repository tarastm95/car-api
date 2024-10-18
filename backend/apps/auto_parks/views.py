from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from apps.auto_parks.models import AutoParkModel
from apps.auto_parks.serializers import AutoParksSerializer
from apps.cars.serializers import CarSerializer

# Створюємо ErrorSerializer з унікальним ref_name для Swagger
class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()

    class Meta:
        ref_name = "AutoParkErrorSerializer"


class AutoParkListCreateAPIView(ListCreateAPIView):
    serializer_class = AutoParksSerializer
    queryset = AutoParkModel.objects.all()


class AutoParkAddCarView(GenericAPIView):
    queryset = AutoParkModel.objects.all()

    def get_serializer(self, *args, **kwargs):
        pass  # Уникаємо проблем з Swagger

    @swagger_auto_schema(
        request_body=CarSerializer,
        responses={status.HTTP_201_CREATED: AutoParksSerializer, status.HTTP_400_BAD_REQUEST: ErrorSerializer}
    )
    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        auto_park = self.get_object()

        try:
            serializer.save(auto_park_id=auto_park.id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        park_serializer = AutoParksSerializer(auto_park)
        return Response(park_serializer.data, status=status.HTTP_201_CREATED)
