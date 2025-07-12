from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('carrito/agregar/<int:flor_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('contacto/', views.contacto, name='contacto'),
    path('checkout/', views.realizar_pedido, name='realizar_pedido'),
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/pago/', views.proceder_pago, name='proceder_pago'),
    path('pago/exito/', views.pago_exito, name='pago_exito'),
    path('pago/error/', views.pago_error, name='pago_error'),
    path('pago/pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('cumpleanos/', views.cumpleanos, name='cumpleanos'),
    path('ocasiones/', views.ocasiones, name='ocasiones'),
    path('flores/', views.flores, name='flores'),
    path('rosas/', views.rosas, name='rosas'),
    path('funeral/', views.funeral, name='funeral'),
    path('plantas/', views.plantas, name='plantas'),
]
