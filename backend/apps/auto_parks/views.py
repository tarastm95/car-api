from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response

from apps.auto_parks.models import AutoParkModel
from apps.auto_parks.serializers import AutoParksSerializer
from apps.cars.serializers import CarSerializer

# Create your views here.

class AutoParkListCreateAPIView(ListCreateAPIView):
    serializer_class = AutoParksSerializer
    queryset = AutoParkModel.objects.all()

class AutoParkAddCarView(GenericAPIView):
    queryset = AutoParkModel.objects.all()

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        auto_park = self.get_object()
        serializer.save(auto_park_id=auto_park.id)
        park_serializer =  AutoParksSerializer(auto_park)
        return Response(park_serializer.data, status=status.HTTP_201_CREATED)
