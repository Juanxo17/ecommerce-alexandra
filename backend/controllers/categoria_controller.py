"""Controlador de CRUD de categorias: crea y manipula objetos Categoria.

La persistencia se delega en el RepositorioSqlite: este controlador valida
los datos y decide, mientras que el repositorio traduce objetos a filas.
"""

from backend.models.Categoria import Categoria


class CategoriaController:
    """Controla el ciclo de vida de los objetos Categoria."""

    def __init__(self, repositorio):
        self._repositorio = repositorio

    def crear(self, nombre, descripcion=""):
        """Crea una categoria tras validar los datos recibidos.

        Retorna el objeto Categoria creado (con su id de base de datos)
        o None si los datos no son validos.
        """
        if nombre is None or nombre.strip() == "":
            return None
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        if not categoria.es_valida():
            return None
        return self._repositorio.guardar_categoria(categoria)

    def listar(self):
        """Retorna la lista completa de objetos Categoria."""
        return self._repositorio.listar_categorias()

    def obtener_por_id(self, id):
        """Retorna la categoria con el id indicado o None si no existe."""
        return self._repositorio.obtener_categoria(id)

    def actualizar(self, id, nombre=None, descripcion=None):
        """Actualiza los campos recibidos de una categoria y retorna el objeto.

        Retorna None si la categoria no existe. Los setters protegidos
        descartan valores vacios sin romper el objeto.
        """
        categoria = self.obtener_por_id(id)
        if categoria is None:
            return None
        if nombre is not None:
            categoria.set_nombre(nombre)
        if descripcion is not None:
            categoria.set_descripcion(descripcion)
        self._repositorio.actualizar_categoria(categoria)
        return categoria

    def eliminar(self, id):
        """Elimina la categoria con el id indicado y retorna un valor logico."""
        return self._repositorio.eliminar_categoria(id)