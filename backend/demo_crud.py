"""Script de verificacion de los controladores CRUD (Modulo 2).

Ejecuta creacion, lectura, actualizacion y eliminacion de cada entidad a
traves de los controladores, mostrando el uso de objetos entre capas, el
paso de parametros y las validaciones con condicionales. Desde el Modulo 3
los controladores guardan los datos a traves del RepositorioSqlite.
"""

import os

from backend.controllers.categoria_controller import CategoriaController
from backend.controllers.producto_controller import ProductoController
from backend.controllers.cliente_controller import ClienteController
from backend.controllers.pedido_controller import PedidoController
from backend.data.repositorio_sqlite import RepositorioSqlite

RUTA_DEMO_DB = os.path.join("database", "tienda_demo.db")

if os.path.exists(RUTA_DEMO_DB):
    os.remove(RUTA_DEMO_DB)

repositorio = RepositorioSqlite(RUTA_DEMO_DB)
repositorio.inicializar()

categoria_controller = CategoriaController(repositorio)
producto_controller = ProductoController(repositorio)
cliente_controller = ClienteController(repositorio)
pedido_controller = PedidoController(repositorio, cliente_controller, producto_controller)

print("=== CRUD de categorias ===")
cat_abarrotes = categoria_controller.crear("Abarrotes", "Despensa y alimentacion")
cat_lacteos = categoria_controller.crear("Lacteos", "Leche y derivados")
print("Categorias creadas:", len(categoria_controller.listar()))
print("Crear categoria sin nombre:", categoria_controller.crear("   "))
print("Categoria inexistente por id:", categoria_controller.obtener_por_id(99))
print("Actualizar categoria 1:", categoria_controller.actualizar(1, nombre="Abarrotes y despensa"))
print("Eliminar categoria 2:", categoria_controller.eliminar(2))
print("Categorias restantes:", len(categoria_controller.listar()))
print()

print("=== CRUD de productos ===")
prod_arroz = producto_controller.crear(
    "Arroz 1 kg", "Arroz blanco", 2500, 3200, 40, categoria_id=1,
)
prod_aceite = producto_controller.crear(
    "Aceite 900 ml", "Aceite vegetal", 7000, 9200, 400, categoria_id=1,
)
print("Productos creados:", len(producto_controller.listar()))
print("Precio de venta invalido (None):", producto_controller.crear("X", "", 100, 0, 5, 1))
print("Categoria inexistente (None):", producto_controller.crear("Y", "", 100, 200, 5, 99))
print("Actualizar stock del producto 1:", producto_controller.actualizar(1, stock=35).get_stock())
print("Productos de la categoria 1:", len(producto_controller.listar_por_categoria(1)))
print("Hay stock para 100 de arroz:", prod_arroz.hay_stock_disponible(100))
print()

print("=== CRUD de clientes ===")
cli_ana = cliente_controller.crear("Ana Torres", "ana.torres@correo.com", "3000000001")
cli_luis = cliente_controller.crear("Luis Mora", "luis.mora@correo.com", "3000000002", puntos=150)
print("Clientes creados:", len(cliente_controller.listar()))
print("Correo duplicado (None):", cliente_controller.crear("Ana Dos", "ana.torres@correo.com"))
print("Correo sin arroba (None):", cliente_controller.crear("Perla", "perla-correo"))
print("Buscar por email:", cliente_controller.obtener_por_email("LUIS.MORA@correo.com").get_nombre())
print()

print("=== CRUD de pedidos ===")
pedido_ana = pedido_controller.crear(1, "2026-09-09")
pedido_luis = pedido_controller.crear(2, "2026-09-09")
print("Pedidos creados:", len(pedido_controller.listar()))
print("Pedido para cliente inexistente (None):", pedido_controller.crear(99, "2026-09-09"))
print("Agregar arroz x5 a pedido 1:", pedido_controller.agregar_producto(1, 1, 5))
print("Agregar arroz x100 (sin stock):", pedido_controller.agregar_producto(1, 1, 100))
print("Total del pedido 1:", pedido_controller.calcular_total(1))
print("Confirmar pedido 1:", pedido_controller.confirmar(1))
print("Stock de arroz tras confirmar:", prod_arroz.get_stock())
print("Agregar tras confirmar:", pedido_controller.agregar_producto(1, 2, 1))
print("Cambiar estado a Entregado:", pedido_controller.cambiar_estado(1, "Entregado"))
print("Cambiar a estado invalido:", pedido_controller.cambiar_estado(1, "En camino"))
print("Agregar aceite x1 a pedido 2:", pedido_controller.agregar_producto(2, 2, 1))
print("Total de pedido 2 (cliente frecuente, 5% dcto):", pedido_controller.calcular_total(2))
print("Pedidos del cliente 2:", len(pedido_controller.listar_por_cliente(2)))
print("Eliminar pedido 2:", pedido_controller.eliminar(2))
print("Pedidos restantes:", len(pedido_controller.listar()))
print()

print("=== Resumen final ===")
print("Categorias:", [str(c) for c in categoria_controller.listar()])
print("Productos:", [(p.get_nombre(), p.get_stock()) for p in producto_controller.listar()])
print("Clientes:", [str(c) for c in cliente_controller.listar()])

repositorio.cerrar()