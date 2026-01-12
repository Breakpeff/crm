from django import forms
from .models import Contato, Empresa, Oportunidade
class OportunidadeForm(forms.ModelForm):
    class Meta:
        model = Oportunidade
        fields = ['titulo', 'contato', 'valor', 'estagio', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'contato': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'valor': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'estagio': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'descricao': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 3}),
        }
        

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone', 'empresa']
        widgets = {
            field: forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500'})
            for field in ['nome', 'email', 'telefone']
        }