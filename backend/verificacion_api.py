"""Script de verificacion de la API REST (Modulo 4).

Usa el cliente de prueba de Flask (sin levantar un servidor real) para
consultar cada endpoint, mostrando el viaje completo de una peticion:
JSON recibido en la ruta -> controlador -> modelo -> repositorio, y la
respuesta JSON de vuelta.
"""

import os

from backend.app import crear_app

RUTA_API_DB = os.path.join("database", "tienda_api.db")

if os.path.exists(RUTA_API_DB):
    os.remove(RUTA_API_DB)

app = crear_app(RUTA_API_DB, sembrar=True)
cliente = app.test_client()
resp = lambda r: (r.status_code, r.get_json())


def mostrar(titulo, resultado):
    print(titulo, "->", resultado)


print("=== Estado del servicio ===")
mostrar("GET /api/estado", resp(cliente.get("/api/estado")))
print()

print("=== CRUD de categorias ===")
mostrar("GET /api/categorias", resp(cliente.get("/api/categorias")))
mostrar("POST /api/categorias (crear)", resp(cliente.post("/api/categorias", json={"nombre": "Bebidas"})))
mostrar("POST nombre vacio", resp(cliente.post("/api/categorias", json={"nombre": "   "})))
mostrar("GET /api/categorias/4", resp(cliente.get("/api/categorias/4")))
mostrar("GET /api/categorias/99", resp(cliente.get("/api/categorias/99")))
mostrar("PUT /api/categorias/4", resp(cliente.put("/api/categorias/4", json={"nombre": "Bebidas y refrescos"})))
mostrar("DELETE /api/categorias/4", resp(cliente.delete("/api/categorias/4")))
mostrar("GET /api/categorias/4 tras borrar", resp(cliente.get("/api/categorias/4")))
print()

print("=== CRUD de productos ===")
mostrar("POST /api/productos (crear)", resp(cliente.post("/api/productos", json={
    "nombre": "Jugo 1 L", "descripcion": "Jugo natural", "precio_compra": 4000,
    "precio_venta": 5200, "stock": 30, "categoria_id": 1,
})))
mostrar("POST precio invalido", resp(cliente.post("/api/productos", json={
    "nombre": "Malo", "precio_venta": 0, "stock": 5, "categoria_id": 1,
})))
mostrar("GET /api/productos", resp(cliente.get("/api/productos")))
mostrar("GET /api/productos?categoria=1", resp(cliente.get("/api/productos?categoria=1")))
mostrar("PUT /api/productos/5 stock=25", resp(cliente.put("/api/productos/5", json={"stock": 25})))
mostrar("DELETE /api/productos/5", resp(cliente.delete("/api/productos/5")))
print()

print("=== CRUD de clientes ===")
mostrar("POST /api/clientes (crear)", resp(cliente.post("/api/clientes", json={
    "nombre": "Memo Diaz", "email": "memo.diaz@correo.com",
})))
mostrar("POST correo duplicado", resp(cliente.post("/api/clientes", json={
    "nombre": "Otro", "email": "memo.diaz@correo.com",
})))
mostrar("POST correo invalido", resp(cliente.post("/api/clientes", json={
    "nombre": "Otro", "email": "correo-sin-arroba",
})))
mostrar("GET /api/clientes", resp(cliente.get("/api/clientes")))
print()

print("=== Pedidos (crear, agregar, confirmar, estado) ===")
mostrar("POST /api/pedidos", resp(cliente.post("/api/pedidos", json={
    "cliente_id": 1, "fecha": "2026-09-09",
})))
mostrar("POST /api/pedidos/1/productos x5 arroz", resp(cliente.post(
    "/api/pedidos/1/productos", json={"producto_id": 1, "cantidad": 5},
)))
mostrar("POST x500 sin stock", resp(cliente.post(
    "/api/pedidos/1/productos", json={"producto_id": 1, "cantidad": 500},
)))
mostrar("GET /api/pedidos/1 (total)", resp(cliente.get("/api/pedidos/1")))
mostrar("POST /api/pedidos/1/confirmar", resp(cliente.post("/api/pedidos/1/confirmar")))
mostrar("POST confirmar de nuevo", resp(cliente.post("/api/pedidos/1/confirmar")))
mostrar("PUT /api/pedidos/1/estado Entregado", resp(cliente.put(
    "/api/pedidos/1/estado", json={"estado": "Entregado"},
)))
mostrar("PUT estado invalido", resp(cliente.put(
    "/api/pedidos/1/estado", json={"estado": "En camino"},
)))
mostrar("GET /api/productos/1 (stock tras confirmar)", resp(cliente.get("/api/productos/1")))
mostrar("GET /api/pedidos", resp(cliente.get("/api/pedidos")))
mostrar("DELETE /api/pedidos/2", resp(cliente.delete("/api/pedidos/2")))