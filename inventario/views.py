from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria, Proveedor, Producto, Movimiento
from .serializers import CategoriaSerializer, ProveedorSerializer, ProductoSerializer, MovimientoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        producto = self.get_object()
        movimientos = Movimiento.objects.filter(producto=producto).order_by('-fecha')
        serializer = MovimientoSerializer(movimientos, many=True)
        return Response(serializer.data)

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

    def perform_create(self, serializer):
        movimiento = serializer.save()
        producto = movimiento.producto
        cantidad = movimiento.cantidad

        if movimiento.tipo == 'ENTRADA':
            producto.stock += cantidad
        elif movimiento.tipo in ['SALIDA', 'MERMA']:
            producto.stock -= cantidad
        
        producto.save()