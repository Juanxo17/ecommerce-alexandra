"""Controlador de CRUD de productos: crea y manipula objetos Producto.

La persistencia se delega en el RepositorioSqlite. El controlador valida
los datos, resuelve la categoria del producto y toma las decisiones.
"""

from backend.models.Producto import Producto


class ProductoController:
    """Controla el ciclo de vida de los objetos Producto."""

    def __init__(self, repositorio):
        self._repositorio = repositorio

    def crear(self, nombre, descripcion, precio_compra, precio_venta, stock,
              categoria_id=None, imagen=""):
        """Crea un producto tras validar datos, precios y categoria.

        Retorna el objeto Producto creado (con su id de base de datos)
        o None si algun dato es invalido.
        """
        if nombre is None or nombre.strip() == "":
            return None
        if precio_venta <= 0 or precio_compra < 0 or stock < 0:
            return None

        categoria = None
        if categoria_id is not None:
            categoria = self._repositorio.obtener_categoria(categoria_id)
            if categoria is None:
                return None

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
            categoria=categoria,
            imagen=imagen if imagen is not None else "",
        )
        if not producto.es_valido():
            return None
        return self._repositorio.guardar_producto(producto)

    def listar(self):
        """Retorna la lista completa de objetos Producto."""
        return self._repositorio.listar_productos()

    def listar_por_categoria(self, categoria_id):
        """Retorna solo los productos que pertenecen a la categoria indicada."""
        return self._repositorio.listar_productos_por_categoria(categoria_id)

    def obtener_por_id(self, id):
        """Retorna el producto con el id indicado o None si no existe."""
        return self._repositorio.obtener_producto(id)

    def actualizar(self, id, nombre=None, descripcion=None, precio_compra=None,
                   precio_venta=None, stock=None, imagen=None):
        """Actualiza los campos recibidos de un producto y retorna el objeto.

        Antes de asignar nuevos valores se validan numeros negativos o
        precios no positivos; en esos casos se ignora el campo recibido.
        """
        producto = self.obtener_por_id(id)
        if producto is None:
            return None
        if nombre is not None:
            producto.set_nombre(nombre)
        if descripcion is not None:
            producto.set_descripcion(descripcion)
        if precio_compra is not None and precio_compra >= 0:
            producto.set_precio_compra(precio_compra)
        if precio_venta is not None and precio_venta > 0:
            producto.set_precio_venta(precio_venta)
        if stock is not None and stock >= 0:
            producto.set_stock(stock)
        if imagen is not None:
            producto.set_imagen(imagen)
        self._repositorio.actualizar_producto(producto)
        return producto

    def eliminar(self, id):
        """Elimina el producto con el id indicado y retorna un valor logico."""
        return self._repositorio.eliminar_producto(id)