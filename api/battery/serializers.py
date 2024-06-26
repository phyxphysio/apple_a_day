from rest_framework import serializers
from .models import Energy

class EnergySerializer(serializers.ModelSerializer):

    class Meta:
        model = Energy 
        fields = ('pk', 'wellbeing', 'mental_stress', 'physical_stress', 'date_added')
