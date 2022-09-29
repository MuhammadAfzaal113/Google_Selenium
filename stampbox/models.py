from django.db import models
import uuid

# Create your models here.


class Images_model(models.Model):
    img_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    media_file = models.FileField(upload_to='File_Storage/', max_length=500, null=True, default='')

    def __str__(self):
        return str(self.img_id)

    class Meta:
        db_table = "uploaded_image"
        verbose_name_plural = "uploaded_images"
