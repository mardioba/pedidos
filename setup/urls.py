"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
]
