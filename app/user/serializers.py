from django.contrib.auth import get_user_model
from django.forms import fields

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields =('email', 'password', 'name')
        extra_kwargs = {'password':{'write_only':True, 'min_length':5}}

    def create(self, validated_data):
        """Create a new user with encryted password and return it"""
        return get_user_model().objects.crreate_user(**validated_data)
    