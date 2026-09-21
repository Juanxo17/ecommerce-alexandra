"""Clase Categoria: agrupa los productos del catalogo de la tienda."""


class Categoria:
    """Representa una categoria a la que pertenecen los productos.

    Sus atributos son privados (prefijo _) y se accede a ellos mediante
    metodos de acceso (get_ / set_), reforzando el encapsulamiento.
    """

    def __init__(self, nombre, descripcion="", id=None):
        """Constructor: recibe parametros y crea una instancia de Categoria."""
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion

    def get_id(self):
        """Retorna el identificador de la categoria."""
        return self._id

    def get_nombre(self):
        """Retorna el nombre de la categoria."""
        return self._nombre

    def set_nombre(self, valor):
        """Asigna el nombre solo si el valor recibido no esta vacio."""
        if valor is not None and valor.strip() != "":
            self._nombre = valor

    def get_descripcion(self):
        """Retorna la descripcion de la categoria."""
        return self._descripcion

    def set_descripcion(self, valor):
        """Asigna la descripcion de la categoria."""
        self._descripcion = valor

    def es_valida(self):
        """Retorna un valor logico: verdadero si el nombre no esta vacio."""
        return self._nombre is not None and self._nombre.strip() != ""

    def __str__(self):
        """Representacion en texto de la categoria."""
        return self._nombre