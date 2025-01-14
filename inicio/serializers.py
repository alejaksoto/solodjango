from rest_framework import serializers
from .models import PlantillaMensaje

class PlantillaMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantillaMensaje
        fields = ['id', 'nombre', 'cuerpo', 'empresa', 'es_aprobada', 'fecha_creacion']
        read_only_fields = ['empresa', 'es_aprobada']
