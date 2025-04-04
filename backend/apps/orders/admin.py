from django.contrib import admin
from .models import Pedido, DetallePedido, PedidoMesero, Pago

# Register your models here.
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(PedidoMesero)
admin.site.register(Pago)
