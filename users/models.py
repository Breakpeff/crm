from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    Cargos = (
        ('admin', 'Administrator'),
        ('vendedor', 'Vendedor'),
        ('sdr', 'SDR'),


    )
    cargo = models.CharField(max_length=20, choices=Cargos, default='vendedor')
    telefone = models.CharField(max_length=15, blank=True, null=True)
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)

    def __str__(self):
        return self.username