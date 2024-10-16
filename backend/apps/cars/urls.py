from django.urls import path

from .views import CarRetrieveUpdateDestroyView, CarListView,CarAddPhotosView

urlpatterns = [
    path('', CarListView.as_view(), name='cars_list'),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view(), name='cars_retrieve_update_destroy'),
    path('/<int:pk>/photos', CarAddPhotosView.as_view(), name='cars_add_photo'),
]
