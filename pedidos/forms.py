from django import forms
from .models import Produto, Cliente

class ProdutoForm(forms.ModelForm):
  class Meta:
    model = Produto
    fields = ['nome', 'preco']
class ClienteForm(forms.ModelForm):
  class Meta:
    model = Cliente
    fields = ['nome', 'telefone', 'email']