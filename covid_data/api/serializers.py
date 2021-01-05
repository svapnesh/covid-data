from rest_framework import serializers

from usermgmt.models import CustomUser
from .validators import first_name_validator, last_name_validator


class CustomUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(validators=[first_name_validator])
    last_name = serializers.CharField(validators=[last_name_validator])
    country = serializers.ChoiceField(choices=CustomUser.country_choices)
    email = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'country']

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)
