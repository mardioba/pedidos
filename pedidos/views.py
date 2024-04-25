from django.shortcuts import render, HttpResponse, redirect
from .models import Produto, Cliente, ItemPedidos, Pedidos
from .forms import ProdutoForm, ClienteForm
from decimal import Decimal
from django.db.models import Sum
# Create your views here.
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
        pedido = Pedidos.objects.create(cliente_id=cliente_id, total=total)

        # Adicionar itens ao pedido
        for item in selected_products:
            produto_id, quantidade = item.split(':')
            produto_id = int(produto_id)
            quantidade = int(quantidade)
            produto = Produto.objects.get(pk=produto_id)
            preco = produto.preco
            total += produto.preco * quantidade
            ItemPedidos.objects.create(pedido=pedido, produto=produto, quantidade=quantidade, preco=preco)

        # Atualizar o total do pedido
        pedido.total = total
        pedido.save()

        # return HttpResponse('Pedido criado com sucesso!')
        return redirect('listarpedidos')
    else:
        return HttpResponse('Método não permitido!')

def ListarPedidos(request):
    pedidos = Pedidos.objects.all()
    return render(request, 'pedido/ListarPedidos.html', {'pedidos': pedidos})

def PedidoDetalhes(request, id):
    itens = ItemPedidos.objects.filter(pedido=id)
    cliente = Pedidos.objects.get(id=id).cliente
    data = Pedidos.objects.get(id=id).datacreation
    total = Decimal(0)
    pedido = str(id).zfill(5)
    for item in itens:
        item.total = item.quantidade * item.produto.preco
        total += item.total
    context = {'itens': itens, 'total': total, 'data': data, 'cliente': cliente, 'pedido': pedido}
    return render(request, 'pedido/PedidoDetalhes.html', context)

def criarPedidos(request):
  produtos = Produto.objects.all()
  clientes = Cliente.objects.all()
  return render(request, 'pedido/criarPedidos.html', {'produtos': produtos, 'clientes': clientes})

def pedidos_por_cliente(request):
    # Agrupando os pedidos por cliente e calculando o total de cada cliente
    pedidos_por_cliente = Pedidos.objects.values('cliente__id','cliente__nome').annotate(total_pedido=Sum('total'))

    return render(request, 'pedido/pedidos_por_cliente.html', {'pedidos_por_cliente': pedidos_por_cliente})

def detalhar_pedidos_por_cliente(request, cliente_id):
    pedidos = Pedidos.objects.filter(cliente_id=int(cliente_id))
    total = Decimal(0)
    for item in pedidos:
        total = total + item.total
    context = {
      'pedidos': pedidos,
      'total': total
      }
    return render(request, 'pedido/detalhar_pedidos_por_cliente.html', context)
    
  