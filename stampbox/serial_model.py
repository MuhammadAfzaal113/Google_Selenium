from rest_framework import serializers
from stampbox.models import Images_model


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images_model
        fields = '__all__'
