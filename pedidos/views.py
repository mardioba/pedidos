from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Produto, Cliente, ItemPedido, Pedido
from .forms import ProdutoForm, ClienteForm, ItemPedidoForm, PedidoForm
from decimal import Decimal
from django.db.models import Sum
from django.views.generic import View
from django.forms.models import inlineformset_factory
from django.db import transaction
def home(request):
  return render(request, 'home.html')

def CadastrarCliente(request):
  form = ClienteForm()
  if request.method == 'GET':
    print('GET')
    return render(request, 'cliente/CadastrarCliente.html', {'form': form})
  if request.method == 'POST':
    print('POST')
    form = ClienteForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('listarcliente')
  return render(request, 'cliente/CadastrarCliente.html', {'form': form})

def Listarclientes(request):
  clientes = Cliente.objects.all()
  return render(request, 'cliente/ListarCliente.html', {'clientes': clientes})

def ExcluirCliente(request, id):
  cliente = Cliente.objects.get(id=id)
  cliente.delete()
  # return redirect('listarcliente')
  return HttpResponse(f'Excluido {cliente} com sucesso!')

def EditarCliente(request, id):
  cliente = Cliente.objects.get(id=id)
  form = ClienteForm(instance=cliente)
  if request.method == 'GET':
    print('GET')
    return render(request, 'cliente/EditarCliente.html', {'form': form})
  if request.method == 'POST':
    print('POST')
    form = ClienteForm(request.POST, instance=cliente)
    if form.is_valid():
      form.save()
      return redirect('listarcliente')

########## Produtos ##########
def CadastrarProduto(request):
  form = ProdutoForm()
  if request.method == 'GET':
    return render(request, 'produto/CadastrarProduto.html', {'form': form})
  if request.method == 'POST':
    form = ProdutoForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('listarproduto')
  return render(request, 'produto/CadastrarProduto.html', {'form': form})

def ListarProdutos(request):
  produtos = Produto.objects.all()
  clientes = Cliente.objects.all()
  return render(request, 'produto/ListarProduto.html', {'produtos': produtos, 'clientes': clientes})

def ExcluirProduto(request, id):
  produto = Produto.objects.get(id=id)
  produto.delete()
  return HttpResponse(f'Excluido com sucesso!')
def EditarProduto(request, id):
  produto = Produto.objects.get(id=id)
  form = ProdutoForm(instance=produto)
  if request.method == 'GET':
    return render(request, 'produto/EditarProduto.html', {'form': form})
  if request.method == 'POST':
    form = ProdutoForm(request.POST, instance=produto)
    if form.is_valid():
      form.save()
      return redirect('listarproduto')
##### Pedidos ####

def criar_pedido(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        selected_products = request.POST.getlist('selected_products[]')
        total = 0
        
        if cliente_id is None:
            return HttpResponse('ID do cliente não fornecido.')

        # Criar o pedido
        pedido = Pedido.objects.create(cliente_id=cliente_id, total=total)

        # Adicionar itens ao pedido
        for item in selected_products:
            produto_id, quantidade = item.split(':')
            produto_id = int(produto_id)
            quantidade = int(quantidade)
            produto = Produto.objects.get(pk=produto_id)
            preco = produto.preco
            total += produto.preco * quantidade
            ItemPedido.objects.create(pedido=pedido, produto=produto, quantidade=quantidade, preco=preco)

        # Atualizar o total do pedido
        pedido.total = total
        pedido.save()

        # return HttpResponse('Pedido criado com sucesso!')
        return redirect('listarpedidos')
    else:
        return HttpResponse('Método não permitido!')

def ListarPedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/ListarPedidos.html', {'pedidos': pedidos})

def PedidoDetalhes(request, id):
    itens = ItemPedido.objects.filter(pedido=id)
    cliente = Pedido.objects.get(id=id).cliente
    data = Pedido.objects.get(id=id).datacreation
    total = Decimal(0)
    pedido = str(id).zfill(5)
    for item in itens:
        item.total = item.quantidade * item.produto.preco
        total += item.total
    context = {'itens': itens, 'total': total, 'data': data, 'cliente': cliente, 'pedido': pedido, 'id': id}
    return render(request, 'pedido/PedidoDetalhes.html', context)

def criarPedidos(request):
  produtos = Produto.objects.all()
  clientes = Cliente.objects.all()
  return render(request, 'pedido/criarPedidos.html', {'produtos': produtos, 'clientes': clientes})

def pedidos_por_cliente(request):
    # Agrupando os pedidos por cliente e calculando o total de cada cliente
    pedidos_por_cliente = Pedido.objects.values('cliente__id','cliente__nome').annotate(total_pedido=Sum('total'))

    return render(request, 'pedido/pedidos_por_cliente.html', {'pedidos_por_cliente': pedidos_por_cliente})

def detalhar_pedidos_por_cliente(request, cliente_id):
    pedidos = Pedido.objects.filter(cliente_id=int(cliente_id))
    total = Decimal(0)
    for item in pedidos:
        total = total + item.total
    context = {
      'pedidos': pedidos,
      'total': total
      }
    return render(request, 'pedido/detalhar_pedidos_por_cliente.html', context)
    
class PedidoEditView(View):
    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedido/editar_pedido.html', {'form': form, 'pedido': pedido})

    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()

            # Atualizar o total do pedido
            pedido.atualizar_total()
            
            return redirect('detalhes_pedido', pedido_id=pedido_id)
        return render(request, 'pedido/editar_pedido.html', {'form': form, 'pedido': pedido})

class ItemPedidoEditView(View):
    def get(self, request, item_pedido_id):
        item_pedido = get_object_or_404(ItemPedido, pk=item_pedido_id)
        form = ItemPedidoForm(instance=item_pedido)
        return render(request, 'pedido/editar_item_pedido.html', {'form': form, 'item_pedido': item_pedido})

    def post(self, request, item_pedido_id):
        item_pedido = get_object_or_404(ItemPedido, pk=item_pedido_id)
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            form.save()

            # Atualizar o total do pedido
            item_pedido.pedido.atualizar_total()
            
            return redirect('pedidodetalhes', pedido_id=item_pedido.pedido_id)
        return render(request, 'pedido/editar_item_pedido.html', {'form': form, 'item_pedido': item_pedido})

class PedidoDeleteView(View):
    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        return render(request, 'pedido/excluir_pedido.html', {'pedido': pedido})

    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        pedido.delete()
        return redirect('listarpedidos')

class ItemPedidoEditView(View):
    def get(self, request, item_pedido_id):
        item_pedido = get_object_or_404(ItemPedido, pk=item_pedido_id)
        form = ItemPedidoForm(instance=item_pedido)
        return render(request, 'pedido/editar_item_pedido.html', {'form': form, 'item_pedido': item_pedido})

    def post(self, request, item_pedido_id):
        item_pedido = get_object_or_404(ItemPedido, pk=item_pedido_id)
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            form.save()
            item_pedido.pedido.atualizar_total()  # Atualizar o total do pedido
            return redirect('pedidodetalhes', id=item_pedido.pedido_id)  # Correção aqui
        return render(request, 'pedido/editar_item_pedido.html', {'form': form, 'item_pedido': item_pedido})

class ItemPedidoDeleteView(View):
    def get(self, request, item_pedido_id):
        item_pedido = get_object_or_404(ItemPedido, pk=item_pedido_id)
        return render(request, 'pedido/excluir_item_pedido.html', {'item_pedido': item_pedido})

    def post(self, request, item_pedido_id):
        item_pedido = get_object_or_404(ItemPedido, pk=item_pedido_id)
        pedido_id = item_pedido.pedido_id
        item_pedido.delete()

        # Atualizar o total do pedido
        item_pedido.pedido.atualizar_total()

        return redirect('pedidodetalhes', id=pedido_id)

#### InlineTabular
@transaction.atomic
def inserir(request):
    if request.method == 'GET':
        form = PedidoForm()
        form_pedidoitem_factory = inlineformset_factory(Pedido, ItemPedido, form=ItemPedidoForm, extra=1)
        form_pedidoitem = form_pedidoitem_factory()
        context = {
            'form': form,
            'form_pedidoitem': form_pedidoitem
        }
        return render(request, 'pedido/add_form.html', context)
    elif request.method == 'POST':
        form = PedidoForm(request.POST)
        form_pedidoitem_factory = inlineformset_factory(Pedido, ItemPedido, form=ItemPedidoForm)
        form_pedidoitem = form_pedidoitem_factory(request.POST)
        if form.is_valid() and form_pedidoitem.is_valid():
            pedido = form.save(commit=False)  # Salvando o pedido sem commit

            pedido.save()  # Salvando o pedido para gerar um ID
            
            form_pedidoitem.instance = pedido
            form_pedidoitem.save()  # Salvando os itens do pedido

            return redirect('listarpedidos')
        else:
            context = {
                'form': form,
                'form_pedidoitem': form_pedidoitem,
            }
            return render(request, 'pedido/add_form.html', context)