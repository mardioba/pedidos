from django.contrib import admin
from .models import Cliente, Produto, ItemPedidos, Pedidos

class PedidoAdmin(admin.ModelAdmin):
  list_display = ('id','cliente', 'total', 'datacreation')


admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(ItemPedidos)
admin.site.register(Pedidos, PedidoAdmin)
