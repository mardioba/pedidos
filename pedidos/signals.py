from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import ItemPedido

@receiver(post_save, sender=ItemPedido)
@receiver(post_delete, sender=ItemPedido)
def atualizar_total(sender, instance, **kwargs):
    pedido = instance.pedido
    pedido.atualizar_total()


@receiver(pre_save, sender=ItemPedido)
def calcular_preco_total(sender, instance, **kwargs):
    if not instance.preco:  # Verificar se o preço já foi definido
        preco_produto = instance.produto.preco
        quantidade = instance.quantidade
        preco_total = preco_produto * quantidade
        instance.preco = preco_total