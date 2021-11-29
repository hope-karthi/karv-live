from django.db.models import fields
from baseapp.models import Room
from rest_framework.serializers import ModelSerializer

class RoomSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'