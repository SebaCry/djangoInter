from django.db import models

class Categoria(models.Model):
    descripCategoria = models.CharField(max_length=45)
    

    def __str__(self):
        return self.descripCategoria
    
    class Meta:
        verbose_name = 'categorias'
        verbose_name_plural = 'categorias de productos'

class Producto(models.Model):
    nombre = models.CharField(max_length=45, null=False)
    descripcion = models.TextField(max_length=300, null=True)
    precioUnitario = models.DecimalField(max_digits=8, decimal_places=2)
    unidad = models.CharField(max_length=10, null=False)
    existencia = models.IntegerField(null=True)
    imgGrande = models.ImageField(upload_to='iconos', null=True)
    imgPeque = models.ImageField(upload_to='iconos', null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=False)

    def __str__(self): ## El método ‘ str ()’ es utilizado para definir que atributos (columnas) mostrar cuando se esté desplegando un objeto (fila)
        return self.nombre
    


# Create your models here.
