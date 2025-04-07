from django.contrib import admin
from .models import *

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripCategoria')

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion','precioUnitario')

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
#admin.site.register(Carro, CarroAdmin)

# Register your models here.
