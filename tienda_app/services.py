import logging
from django.shortcuts import get_object_or_404
from django.db import transaction

from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro, Orden

logger = logging.getLogger('tienda')


class CompraService:
    """
    SERVICE LAYER: Orquesta la interacción entre el dominio,
    la infraestructura y la base de datos.
    """

    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        inventario = Inventario.objects.filter(libro=libro).first()
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {
            "libro": libro,
            "total": round(total, 2),
            "stock": inventario.cantidad if inventario else 0,
        }

    def ejecutar_compra(self, libro_id, cantidad=1, direccion="Sin direccion", usuario=None):
        with transaction.atomic():
            libro = get_object_or_404(Libro, id=libro_id)
            inventario = get_object_or_404(Inventario, libro=libro)

            if inventario.cantidad < cantidad:
                raise ValueError(f"Stock insuficiente. Stock actual: {inventario.cantidad}")

            total = CalculadorImpuestos.obtener_total_con_iva(float(libro.precio) * cantidad)

            # 1. Procesar pago usando la Factory inyectada
            pago_exitoso = self.procesador_pago.pagar(total)
            if not pago_exitoso:
                logger.error(f"[PAGO FALLIDO] Procesador {self.procesador_pago.__class__.__name__}: Monto=${total:.2f}")
                raise Exception("Error al procesar el pago con la pasarela.")

            logger.info(
                f"[PAGO EXITOSO] Procesador: {self.procesador_pago.__class__.__name__} | Monto: ${total:.2f}"
            )

            # 2. Descontar inventario
            inventario.cantidad -= cantidad
            inventario.save()
            logger.info(
                f"[INVENTARIO DESCONTADO] Libro: '{libro.titulo}' (ID: {libro.id}) | Descontados: {cantidad} | Stock restante: {inventario.cantidad}"
            )

            # 3. Registrar Orden
            orden = Orden.objects.create(
                usuario=usuario,
                libro=libro,
                total=total,
                direccion_envio=direccion,
            )
            logger.info(f"[ORDEN REGISTRADA] Orden ID: {orden.id} creada para Libro ID: {libro.id}")

            return round(total, 2)


class CompraRapidaService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago

    def procesar(self, libro_id):
        servicio_compra = CompraService(self.procesador_pago)
        return servicio_compra.ejecutar_compra(libro_id=libro_id, cantidad=1)

        