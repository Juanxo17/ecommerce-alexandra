"""Capa de acceso a datos: traduce objetos POO a filas de SQLite y viceversa.

El RepositorioSqlite separa la logica de negocio (backend.models) de la
persistencia: los controladores trabajan unicamente con objetos y esta capa
se encarga de convertir cada objeto en una fila de la base de datos (INSERT/
UPDATE) y cada fila de vuelta en un objeto (constructor del modelo).
"""

import os
import sqlite3

from backend.models.Categoria import Categoria
from backend.models.Cliente import Cliente
from backend.models.DetallePedido import DetallePedido
from backend.models.Pedido import Pedido
from backend.models.Producto import Producto

RUTA_BASE_DATOS = os.path.join("database", "tienda.db")

RUTA_SCHEMA = os.path.join("database", "schema.sql")
RUTA_SEED = os.path.join("database", "seed.sql")


class RepositorioSqlite:
    """Ofrece las operaciones de persistencia de las cinco entidades.

    Cada metodo de escritura recibe un objeto del modelo y lo convierte en
    una fila SQL; cada metodo de lectura convierte filas en objetos usando
    los constructores del modelo. Todas las consultas usan parametros
    placeholder (?) para evitar inyeccion SQL.
    """

    def __init__(self, ruta_base_datos=RUTA_BASE_DATOS):
        """Abre la conexion al archivo SQLite.

        check_same_thread=False permite que la misma conexion sea usada por
        los hilos del servidor Flask (cada peticion HTTP se atiende en un
        hilo distinto).
        """
        self._ruta_base_datos = ruta_base_datos
        self._conexion = sqlite3.connect(ruta_base_datos, check_same_thread=False)
        self._conexion.row_factory = sqlite3.Row
        self._conexion.execute("PRAGMA foreign_keys = ON")

    def cerrar(self):
        """Cierra la conexion con la base de datos."""
        self._conexion.close()

    def inicializar(self, sembrar=False):
        """Crea las tablas con schema.sql y, si se pide, carga seed.sql."""
        with open(RUTA_SCHEMA, "r", encoding="utf-8") as archivo:
            self._conexion.executescript(archivo.read())
        if sembrar:
            with open(RUTA_SEED, "r", encoding="utf-8") as archivo:
                self._conexion.executescript(archivo.read())

    # ------------------------------------------------------------------
    # Categorias
    # ------------------------------------------------------------------

    def guardar_categoria(self, categoria):
        """Traduce el objeto Categoria a una fila nueva de la tabla."""
        cursor = self._conexion.execute(
            "INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)",
            (categoria.get_nombre(), categoria.get_descripcion()),
        )
        self._conexion.commit()
        return Categoria(nombre=categoria.get_nombre(),
                         descripcion=categoria.get_descripcion(),
                         id=cursor.lastrowid)

    def obtener_categoria(self, id):
        """Traduce la fila de una categoria a un objeto Categoria."""
        fila = self._conexion.execute(
            "SELECT * FROM categorias WHERE id = ?", (id,)
        ).fetchone()
        if fila is None:
            return None
        return Categoria(nombre=fila["nombre"], descripcion=fila["descripcion"],
                         id=fila["id"])

    def listar_categorias(self):
        """Retorna una lista de objetos Categoria con todas las categorias."""
        filas = self._conexion.execute(
            "SELECT * FROM categorias ORDER BY id"
        ).fetchall()
        return [Categoria(nombre=fila["nombre"], descripcion=fila["descripcion"],
                          id=fila["id"]) for fila in filas]

    def actualizar_categoria(self, categoria):
        """Traduce las modificaciones de un objeto Categoria a una fila."""
        self._conexion.execute(
            "UPDATE categorias SET nombre = ?, descripcion = ? WHERE id = ?",
            (categoria.get_nombre(), categoria.get_descripcion(), categoria.get_id()),
        )
        self._conexion.commit()

    def eliminar_categoria(self, id):
        """Elimina la categoria con el id indicado; retorna un valor logico."""
        cursor = self._conexion.execute(
            "DELETE FROM categorias WHERE id = ?", (id,)
        )
        self._conexion.commit()
        return cursor.rowcount > 0

    # ------------------------------------------------------------------
    # Productos
    # ------------------------------------------------------------------

    def _fila_producto_a_objeto(self, fila):
        """Convierte una fila de productos (con categoria) en un objeto Producto."""
        categoria = None
        if fila["categoria_id"] is not None:
            categoria = Categoria(nombre=fila["categoria_nombre"],
                                  descripcion=fila["categoria_descripcion"],
                                  id=fila["categoria_id"])
        return Producto(nombre=fila["nombre"], descripcion=fila["descripcion"],
                        precio_compra=fila["precio_compra"],
                        precio_venta=fila["precio_venta"], stock=fila["stock"],
                        categoria=categoria, id=fila["id"],
                        imagen=fila["imagen"] if "imagen" in fila.keys() else "")

    def _consulta_productos_con_categoria(self):
        """SQL base que une productos con su categoria para construir objetos."""
        return (
            "SELECT p.*, c.nombre AS categoria_nombre, "
            "c.descripcion AS categoria_descripcion "
            "FROM productos p LEFT JOIN categorias c ON c.id = p.categoria_id "
        )

    def guardar_producto(self, producto):
        """Traduce el objeto Producto a una fila nueva de la tabla."""
        categoria_id = None
        if producto.get_categoria() is not None:
            categoria_id = producto.get_categoria().get_id()
        cursor = self._conexion.execute(
            "INSERT INTO productos (nombre, descripcion, precio_compra, "
            "precio_venta, stock, categoria_id, imagen) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (producto.get_nombre(), producto.get_descripcion(),
             producto.get_precio_compra(), producto.get_precio_venta(),
             producto.get_stock(), categoria_id, producto.get_imagen()),
        )
        self._conexion.commit()
        return self.obtener_producto(cursor.lastrowid)

    def listar_productos(self):
        """Retorna una lista de objetos Producto con todas las filas."""
        filas = self._conexion.execute(
            self._consulta_productos_con_categoria() + "ORDER BY p.id"
        ).fetchall()
        return [self._fila_producto_a_objeto(fila) for fila in filas]

    def listar_productos_por_categoria(self, categoria_id):
        """Retorna solo los productos de la categoria indicada."""
        filas = self._conexion.execute(
            self._consulta_productos_con_categoria() + "WHERE p.categoria_id = ?",
            (categoria_id,),
        ).fetchall()
        return [self._fila_producto_a_objeto(fila) for fila in filas]

    def obtener_producto(self, id):
        """Traduce la fila de un producto a un objeto Producto."""
        fila = self._conexion.execute(
            self._consulta_productos_con_categoria() + "WHERE p.id = ?",
            (id,),
        ).fetchone()
        if fila is None:
            return None
        return self._fila_producto_a_objeto(fila)

    def actualizar_producto(self, producto):
        """Traduce las modificaciones de un objeto Producto a una fila."""
        categoria_id = None
        if producto.get_categoria() is not None:
            categoria_id = producto.get_categoria().get_id()
        self._conexion.execute(
            "UPDATE productos SET nombre = ?, descripcion = ?, precio_compra = ?, "
            "precio_venta = ?, stock = ?, categoria_id = ?, imagen = ? WHERE id = ?",
            (producto.get_nombre(), producto.get_descripcion(),
             producto.get_precio_compra(), producto.get_precio_venta(),
             producto.get_stock(), categoria_id, producto.get_imagen(),
             producto.get_id()),
        )
        self._conexion.commit()

    def eliminar_producto(self, id):
        """Elimina el producto con el id indicado; retorna un valor logico."""
        cursor = self._conexion.execute(
            "DELETE FROM productos WHERE id = ?", (id,)
        )
        self._conexion.commit()
        return cursor.rowcount > 0

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------

    def guardar_cliente(self, cliente):
        """Traduce el objeto Cliente a una fila nueva de la tabla."""
        cursor = self._conexion.execute(
            "INSERT INTO clientes (nombre, email, telefono, puntos) "
            "VALUES (?, ?, ?, ?)",
            (cliente.get_nombre(), cliente.get_email(),
             cliente.get_telefono(), cliente.get_puntos()),
        )
        self._conexion.commit()
        return Cliente(nombre=cliente.get_nombre(), email=cliente.get_email(),
                       telefono=cliente.get_telefono(),
                       puntos=cliente.get_puntos(), id=cursor.lastrowid)

    def _fila_cliente_a_objeto(self, fila):
        """Convierte una fila de clientes en un objeto Cliente."""
        return Cliente(nombre=fila["nombre"], email=fila["email"],
                       telefono=fila["telefono"], puntos=fila["puntos"],
                       id=fila["id"])

    def listar_clientes(self):
        """Retorna una lista de objetos Cliente con todas las filas."""
        filas = self._conexion.execute(
            "SELECT * FROM clientes ORDER BY id"
        ).fetchall()
        return [self._fila_cliente_a_objeto(fila) for fila in filas]

    def obtener_cliente(self, id):
        """Traduce la fila de un cliente a un objeto Cliente."""
        fila = self._conexion.execute(
            "SELECT * FROM clientes WHERE id = ?", (id,)
        ).fetchone()
        if fila is None:
            return None
        return self._fila_cliente_a_objeto(fila)

    def obtener_cliente_por_email(self, email):
        """Traduce la fila de un cliente buscado por correo a un objeto."""
        fila = self._conexion.execute(
            "SELECT * FROM clientes WHERE email = ? COLLATE NOCASE", (email,)
        ).fetchone()
        if fila is None:
            return None
        return self._fila_cliente_a_objeto(fila)

    def actualizar_cliente(self, cliente):
        """Traduce las modificaciones de un objeto Cliente a una fila."""
        self._conexion.execute(
            "UPDATE clientes SET nombre = ?, email = ?, telefono = ?, "
            "puntos = ? WHERE id = ?",
            (cliente.get_nombre(), cliente.get_email(),
             cliente.get_telefono(), cliente.get_puntos(), cliente.get_id()),
        )
        self._conexion.commit()

    def eliminar_cliente(self, id):
        """Elimina el cliente con el id indicado; retorna un valor logico."""
        cursor = self._conexion.execute(
            "DELETE FROM clientes WHERE id = ?", (id,)
        )
        self._conexion.commit()
        return cursor.rowcount > 0

    # ------------------------------------------------------------------
    # Pedidos y detalle de pedidos
    # ------------------------------------------------------------------

    def guardar_pedido(self, pedido):
        """Traduce el objeto Pedido a una fila nueva de la tabla.

        Los detalles del pedido se guardan por separado con
        guardar_detalle_pedido cuando se agregan productos.
        """
        cursor = self._conexion.execute(
            "INSERT INTO pedidos (cliente_id, fecha, estado) VALUES (?, ?, ?)",
            (pedido.get_cliente().get_id(), pedido.get_fecha(),
             pedido.get_estado()),
        )
        self._conexion.commit()
        return Pedido(cliente=pedido.get_cliente(), fecha=pedido.get_fecha(),
                      estado=pedido.get_estado(), id=cursor.lastrowid)

    def guardar_detalle_pedido(self, pedido_id, producto_id, cantidad):
        """Traduce una linea nueva del pedido a una fila de detalle_pedidos.

        El precio unitario se toma de la columna precio_venta del producto,
        igual que hace el modelo DetallePedido cuando no recibe precio.
        """
        self._conexion.execute(
            "INSERT INTO detalle_pedidos (pedido_id, producto_id, cantidad, "
            "precio_unitario) "
            "SELECT ?, ?, ?, precio_venta FROM productos WHERE id = ?",
            (pedido_id, producto_id, cantidad, producto_id),
        )
        self._conexion.commit()

    def obtener_pedido(self, id):
        """Traduce un pedido (con cliente y lineas) a objetos del modelo."""
        fila = self._conexion.execute(
            "SELECT * FROM pedidos WHERE id = ?", (id,)
        ).fetchone()
        if fila is None:
            return None
        cliente = self.obtener_cliente(fila["cliente_id"])
        pedido = Pedido(cliente=cliente, fecha=fila["fecha"],
                        estado=fila["estado"], id=fila["id"])
        filas_detalle = self._conexion.execute(
            "SELECT * FROM detalle_pedidos WHERE pedido_id = ? ORDER BY id",
            (id,),
        ).fetchall()
        for fila_detalle in filas_detalle:
            producto = self.obtener_producto(fila_detalle["producto_id"])
            detalle = DetallePedido(producto=producto,
                                    cantidad=fila_detalle["cantidad"],
                                    precio_unitario=fila_detalle["precio_unitario"],
                                    id=fila_detalle["id"])
            pedido.get_detalles().append(detalle)
        return pedido

    def listar_pedidos(self):
        """Retorna una lista de objetos Pedido, ordenados por id."""
        filas = self._conexion.execute(
            "SELECT * FROM pedidos ORDER BY id"
        ).fetchall()
        return [self.obtener_pedido(fila["id"]) for fila in filas]

    def listar_pedidos_por_cliente(self, cliente_id):
        """Retorna los pedidos de un cliente en orden de creacion."""
        filas = self._conexion.execute(
            "SELECT * FROM pedidos WHERE cliente_id = ? ORDER BY id",
            (cliente_id,),
        ).fetchall()
        return [self.obtener_pedido(fila["id"]) for fila in filas]

    def actualizar_pedido(self, pedido):
        """Persiste el estado del pedido y el stock de sus productos.

        Se usa al confirmar: el objeto Pedido ya decremento el stock de cada
        producto, y esta capa escribe ese nuevo stock en la tabla productos.
        """
        with self._conexion:
            self._conexion.execute(
                "UPDATE pedidos SET estado = ? WHERE id = ?",
                (pedido.get_estado(), pedido.get_id()),
            )
            for detalle in pedido.get_detalles():
                producto = detalle.get_producto()
                self._conexion.execute(
                    "UPDATE productos SET stock = ? WHERE id = ?",
                    (producto.get_stock(), producto.get_id()),
                )

    def actualizar_estado_pedido(self, pedido_id, estado):
        """Persiste solo el estado de un pedido."""
        self._conexion.execute(
            "UPDATE pedidos SET estado = ? WHERE id = ?", (estado, pedido_id)
        )
        self._conexion.commit()

    def eliminar_pedido(self, id):
        """Elimina el pedido y sus lineas; retorna un valor logico."""
        with self._conexion:
            self._conexion.execute(
                "DELETE FROM detalle_pedidos WHERE pedido_id = ?", (id,)
            )
            cursor = self._conexion.execute(
                "DELETE FROM pedidos WHERE id = ?", (id,)
            )
        return cursor.rowcount > 0