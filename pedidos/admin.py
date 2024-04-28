from django.contrib import admin
from .models import Cliente, Produto, ItemPedido, Pedido

class PedidoAdmin(admin.ModelAdmin):
  list_display = ('id','cliente', 'total', 'datacreation')


admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(ItemPedido)
admin.site.register(Pedido, PedidoAdmin)
