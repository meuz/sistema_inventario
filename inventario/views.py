# inventario/views.py

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

    # REQUISITO 2.1.3: Endpoint para ver el histórico de movimientos de un producto
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        producto = self.get_object()
        movimientos = Movimiento.objects.filter(producto=producto).order_by('-fecha')
        serializer = MovimientoSerializer(movimientos, many=True)
        return Response(serializer.data)

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

    # REQUISITO 2.1.3: Lógica para sumar o restar stock
    def perform_create(self, serializer):
        movimiento = serializer.save()
        producto = movimiento.producto
        cantidad = movimiento.cantidad

        if movimiento.tipo == 'ENTRADA':
            producto.stock += cantidad
        elif movimiento.tipo in ['SALIDA', 'MERMA']:
            # La validación ya se hizo en el serializer, aquí solo ejecutamos la resta
            producto.stock -= cantidad
        
        producto.save()