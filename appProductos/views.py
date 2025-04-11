from django.shortcuts import render
from django.http import JsonResponse
from .models import Categoria, Producto, Carrito
import json
# Create your views here.

def verCategoria(request):
    listCateg = Categoria.objects.all() ## === SELECT * FROM Categoria; Asi seria la consulta SQL

    context = {
        'categorias' : listCateg,
        'titulo' : 'Categorias de Productos del Ecommerce'
    }

    return render(request, 'productos/categorias.html', context)


def verProductosCategoria(request, idCategoria):
    idCat = int(idCategoria)
    nombreCat = Categoria.objects.get(id=idCat)
    listaProducto = Producto.objects.filter(categoria = idCat)

    context = {
        'productos' : listaProducto,
        'titulo' : str(nombreCat)
    }

    return render(request, 'productos/productos.html', context)

def verProducto(request, idProd, msj=None):
    idProd = int(idProd)
    regProducto = Producto.objects.get(id=idProd)

    context = {
        'producto' : regProducto,
        'titulo' : f'Detalles de {str(regProducto.nombre)}'
    }

    if msj:
        context['mensaje'] = msj

    return render(request, 'productos/producto.html', context)


def agregarCarrito(request, idProd):
    idProd = int(idProd)
    regUsuario = request.user
    msj = None

    existe = Producto.objects.filter(id=idProd).exists()
    if existe:
        regProducto = Producto.objects.get(id=idProd)

        existe = Carrito.objects.filter(producto=regProducto, estado= 'activo', usuario=regUsuario).exists()

        if existe:
            regCarro = Carrito.objects.get(producto=regProducto, estado='activo', usuario=regUsuario)
            regCarro.cantidad += 1
        else:
            regCarro = Carrito(producto=regProducto, usuario = regUsuario, valUnit = regProducto.precioUnitario)

        regCarro.save()

    else:
        msj = 'Producto no disponible'

    return verProducto(request, idProd, msj)

def verCarrito(request):
    context = consultarCarrito(request)
    return render(request, 'productos/carrito.html', context)

def eliminarCarrito(request,id): 
    regCarrito = Carrito.objects.get(id=id)
    regCarrito.estado = 'anulado'

    regCarrito.save()

    return verCarrito(request)

def cambiarCantidad(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            id = data.get('id')
            cantidad = int(data.get('cantidad'))
            if cantidad > 0:
                regProducto = Carrito.objects.get(id=id)
                regProducto.cantidad = cantidad
                regProducto.save()

            # Contexto actualizado
            context = consultarCarrito(request)
            return JsonResponse(context)
        return JsonResponse({'alarma': 'No se pudo modificar...'}, status=400)
    else:
        return verCarrito(request)
    
def consultarCarrito(request):
    if not request.user.is_authenticated:
        return {
            'titulo' : 'Carrito vacio',
            'carrito': [],
            'subtotal': 0,
            'iva': 0,
            'envio': 0,
            'total': 0,
        }
    regUsuario = request.user

    listaCarrito = Carrito.objects.filter(usuario=regUsuario, estado='activo').values('id', 'cantidad', 'valUnit', 'producto__nombre', 'producto__unidad', 'producto__id')

    listado = []
    subtotal = 0
    for prod in listaCarrito:
        reg = {
            'id' : prod['id'],
            'cantidad' : prod['cantidad'],
            'valUnit' : prod['valUnit'],
            'nombre' : prod['producto__nombre'],
            'unidad' : prod['producto__unidad'],
            'total' : prod['valUnit'] * prod['cantidad'],
            'prodId' : prod['producto__id']
        }

        subtotal += prod['cantidad'] * prod['valUnit']

        listado.append(reg)

    envio = 8000
    if len(listado) == 0:
        envio = 0

    context = {
        'titulo' : 'Producto en el carrito de compras',
        'carrito' : listado,
        'subtotal' : subtotal,
        'iva' : 0.19 * int(subtotal),
        'envio' : envio,
        'total' : int(subtotal) * 1.19 + envio      
    }

    return context