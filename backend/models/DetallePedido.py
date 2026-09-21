"""Clase DetallePedido: una linea individual dentro de un pedido."""


class DetallePedido:
    """Representa la compra de un producto especifico en cantidad determinada.

    Une el Pedido con el Producto: cada detalle guarda la referencia al objeto
    Producto y el precio unitario con el que se cobro en ese momento.
    """

    def __init__(self, producto, cantidad, precio_unitario=None, id=None):
        """Constructor: recibe un objeto Producto y la cantidad a comprar.

        Si no se indica precio_unitario, se toma el precio de venta actual
        del producto (uso de objetos: se lee un dato de otro objeto).
        """
        self._id = id
        self._producto = producto
        self._cantidad = cantidad
        if precio_unitario is None:
            precio_unitario = producto.get_precio_venta()
        self._precio_unitario = precio_unitario

    def get_id(self):
        """Retorna el identificador del detalle."""
        return self._id

    def get_producto(self):
        """Retorna el objeto Producto asociado a este detalle."""
        return self._producto

    def get_cantidad(self):
        """Retorna la cantidad de unidades solicitadas."""
        return self._cantidad

    def set_cantidad(self, valor):
        """Asigna la cantidad solo si el valor es mayor que cero."""
        if valor > 0:
            self._cantidad = valor

    def get_precio_unitario(self):
        """Retorna el precio unitario congelado para este detalle."""
        return self._precio_unitario

    def calcular_subtotal(self):
        """Retorna un valor numerico: cantidad por precio unitario.

        Si la cantidad no es valida (menor o igual a cero), retorna cero.
        """
        if self._cantidad > 0:
            return round(self._cantidad * self._precio_unitario, 2)
        return 0.0

    def __str__(self):
        """Representacion en texto del detalle."""
        return f"{self._cantidad} x {self._producto.get_nombre()}"