from django.shortcuts import render, HttpResponse, redirect
from .models import Produto, Cliente, ItemPedidos, Pedidos
from .forms import ProdutoForm, ClienteForm
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
def ProcessarFormulario(request):
  return HttpResponse('Processando formulário...')

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
            total += produto.preco * quantidade
            ItemPedidos.objects.create(pedido=pedido, produto=produto, quantidade=quantidade)

        # Atualizar o total do pedido
        pedido.total = total
        pedido.save()

        return HttpResponse('Pedido criado com sucesso!')
    else:
        return HttpResponse('Método não permitido!')

def ListarPedidos(request):
    pedidos = Pedidos.objects.all()
    return render(request, 'pedido/ListarPedidos.html', {'pedidos': pedidos})

def PedidoDetalhes(request, id):
    itens = ItemPedidos.objects.filter(pedido=id)
    total = Pedidos.objects.get(id=id).total
    return render(request, 'pedido/PedidoDetalhes.html', {'itens': itens, 'total': total})
    