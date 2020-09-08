from django.db import models
from django.contrib.auth import get_user_model

class Image(models.Model): 
    image_name = models.CharField(max_length=50) 
    image_file = models.ImageField(upload_to='images/') 
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.image_name

    class Meta:
        ordering = ('image_name',)


