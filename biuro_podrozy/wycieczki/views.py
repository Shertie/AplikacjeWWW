from rest_framework import viewsets, permissions
from .models import Kraj, LiniaLotnicza, Lot, Hotel, Wycieczka
from .serializers import (
    KrajSerializer, LiniaLotniczaSerializer, LotSerializer, 
    HotelSerializer, WycieczkaSerializer
)

class KrajViewSet(viewsets.ModelViewSet):
    queryset = Kraj.objects.all()
    serializer_class = KrajSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class LiniaLotniczaViewSet(viewsets.ModelViewSet):
    queryset = LiniaLotnicza.objects.all()
    serializer_class = LiniaLotniczaSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class LotViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class WycieczkaViewSet(viewsets.ModelViewSet):
    queryset = Wycieczka.objects.all()
    serializer_class = WycieczkaSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

