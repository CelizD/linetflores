from django.contrib import admin
from .models import Pedido, PedidoItem, Flor, Carrito, CarritoItem, Variedad, Color, Material
from import_export import resources
from import_export.admin import ImportExportModelAdmin


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'nombre', 'correo', 'telefono', 'identificacion', 'creado_en')
    search_fields = ('usuario__username', 'nombre', 'correo', 'identificacion')
    list_filter = ('creado_en',)

admin.site.register(PedidoItem)
admin.site.register(Carrito)
admin.site.register(CarritoItem)
admin.site.register(Variedad)
admin.site.register(Color)
admin.site.register(Material)

# Crear el recurso
class FlorResource(resources.ModelResource):
    class Meta:
        model = Flor

# Registrar en el admin con import-export
@admin.register(Flor)
class FlorAdmin(ImportExportModelAdmin):
    resource_class = FlorResource
    list_display = ('nombre', 'precio', 'categoria', 'disponible', 'stock')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre', 'descripcion')

    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'imagen')
        }),
        ('Información de inventario', {
            'fields': ('precio', 'categoria', 'disponible', 'stock'),
            'classes': ('collapse',),  # opcional para que se pliegue
        }),
    )

