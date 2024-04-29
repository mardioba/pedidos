from typing import Any
from django.db import models

class Produto(models.Model):
  nome = models.CharField(max_length=100)
  preco = models.DecimalField(max_digits=8, decimal_places=2)

  def __str__(self):
    return self.nome

class Cliente(models.Model):
  nome = models.CharField(max_length=100)
  telefone = models.CharField(max_length=20)
  email = models.EmailField()

  def __str__(self):
    return self.nome
  
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    datacreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cliente)

    def atualizar_total(self):
        total_pedido = sum(item.preco * item.quantidade for item in self.itens_pedido.all())
        self.total = total_pedido
        self.save(update_fields=['total'])


class ItemPedido(models.Model):
    # pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens_pedido')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Se for um novo item de pedido
            self.preco = self.produto.preco
        super().save(*args, **kwargs)
# class ItemPedido(models.Model):
#   pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
#   produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
#   quantidade = models.IntegerField()
#   preco = Produto.preco()
  
#   def __str__(self):
#     return str(self.pedido.pk)