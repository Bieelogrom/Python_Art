from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    
class Posts(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=100)
    imagem = models.ImageField(upload_to='img/posts')
    data_publicacao = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class PostagensSalvas(models.Model):
    id_usuario_que_salvou = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_postagem_salva = models.ForeignKey(Posts, on_delete=models.CASCADE)
    horario_salvo = models.DateTimeField(default=timezone.now)
    
    