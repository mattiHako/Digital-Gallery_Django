from django.contrib.auth.models import User
from django.db import models
from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
import os

# Validator funktio väärille kuvatyypeille, jos käyttäjä koittaa ladata vääränlaisen tiedoston
def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # Extract the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Trying to upload an unsupported file extension.')

# Kansion tietokantataulukko
class Folder(models.Model):
    name = models.CharField(max_length = 100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')

    def __str__(self):
        return self.name

# Kuvien tietokantataulukko
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_title = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='images/', validators=[validate_image_extension])
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    
    # Kuvien tallentamisen funktio. Sisältää monia vaiheita.
    def save(self, *args, **kwargs):
        if not self.thumbnail:
            super().save(*args, **kwargs) # Tallentaa modelin ensin
            
            img = PilImage.open(self.image.path) # Avaa alkuperäisen tiedoston Pillowilla.
        
            # Määritetään thumbnalen koko
            tnsize = (128, 128)
            img.thumbnail(tnsize, PilImage.LANCZOS)
            
            # Tallentaa thumbnailin tilapäiseen puskurimuistiin
            temp_thumb = BytesIO()
            
            # hae tiedoston alkuperäinen formaatti
            original_format = img.format
            img_format = 'JPEG' if original_format != 'PNG' else 'PNG'
            
            if original_format == 'GIF':
                img.save(temp_thumb, format='GIF')
            else:
                tnsize = (128, 128)
                img.thumbnail(tnsize, PilImage.LANCZOS)

                if img_format == 'PNG':
                    img.save(temp_thumb, format='PNG')
                else:
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    img.save(temp_thumb, format='JPEG', quality=95)
                    
            temp_thumb.seek(0)
            
            # Asettaa thumbnalen kentän uudeksi pakatuksi kuvaksi
            self.thumbnail.save(
                self.image.name, 
                ContentFile(temp_thumb.read()), 
                save=False
            )
            temp_thumb.close()
            
            # Tallentaa modelin uudestaan taltioidakseen thumbnailin.
        super().save(*args, **kwargs)
        
            
        
        