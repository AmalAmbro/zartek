from rest_framework.serializers import ModelSerializer

from ride.models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password',]

class RideSerializer(ModelSerializer):
    class Meta:
        model = Rides
        fields = "__all__"
