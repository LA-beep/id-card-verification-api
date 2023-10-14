from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import User, IdentityCards, PassportDetails


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class IdentitycardSerializer(serializers.ModelSerializer):

    class Meta:
        model = IdentityCards
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=IdentityCards.objects.all(),
                fields=['contactNo', 'identity_type'],
                message ="An identity card with the same contact number and identity type already exists."
            )
        ]


class PassportDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PassportDetails
        fields = '__all__'