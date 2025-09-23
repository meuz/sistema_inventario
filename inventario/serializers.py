from rest_framework import serializers
from .models import Categoria, Proveedor, Producto, Movimiento

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'

    def validate(self, data):
        producto = data['producto']
        cantidad = data['cantidad']
        tipo = data['tipo']

        if tipo in ['SALIDA', 'MERMA'] and producto.stock < cantidad:
            raise serializers.ValidationError(f"Stock insuficiente. Stock actual: {producto.stock}, se intenta restar: {cantidad}")
        return data