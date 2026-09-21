"""Controlador de CRUD de clientes: crea y manipula objetos Cliente.

La persistencia se delega en el RepositorioSqlite. Incluye una validacion
extra de unicidad: no se permite dos clientes con el mismo correo.
"""

from backend.models.Cliente import Cliente


class ClienteController:
    """Controla el ciclo de vida de los objetos Cliente."""

    def __init__(self, repositorio):
        self._repositorio = repositorio

    def crear(self, nombre, email, telefono="", puntos=0):
        """Crea un cliente tras validar sus datos y la unicidad del correo.

        Retorna el objeto Cliente creado, None si los datos son invalidos
        o si el correo ya esta registrado.
        """
        if nombre is None or nombre.strip() == "":
            return None
        cliente = Cliente(nombre=nombre, email=email, telefono=telefono,
                          puntos=puntos)
        if not cliente.es_valido():
            return None
        if self.obtener_por_email(email) is not None:
            return None
        return self._repositorio.guardar_cliente(cliente)

    def listar(self):
        """Retorna la lista completa de objetos Cliente."""
        return self._repositorio.listar_clientes()

    def obtener_por_id(self, id):
        """Retorna el cliente con el id indicado o None si no existe."""
        return self._repositorio.obtener_cliente(id)

    def obtener_por_email(self, email):
        """Retorna el cliente con el correo indicado o None si no existe."""
        return self._repositorio.obtener_cliente_por_email(email)

    def actualizar(self, id, nombre=None, email=None, telefono=None, puntos=None):
        """Actualiza los campos recibidos de un cliente y retorna el objeto."""
        cliente = self.obtener_por_id(id)
        if cliente is None:
            return None
        if nombre is not None:
            cliente.set_nombre(nombre)
        if email is not None:
            if self.obtener_por_email(email) is not None:
                return None
            cliente.set_email(email)
        if telefono is not None:
            cliente.set_telefono(telefono)
        if puntos is not None:
            cliente.set_puntos(puntos)
        self._repositorio.actualizar_cliente(cliente)
        return cliente

    def eliminar(self, id):
        """Elimina el cliente con el id indicado y retorna un valor logico."""
        return self._repositorio.eliminar_cliente(id)