from django.db import models
from django.conf import settings  # para usar AUTH_USER_MODEL
from django.contrib.auth.models import User  # opcional si usas directamente User

class Flor(models.Model):
    CATEGORIAS = [
        ('rosas', 'Rosas'),
        ('tulipanes', 'Tulipanes'),
        ('girasoles', 'Girasoles'),
        ('mix', 'Mix de flores'),
        ('especial', 'Edición Especial'),
        ('otros', 'Otros'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to='flores/', blank=True, null=True)

    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='otros')
    disponible = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    identificacion = models.CharField(max_length=50, blank=True, null=True)  # campo opcional
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    flor = models.ForeignKey(Flor, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.flor.nombre} (Pedido #{self.pedido.id})"

class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    flor = models.ForeignKey(Flor, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.flor.nombre} (Carrito de {self.carrito.usuario.username})"

class Variedad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Color(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Material(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre