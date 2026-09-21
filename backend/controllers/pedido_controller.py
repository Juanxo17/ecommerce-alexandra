"""Controlador de pedidos: arma, confirma y consulta pedidos.

Depende de ClienteController y de ProductoController para resolver los
objetos Cliente y Producto a partir de sus identificadores, y del
RepositorioSqlite que traduce los pedidos a filas y viceversa.
"""

from backend.models.Pedido import Pedido


class PedidoController:
    """Controla el ciclo de vida de los objetos Pedido."""

    def __init__(self, repositorio, cliente_controller, producto_controller):
        self._repositorio = repositorio
        self._cliente_controller = cliente_controller
        self._producto_controller = producto_controller

    def crear(self, cliente_id, fecha):
        """Crea un pedido para el cliente indicado y retorna el objeto.

        Retorna None si el cliente no existe o si la fecha esta vacia.
        El pedido nace en estado Pendiente y sin lineas.
        """
        cliente = self._cliente_controller.obtener_por_id(cliente_id)
        if cliente is None:
            return None
        if fecha is None or fecha.strip() == "":
            return None
        pedido = Pedido(cliente=cliente, fecha=fecha, estado="Pendiente")
        return self._repositorio.guardar_pedido(pedido)

    def agregar_producto(self, pedido_id, producto_id, cantidad):
        """Agrega un producto a un pedido pendiente y retorna un valor logico.

        Valida que el pedido exista, que siga en estado Pendiente y que el
        producto exista. Despues delega la decision de stock al modelo y,
        si se acepta, guarda la linea en la base de datos.
        """
        pedido = self.obtener_por_id(pedido_id)
        if pedido is None:
            return False
        if pedido.get_estado() != "Pendiente":
            return False
        producto = self._producto_controller.obtener_por_id(producto_id)
        if producto is None:
            return False
        if pedido.agregar_producto(producto, cantidad):
            self._repositorio.guardar_detalle_pedido(pedido_id, producto_id, cantidad)
            return True
        return False

    def confirmar(self, pedido_id):
        """Confirma un pedido, persiste el cambio y retorna un valor logico.

        Al confirmar, el modelo descuenta el stock de cada producto; el
        repositorio escribe ese nuevo stock y el estado Confirmado.
        """
        pedido = self.obtener_por_id(pedido_id)
        if pedido is None:
            return False
        if pedido.confirmar():
            self._repositorio.actualizar_pedido(pedido)
            return True
        return False

    def cambiar_estado(self, pedido_id, nuevo_estado):
        """Cambia el estado de un pedido y retorna un valor logico."""
        pedido = self.obtener_por_id(pedido_id)
        if pedido is None:
            return False
        if pedido.cambiar_estado(nuevo_estado):
            self._repositorio.actualizar_estado_pedido(pedido.get_id(), pedido.get_estado())
            return True
        return False

    def calcular_total(self, pedido_id):
        """Retorna el total del pedido o None si el pedido no existe."""
        pedido = self.obtener_por_id(pedido_id)
        if pedido is None:
            return None
        return pedido.calcular_total()

    def listar(self):
        """Retorna la lista completa de objetos Pedido."""
        return self._repositorio.listar_pedidos()

    def listar_por_cliente(self, cliente_id):
        """Retorna solo los pedidos del cliente indicado."""
        return self._repositorio.listar_pedidos_por_cliente(cliente_id)

    def obtener_por_id(self, id):
        """Retorna el pedido con el id indicado o None si no existe."""
        return self._repositorio.obtener_pedido(id)

    def eliminar(self, id):
        """Elimina el pedido y sus lineas; retorna un valor logico."""
        return self._repositorio.eliminar_pedido(id)