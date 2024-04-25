from django.contrib import admin
from django.urls import path
from pedidos import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cadastrarcliente/', views.CadastrarCliente, name='cadastrarcliente'),
    path('listarcliente/', views.Listarclientes, name='listarcliente'),
    path('excluircliente/<int:id>', views.ExcluirCliente, name='excluircliente'),
    path('cadastrarproduto/', views.CadastrarProduto, name='cadastrarproduto'),
    path('listarproduto/', views.ListarProdutos, name='listarproduto'),
    path('excluirproduto/<int:id>', views.ExcluirProduto, name='excluirproduto'),
    path('atualizarcliente/<int:id>', views.EditarCliente, name='atualizarcliente'),
    path('atualizarproduto/<int:id>', views.EditarProduto, name='atualizarproduto'),
    path('processar_formulario/', views.criar_pedido, name='processar_formulario'),
    path('criarpedido/', views.criarPedidos, name='criarpedido'),
    path('listarpedidos/', views.ListarPedidos, name='listarpedidos'),
    path('pedidodetalhes/<int:id>', views.PedidoDetalhes, name='pedidodetalhes'),
    path('pedidosporcliente', views.pedidos_por_cliente, name='pedidosporcliente'),
    path('detalhar_pedidos_por_cliente/<int:cliente_id>', views.detalhar_pedidos_por_cliente, name='detalhar_pedidos_por_cliente'),
]
