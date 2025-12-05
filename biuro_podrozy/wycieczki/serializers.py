from rest_framework import serializers
from .models import Kraj, LiniaLotnicza, Lot, Hotel, Wycieczka
from django.utils import timezone

class KrajSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kraj
        fields = '__all__'

class LiniaLotniczaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiniaLotnicza
        fields = '__all__'

class LotSerializer(serializers.ModelSerializer):
    linia_lotnicza_nazwa = serializers.CharField(source='linia_lotnicza.nazwa', read_only=True)

    class Meta:
        model = Lot
        fields = '__all__'
    
    def validate(self, data):
        """
        Sprawdza czy data przylotu jest późniejsza niż data wylotu.
        """
        if data['data_przylotu'] <= data['data_wylotu']:
            raise serializers.ValidationError("Data przylotu musi być późniejsza niż data wylotu.")
        return data

class HotelSerializer(serializers.ModelSerializer):
    kraj_nazwa = serializers.CharField(source='kraj.nazwa', read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'

class WycieczkaSerializer(serializers.ModelSerializer):
    kraj_docelowy_nazwa = serializers.CharField(source='kraj_docelowy.nazwa', read_only=True)
    hotel_nazwa = serializers.CharField(source='hotel.nazwa', read_only=True)
    
    class Meta:
        model = Wycieczka
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        """
        Walidacja wycieczki.
        """
        # Sprawdzenie czy lot powrotny jest po locie tam (jeśli dotyczy dat, ale tu mamy relacje do Lot)
        # Możemy sprawdzić czy kraj hotelu zgadza się z krajem docelowym wycieczki
        if 'hotel' in data and 'kraj_docelowy' in data:
            if data['hotel'].kraj != data['kraj_docelowy']:
                raise serializers.ValidationError("Hotel musi znajdować się w kraju docelowym wycieczki.")
        return data
