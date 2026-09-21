"""Script de verificacion de los modelos POO (Modulo 1).

Ejecuta los cinco modelos para evidenciar en consola: constructores con
parametros, atributos privados, metodos con retorno numerico y logico,
uso de objetos, condicionales y el destructor de Producto.
"""

from backend.models.Categoria import Categoria
from backend.models.Producto import Producto
from backend.models.Cliente import Cliente
from backend.models.Pedido import Pedido

CATEGORIA_ABARROTES = Categoria(
    nombre="Abarrotes",
    descripcion="Productos de despensa y alimentacion",
)
print("Categoria creada:", CATEGORIA_ABARROTES)
print("La categoria es valida:", CATEGORIA_ABARROTES.es_valida())
print()

producto_arroz = Producto(
    nombre="Arroz 1 kg",
    descripcion="Arroz blanco de grano largo",
    precio_compra=2500,
    precio_venta=3200,
    stock=40,
    categoria=CATEGORIA_ABARROTES,
)
producto_aceite = Producto(
    nombre="Aceite vegetal 900 ml",
    descripcion="Aceite de cocina",
    precio_compra=7000,
    precio_venta=9200,
    stock=400,
    categoria=CATEGORIA_ABARROTES,
)

print("Producto creado:", producto_arroz)
print("Es valido:", producto_arroz.es_valido())
print("Ganancia por unidad:", producto_arroz.calcular_ganancia())
print("Precio con 10% de descuento:", producto_arroz.aplicar_descuento(10))
print("Hay stock para 5 unidades:", producto_arroz.hay_stock_disponible(5))
print("Hay stock para 500 unidades:", producto_arroz.hay_stock_disponible(500))
print()

cliente_normal = Cliente(
    nombre="Ana Torres",
    email="ana.torres@correo.com",
    telefono="3000000001",
)
cliente_frecuente = Cliente(
    nombre="Luis Mora",
    email="luis.mora@correo.com",
    telefono="3000000002",
    puntos=150,
)
print("Cliente creado:", cliente_normal)
print("Cliente valido:", cliente_normal.es_valido())
print("Puntos tras compra de 4000:", cliente_normal.acumular_puntos(4000))
print("Es cliente frecuente (Ana):", cliente_normal.es_cliente_frecuente())
print("Es cliente frecuente (Luis):", cliente_frecuente.es_cliente_frecuente())
print()

pedido_ana = Pedido(cliente=cliente_normal, fecha="2026-09-09")
pedido_luis = Pedido(cliente=cliente_frecuente, fecha="2026-09-09")

print("Pedido creado:", pedido_ana)
print("Agregar arroz x5:", pedido_ana.agregar_producto(producto_arroz, 5))
print("Agregar aceite x2:", pedido_ana.agregar_producto(producto_aceite, 2))
print("Total del pedido de Ana:", pedido_ana.calcular_total())

print("Agregar arroz x3 al pedido de Luis:", pedido_luis.agregar_producto(producto_arroz, 3))
print("Total del pedido de Luis con descuento:", pedido_luis.calcular_total())
print()

print("Stock de arroz antes de confirmar:", producto_arroz.get_stock())
print("Confirmar pedido de Ana:", pedido_ana.confirmar())
print("Stock de arroz despues de confirmar:", producto_arroz.get_stock())
print("Cambiar estado a Entregado:", pedido_ana.cambiar_estado("Entregado"))
print("Cambiar estado a un estado no valido:", pedido_ana.cambiar_estado("En camino"))
print("Unidades totales del pedido de Ana:", pedido_ana.cantidad_total_items())
print()

print("=== Evidencia del destructor ===")
del producto_aceite