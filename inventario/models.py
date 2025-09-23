# # inventario/models.py

# from django.db import models

# class Categoria(models.Model):
#     nombre = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.nombre

# class Proveedor(models.Model):
#     nombre = models.CharField(max_length=150)
#     telefono = models.CharField(max_length=20, blank=True)

#     def __str__(self):
#         return self.nombre

# class Producto(models.Model):
#     nombre = models.CharField(max_length=150)
#     sku = models.CharField(max_length=50, unique=True)
#     stock = models.PositiveIntegerField(default=0)
#     categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
#     proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return self.nombre

# class Movimiento(models.Model):
#     TIPO_MOVIMIENTO_CHOICES = [
#         ('ENTRADA', 'Entrada'),
#         ('SALIDA', 'Salida'),
#         ('MERMA', 'Merma'),
#     ]
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
#     cantidad = models.PositiveIntegerField()
#     fecha = models.DateTimeField(auto_now_add=True)
#     descripcion = models.TextField(blank=True)

#     def __str__(self):
#         return f'{self.tipo} - {self.producto.nombre} ({self.cantidad})'

# inventario/models.py

from django.db import models
from django.core.exceptions import ValidationError

# 1. Tabla/Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True) # Campo opcional

    def __str__(self):
        return self.nombre

# 2. Tabla/Modelo Proveedor
class Proveedor(models.Model):
    razon_social = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.razon_social

# 3. Tabla/Modelo Bodega
class Bodega(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

# 4. Tabla/Modelo Producto
class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2) # Campo numérico para precios
    stock_actual = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.nombre} (SKU: {self.sku})'

# 5. Tabla/Modelo Movimiento
class Movimiento(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('MERMA', 'Merma'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.tipo} - {self.producto.nombre} ({self.cantidad})'

    def clean(self):
        # Validación para evitar stock negativo
        if self.tipo in ['SALIDA', 'MERMA']:
            if self.producto.stock_actual < self.cantidad:
                raise ValidationError(f'Stock insuficiente para {self.producto.nombre}. Stock actual: {self.producto.stock_actual}, se intenta restar: {self.cantidad}')

    def save(self, *args, **kwargs):
        self.full_clean() # Llama a la validación antes de guardar
        super().save(*args, **kwargs)
        # Actualizar stock después de guardar el movimiento
        if self.tipo == 'ENTRADA':
            self.producto.stock_actual += self.cantidad
        elif self.tipo in ['SALIDA', 'MERMA']:
            self.producto.stock_actual -= self.cantidad
        self.producto.save()