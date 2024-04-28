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
  total = models.DecimalField(max_digits=8, decimal_places=2)
  datacreation = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.cliente)
  
  def atualizar_total(self):
      total_pedido = sum(item.quantidade * item.preco for item in self.itempedidos_set.all())
      self.total = total_pedido
      self.save()

class ItemPedido(models.Model):
  pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
  produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
  quantidade = models.IntegerField()
  preco = models.DecimalField(max_digits=8, decimal_places=2)
  
  def __str__(self):
    return str(self.pedido.pk)