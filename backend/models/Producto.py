"""Clase Producto: nucleo del inventario y de los precios del catalogo."""


class Producto:
    """Representa un producto del catalogo con su precio de compra, precio de
    venta, existencia disponible y categoria asociada.

    Incluye el destructor __del__ que deja evidencia en consola del momento
    en que un objeto se descarta de la memoria.
    """

    def __init__(self, nombre, descripcion, precio_compra, precio_venta, stock,
                 categoria=None, id=None, imagen=""):
        """Constructor: recibe parametros para crear un objeto Producto."""
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio_compra = precio_compra
        self._precio_venta = precio_venta
        self._stock = stock
        self._categoria = categoria
        self._imagen = imagen

    def __del__(self):
        """Destructor: evidencia en consola cuando el objeto se elimina."""
        print(f"[Destructor] El producto '{self._nombre}' se esta eliminando de la memoria.")

    def get_id(self):
        """Retorna el identificador del producto."""
        return self._id

    def get_nombre(self):
        """Retorna el nombre del producto."""
        return self._nombre

    def set_nombre(self, valor):
        """Asigna el nombre solo si el valor recibido no esta vacio."""
        if valor is not None and valor.strip() != "":
            self._nombre = valor

    def get_descripcion(self):
        """Retorna la descripcion del producto."""
        return self._descripcion

    def set_descripcion(self, valor):
        """Asigna la descripcion del producto."""
        self._descripcion = valor

    def get_precio_compra(self):
        """Retorna el precio de compra del producto."""
        return self._precio_compra

    def set_precio_compra(self, valor):
        """Asigna el precio de compra si el valor no es negativo."""
        if valor >= 0:
            self._precio_compra = valor

    def get_precio_venta(self):
        """Retorna el precio de venta del producto."""
        return self._precio_venta

    def set_precio_venta(self, valor):
        """Asigna el precio de venta si el valor es positivo."""
        if valor > 0:
            self._precio_venta = valor

    def get_stock(self):
        """Retorna las existencias disponibles del producto."""
        return self._stock

    def set_stock(self, valor):
        """Asigna las existencias si el valor no es negativo."""
        if valor >= 0:
            self._stock = valor

    def get_categoria(self):
        """Retorna el objeto Categoria asociado al producto."""
        return self._categoria

    def set_categoria(self, valor):
        """Asigna el objeto Categoria asociado al producto."""
        self._categoria = valor

    def get_imagen(self):
        """Retorna la imagen del producto (URL o datos en base 64)."""
        return self._imagen

    def set_imagen(self, valor):
        """Asigna la imagen del producto si el valor recibido es texto."""
        if valor is not None:
            self._imagen = valor

    def calcular_ganancia(self):
        """Retorna un valor numerico: la ganancia por unidad vendida."""
        return self._precio_venta - self._precio_compra

    def aplicar_descuento(self, porcentaje):
        """Retorna un valor numerico: el precio de venta con descuento.

        Si el porcentaje recibido no esta entre 0 y 100, retorna el precio
        original (condicion de proteccion).
        """
        if porcentaje >= 0 and porcentaje <= 100:
            return round(self._precio_venta * (1 - porcentaje / 100), 2)
        return self._precio_venta

    def hay_stock_disponible(self, cantidad):
        """Retorna un valor logico: hay suficiente existencia para la cantidad.

        La cantidad debe ser mayor que cero y no superar el stock actual.
        """
        return cantidad > 0 and self._stock >= cantidad

    def actualizar_stock(self, cantidad):
        """Resta existencias y retorna un valor logico del resultado.

        Solo descuenta si hay stock disponible; en caso contrario retorna
        False sin modificar el inventario.
        """
        if self.hay_stock_disponible(cantidad):
            self._stock = self._stock - cantidad
            return True
        return False

    def es_valido(self):
        """Retorna un valor logico: el producto tiene datos y precios validos."""
        nombre_ok = self._nombre is not None and self._nombre.strip() != ""
        precio_ok = self._precio_venta > 0 and self._precio_compra >= 0
        stock_ok = self._stock >= 0
        return nombre_ok and precio_ok and stock_ok

    def __str__(self):
        """Representacion en texto del producto."""
        return self._nombre