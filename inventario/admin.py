from django.contrib import admin
from .models import Categoria, Proveedor, Producto, Movimiento, Bodega

#Personalización para el modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sku', 'stock_actual', 'categoria', 'proveedor') #Campos a mostrar
    search_fields = ('nombre', 'sku') #Campos por los que se puede buscar
    list_filter = ('categoria', 'proveedor') #Filtros en la barra lateral

#Registro de los otros modelos (sin personalización avanzada)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Movimiento)
admin.site.register(Bodega)
