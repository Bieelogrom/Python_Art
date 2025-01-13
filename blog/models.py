from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    
class Posts(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=100)
    imagem = models.ImageField(upload_to='img/posts')
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    