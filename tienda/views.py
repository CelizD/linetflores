from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import mercadopago
from django.urls import reverse
from .models import Flor, Carrito, CarritoItem, Pedido
from .forms import ContactoForm, PedidoForm
from django.shortcuts import render
from .models import Variedad, Color, Material

def inicio(request):
    flores = Flor.objects.all()
    return render(request, 'tienda/inicio.html', {'flores': flores})


@login_required
def agregar_al_carrito(request, flor_id):
    if request.method == 'POST':
        flor = get_object_or_404(Flor, id=flor_id)
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        item, created = CarritoItem.objects.get_or_create(carrito=carrito, flor=flor)
        if not created:
            item.cantidad += 1
            item.save()
    return redirect('inicio')


@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    for item in items:
        item.subtotal = item.flor.precio * item.cantidad  # subtotal calculado manualmente
    total = sum(item.subtotal for item in items)
    return render(request, 'tienda/carrito.html', {'items': items, 'total': total})


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            send_mail(
                subject=f"Mensaje de {nombre}",
                message=mensaje,
                from_email=email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return render(request, 'tienda/contacto_exito.html', {'nombre': nombre})
    else:
        form = ContactoForm()
    return render(request, 'tienda/contacto.html', {'form': form})


@login_required
def realizar_pedido(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    items = carrito.items.all() if carrito else []
    total = sum(item.flor.precio * item.cantidad for item in items)

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            Pedido.objects.create(
                usuario=request.user,
                nombre=form.cleaned_data['nombre'],
                direccion=form.cleaned_data['direccion'],
                correo=form.cleaned_data['correo'],
                telefono=form.cleaned_data['telefono'],
                identificacion=form.cleaned_data.get('identificacion', '')  # Guardar el nuevo campo
            )
            carrito.items.all().delete()  # Vacía el carrito
            return render(request, 'tienda/pedido_exito.html')
    else:
        form = PedidoForm()

    return render(request, 'tienda/checkout.html', {'form': form, 'items': items, 'total': total})


@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-creado_en')
    return render(request, 'tienda/pedidos.html', {'pedidos': pedidos})


@login_required
def vaciar_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    if carrito:
        carrito.items.all().delete()
    return redirect('ver_carrito')


@login_required
def proceder_pago(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito or carrito.items.count() == 0:
        return redirect('ver_carrito')

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    items = []
    for item in carrito.items.all():
        items.append({
            "title": item.flor.nombre,
            "quantity": int(item.cantidad),
            "currency_id": "MXN",
            "unit_price": float(item.flor.precio),
        })

    # ✅ back_urls corregidos (sin acentos)
    preference_data = {
    "items": items,
    "back_urls": {
        "success": request.build_absolute_uri('/pago/exito/'),
        "failure": request.build_absolute_uri('/pago/error/'),
        "pending": request.build_absolute_uri('/pago/pendiente/'),
    },
    "auto_return": "approved",
}


    # Crear preferencia en MercadoPago
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response.get("response", {})

    # Validar si hubo error
    if "id" not in preference:
        print("Error en preferencia de MercadoPago:", preference)
        return render(request, "tienda/pago_error.html", {
            "mensaje": preference.get("message", "Error al generar el pago.")
        })

    return render(request, "tienda/proceder_pago.html", {
        "preference_id": preference["id"],
        "public_key": settings.MERCADOPAGO_PUBLIC_KEY,
    })




def pago_exito(request):
    pedido_reciente = Pedido.objects.filter(usuario=request.user).order_by('-creado_en').first()
    return render(request, "tienda/pago_exito.html", {
        "pedido_id": pedido_reciente.id if pedido_reciente else None
    })


def pago_error(request):
    return render(request, "tienda/pago_error.html")


def pago_pendiente(request):
    pedido_reciente = Pedido.objects.filter(usuario=request.user).order_by('-creado_en').first()
    return render(request, "tienda/pago_pendiente.html", {
        "pedido_id": pedido_reciente.id if pedido_reciente else None
    })


def cumpleanos(request):
    return render(request, 'tienda/categorias/cumpleanos.html')

def ocasiones(request):
    return render(request, 'tienda/categorias/ocasiones.html')

def flores(request):
    return render(request, 'tienda/categorias/flores.html')

def rosas(request):
    return render(request, 'tienda/categorias/rosas.html')

def funeral(request):
    return render(request, 'tienda/categorias/funeral.html')

def plantas(request):
    return render(request, 'tienda/categorias/plantas.html')

def inicio(request):
    variedades = Variedad.objects.all()
    colores = Color.objects.all()
    materiales = Material.objects.all()
    precios = [
        "Menos de $100",
        "$100 - $500",
        "Más de $500"
    ]
    longitudes = [
        "Menos de 20 cm",
        "20 cm - 50 cm",
        "Más de 50 cm"
    ]

    flores = Flor.objects.all()

    # Filtros desde GET
    variedad_id = request.GET.get('variedad')
    color_id = request.GET.get('color')
    material_id = request.GET.get('material')
    precio_rango = request.GET.get('precio')
    longitud_rango = request.GET.get('longitud')

    if variedad_id:
        flores = flores.filter(variedad_id=variedad_id)

    if color_id:
        flores = flores.filter(color_id=color_id)

    if material_id:
        flores = flores.filter(material_id=material_id)

    if precio_rango:
        if precio_rango == "Menos de $100":
            flores = flores.filter(precio__lt=100)
        elif precio_rango == "$100 - $500":
            flores = flores.filter(precio__gte=100, precio__lte=500)
        elif precio_rango == "Más de $500":
            flores = flores.filter(precio__gt=500)

    if longitud_rango:
        # Suponiendo que Flor tiene campo longitud en cm
        if longitud_rango == "Menos de 20 cm":
            flores = flores.filter(longitud__lt=20)
        elif longitud_rango == "20 cm - 50 cm":
            flores = flores.filter(longitud__gte=20, longitud__lte=50)
        elif longitud_rango == "Más de 50 cm":
            flores = flores.filter(longitud__gt=50)

    context = {
        'variedades': variedades,
        'colores': colores,
        'materiales': materiales,
        'precios': precios,
        'longitudes': longitudes,
        'flores': flores,
        'filtros_seleccionados': {
            'variedad': variedad_id,
            'color': color_id,
            'material': material_id,
            'precio': precio_rango,
            'longitud': longitud_rango,
        }
    }
    return render(request, 'tienda/inicio.html', context)