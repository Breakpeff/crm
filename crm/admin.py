from django.contrib import admin
from .models import Empresa, Contato, Oportunidade

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'email')

@admin.register(Oportunidade)
class OportunidadeAdmin(admin.ModelAdmin):
    list_display = ('contato', 'valor', 'estagio', 'vendedor')