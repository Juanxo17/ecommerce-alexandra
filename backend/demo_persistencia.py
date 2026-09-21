"""Script de verificacion de la persistencia SQLite (Modulo 3).

Demuestra la traduccion objetos <-> filas: crea datos con los controladores
y el repositorio, cierra la conexion (simula el cierre del programa) y
vuelve a abrir otra conexion al mismo archivo para comprobar que todos los
datos siguen en la base de datos.
"""

import os

from backend.controllers.categoria_controller import CategoriaController
from backend.controllers.cliente_controller import ClienteController
from backend.controllers.pedido_controller import PedidoController
from backend.controllers.producto_controller import ProductoController
from backend.data.repositorio_sqlite import RepositorioSqlite

RUTA_TIENDA_DB = os.path.join("database", "tienda.db")

if os.path.exists(RUTA_TIENDA_DB):
    os.remove(RUTA_TIENDA_DB)

print("=== 1. Inicializacion con datos semilla ===")
repositorio = RepositorioSqlite(RUTA_TIENDA_DB)
repositorio.inicializar(sembrar=True)

categoria_controller = CategoriaController(repositorio)
producto_controller = ProductoController(repositorio)
cliente_controller = ClienteController(repositorio)
pedido_controller = PedidoController(repositorio, cliente_controller, producto_controller)

print("Categorias sembradas:", len(categoria_controller.listar()))
print("Productos sembrados:", len(producto_controller.listar()))
print("Clientes sembrados:", len(cliente_controller.listar()))
print()

print("=== 2. Nuevos registros creados con los controladores ===")
categoria_bebidas = categoria_controller.crear("Bebidas", "Jugos y gaseosas")
print("Nueva categoria:", categoria_bebidas.get_nombre(), "(id", categoria_bebidas.get_id(), ")")
producto_jugo = producto_controller.crear(
    "Jugo 1 L", "Jugo de fruta natural", 4000, 5200, 30, categoria_id=categoria_bebidas.get_id(),
)
print("Nuevo producto:", producto_jugo.get_nombre(), "(id", producto_jugo.get_id(), ")")
cliente_memo = cliente_controller.crear("Memo Diaz", "memo.diaz@correo.com", "3000000004")
print("Nuevo cliente:", cliente_memo.get_nombre(), "(id", cliente_memo.get_id(), ")")
print()

print("=== 3. Pedido con confirmacion ===")
pedido = pedido_controller.crear(1, "2026-09-09")
print("Pedido creado para Ana (id", pedido.get_id(), "):", str(pedido))
print("Agregar arroz x3:", pedido_controller.agregar_producto(pedido.get_id(), 1, 3))
print("Agregar jugo x2:", pedido_controller.agregar_producto(pedido.get_id(), producto_jugo.get_id(), 2))
print("Total del pedido:", pedido_controller.calcular_total(pedido.get_id()))
print("Confirmar pedido:", pedido_controller.confirmar(pedido.get_id()))
pedido_confirmado = pedido_controller.obtener_por_id(pedido.get_id())
print("Estado del pedido:", pedido_confirmado.get_estado())
print("Lineas del pedido:", [str(d) for d in pedido_confirmado.get_detalles()])
print("Stock de arroz despues de confirmar:", producto_controller.obtener_por_id(1).get_stock())
print("Stock de jugo despues de confirmar:", producto_controller.obtener_por_id(producto_jugo.get_id()).get_stock())
print()

print("=== 4. Actualizacion y cierre de la conexion ===")
print("Actualizar stock del aceite a 380:", producto_controller.actualizar(2, stock=380).get_stock())
repositorio.cerrar()
print("Conexion cerrada. Los datos quedaron en el archivo:", RUTA_TIENDA_DB)
print()

print("=== 5. Reapertura: los datos sobrevivieron en disco ===")
repositorio_nuevo = RepositorioSqlite(RUTA_TIENDA_DB)
repositorio_nuevo.inicializar()

categoria_controller2 = CategoriaController(repositorio_nuevo)
producto_controller2 = ProductoController(repositorio_nuevo)
cliente_controller2 = ClienteController(repositorio_nuevo)
pedido_controller2 = PedidoController(repositorio_nuevo, cliente_controller2, producto_controller2)

print("Categorias leidas:", len(categoria_controller2.listar()))
print("Productos leidos:", len(producto_controller2.listar()))
print("Clientes leidos:", len(cliente_controller2.listar()))
pedido_leido = pedido_controller2.obtener_por_id(1)
print("Pedido 1 reconstruido desde disco:", str(pedido_leido))
print("  Total del pedido 1:", pedido_controller2.calcular_total(1))
print("  Lineas:", [str(d) for d in pedido_leido.get_detalles()])
print("  Stock de arroz en disco:", producto_controller2.obtener_por_id(1).get_stock())
print("  Stock de aceite en disco:", producto_controller2.obtener_por_id(2).get_stock())
print("  Cliente frecuente (Luis):", cliente_controller2.obtener_por_id(2).es_cliente_frecuente())
print("  Jugo sigue con su categoria:", producto_controller2.obtener_por_id(5).get_categoria().get_nombre())

repositorio_nuevo.cerrar()