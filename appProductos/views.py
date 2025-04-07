from django.shortcuts import render
from .models import Categoria, Producto
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

