from django.db import models

# Create your models here.


class Image(models.Model):
    phrase = models.CharField(max_length=200)
    ai_image = models.ImageField(upload_to='images')

    def _str_(self):
        return str(self.phrase)
    
