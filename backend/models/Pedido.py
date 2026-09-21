"""Clase Pedido: agrupa detalle de pedidos que un cliente realiza en la tienda."""

from backend.models.DetallePedido import DetallePedido


class Pedido:
    """Representa un pedido realizado por un cliente.

    Recibe un objeto Cliente como parametro (uso de objetos), contiene una
    lista de objetos DetallePedido y evoluciona entre estados validos.
    """

    ESTADOS_VALIDOS = ["Pendiente", "Confirmado", "Entregado", "Cancelado"]

    def __init__(self, cliente, fecha, estado="Pendiente", id=None):
        """Constructor: recibe un objeto Cliente y la fecha del pedido."""
        self._id = id
        self._cliente = cliente
        self._fecha = fecha
        self._estado = estado
        self._detalles = []

    def get_id(self):
        """Retorna el identificador del pedido."""
        return self._id

    def get_cliente(self):
        """Retorna el objeto Cliente asociado a este pedido."""
        return self._cliente

    def get_fecha(self):
        """Retorna la fecha en la que se realizo el pedido."""
        return self._fecha

    def get_estado(self):
        """Retorna el estado actual del pedido."""
        return self._estado

    def get_detalles(self):
        """Retorna la lista de objetos DetallePedido del pedido."""
        return self._detalles

    def agregar_producto(self, producto, cantidad):
        """Agrega un producto al pedido y retorna un valor logico.

        Recibe un objeto Producto y la cantidad; si hay stock disponible se
        crea un objeto DetallePedido y se agrega a la lista.
        """
        if producto.hay_stock_disponible(cantidad):
            detalle = DetallePedido(producto, cantidad)
            self._detalles.append(detalle)
            return True
        return False

    def confirmar(self):
        """Confirma el pedido, descuenta stock y retorna un valor logico.

        Solo se puede confirmar un pedido en estado Pendiente y con al menos
        un detalle. Al confirmar, cada producto baja su existencia.
        """
        if self._estado == "Pendiente" and len(self._detalles) > 0:
            for detalle in self._detalles:
                detalle.get_producto().actualizar_stock(detalle.get_cantidad())
            self._estado = "Confirmado"
            return True
        return False

    def calcular_total(self):
        """Retorna un valor numerico: el total del pedido.

        Si el cliente es frecuente, se aplica un descuento del 5 por ciento
        sobre el total (condicion sobre los puntos del cliente).
        """
        total = 0.0
        for detalle in self._detalles:
            total = total + detalle.calcular_subtotal()
        if self._cliente.es_cliente_frecuente():
            total = total * 0.95
        return round(total, 2)

    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado del pedido y retorna un valor logico.

        Solo acepta estados validos distintos del estado actual.
        """
        if nuevo_estado in self.ESTADOS_VALIDOS and nuevo_estado != self._estado:
            self._estado = nuevo_estado
            return True
        return False

    def cantidad_total_items(self):
        """Retorna un valor numerico entero: la suma de unidades del pedido."""
        total = 0
        for detalle in self._detalles:
            total = total + detalle.get_cantidad()
        return total

    def __str__(self):
        """Representacion en texto del pedido."""
        return f"Pedido de {self._cliente.get_nombre()} ({self._estado})"