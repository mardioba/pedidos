from django import forms
from .models import Produto, Cliente, ItemPedido, Pedido

class ProdutoForm(forms.ModelForm):
  class Meta:
    model = Produto
    fields = ['nome', 'preco']
class ClienteForm(forms.ModelForm):
  class Meta:
    model = Cliente
    fields = ['nome', 'telefone', 'email']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido', 'produto', 'quantidade', 'preco']