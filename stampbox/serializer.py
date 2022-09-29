from rest_framework import serializers
from helpers.log_util import logger
from stampbox.models import Images_model
from stampbox.serial_model import UploadImageSerializer


class image_Add_serializer(serializers.ModelSerializer):
    try:
        image_file = UploadImageSerializer

        class Meta:
            model = Images_model
            fields = '__all__'

        def create(self, validated_data):
            logger.info(f'[UploadImage_AddSerializer] Adding Media For Stamp Image')
            image_file = Images_model.objects.create(media_file=validated_data['media_file'])
            return image_file

    except Exception as e:
        logger.error(f'[UploadImage_AddSerializer] Serializer throws Exception :{e}')
