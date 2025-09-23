from django.contrib import admin
from django.urls import path, include
# Importa RedirectView para poder hacer redirecciones
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/inventario/productos/', permanent=False)),

    path('admin/', admin.site.urls),
    path('inventario/', include('inventario.urls')), # Asumo que tienes una línea como esta
]