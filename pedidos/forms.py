from django import forms
from .models import Produto, Cliente, ItemPedidos, Pedidos

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
        model = Pedidos
        fields = ['cliente']

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedidos
        fields = ['pedido', 'produto', 'quantidade', 'preco']