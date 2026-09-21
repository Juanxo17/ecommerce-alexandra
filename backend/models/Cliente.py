"""Clase Cliente: datos e historial de puntos de quien compra en la tienda."""


class Cliente:
    """Representa un cliente de la tienda con sus datos de contacto y puntos.

    Los puntos se acumulan con cada compra y permiten reconocer a los
    clientes frecuentes (decisio de negocio apoyada en un condicional).
    """

    UMBRAL_CLIENTE_FRECUENTE = 100

    def __init__(self, nombre, email, telefono="", puntos=0, id=None):
        """Constructor: recibe parametros para crear un objeto Cliente."""
        self._id = id
        self._nombre = nombre
        self._email = email
        self._telefono = telefono
        self._puntos = puntos

    def get_id(self):
        """Retorna el identificador del cliente."""
        return self._id

    def get_nombre(self):
        """Retorna el nombre del cliente."""
        return self._nombre

    def set_nombre(self, valor):
        """Asigna el nombre solo si el valor recibido no esta vacio."""
        if valor is not None and valor.strip() != "":
            self._nombre = valor

    def get_email(self):
        """Retorna el correo electronico del cliente."""
        return self._email

    def set_email(self, valor):
        """Asigna el correo electronico del cliente."""
        self._email = valor

    def get_telefono(self):
        """Retorna el telefono del cliente."""
        return self._telefono

    def set_telefono(self, valor):
        """Asigna el telefono del cliente."""
        self._telefono = valor

    def get_puntos(self):
        """Retorna los puntos acumulados del cliente."""
        return self._puntos

    def set_puntos(self, valor):
        """Asigna los puntos del cliente si el valor no es negativo."""
        if valor >= 0:
            self._puntos = valor

    def es_valido(self):
        """Retorna un valor logico: nombre y correo en formato basico valido."""
        nombre_ok = self._nombre is not None and self._nombre.strip() != ""
        email_ok = self._email is not None and "@" in self._email and "." in self._email
        return nombre_ok and email_ok

    def acumular_puntos(self, monto):
        """Retorna un valor numerico: los puntos acumulados tras una compra.

        Se otorgan 10 puntos por cada 1000 de valor de compra.
        """
        puntos_nuevos = (int(monto) // 1000) * 10
        self._puntos = self._puntos + puntos_nuevos
        return self._puntos

    def es_cliente_frecuente(self):
        """Retorna un valor logico: el cliente supero el umbral de puntos."""
        return self._puntos >= self.UMBRAL_CLIENTE_FRECUENTE

    def __str__(self):
        """Representacion en texto del cliente."""
        return self._nombreD