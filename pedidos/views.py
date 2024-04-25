from django.shortcuts import render, HttpResponse, redirect
from .models import Produto, Cliente
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
  return render(request, 'produto/ListarProduto.html', {'produtos': produtos})

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