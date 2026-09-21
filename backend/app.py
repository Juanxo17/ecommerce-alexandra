"""Aplicacion Flask del Taller CRUD Tienda (capa de Rutas/HTTP).

Fabrica la aplicacion conectando el RepositorioSqlite (Modulo 3) con los
controladores (Modulo 2) y los blueprints de rutas (Modulo 4). Cada
peticion HTTP viaja: ruta -> controlador -> modelo -> repositorio, y la
respuesta regresa como JSON hacia la Vista (Modulo 5).
"""

import os

from flask import Flask

from backend.controllers.categoria_controller import CategoriaController
from backend.controllers.cliente_controller import ClienteController
from backend.controllers.pedido_controller import PedidoController
from backend.controllers.producto_controller import ProductoController
from backend.data.repositorio_sqlite import RepositorioSqlite

RUTA_TIENDA_DB = os.path.join("database", "tienda.db")


def crear_app(ruta_base_datos=RUTA_TIENDA_DB, sembrar=False):
    """Fabrica y devuelve la aplicacion Flask con todo el backend conectado."""
    repositorio = RepositorioSqlite(ruta_base_datos)
    repositorio.inicializar(sembrar=sembrar)

    categoria_controller = CategoriaController(repositorio)
    producto_controller = ProductoController(repositorio)
    cliente_controller = ClienteController(repositorio)
    pedido_controller = PedidoController(
        repositorio, cliente_controller, producto_controller,
    )

    from backend.routes.categorias_routes import crear_blueprint as categorias_bp
    from backend.routes.clientes_routes import crear_blueprint as clientes_bp
    from backend.routes.pedidos_routes import crear_blueprint as pedidos_bp
    from backend.routes.productos_routes import crear_blueprint as productos_bp

    app = Flask(__name__)
    app.register_blueprint(categorias_bp(categoria_controller))
    app.register_blueprint(productos_bp(producto_controller))
    app.register_blueprint(clientes_bp(cliente_controller))
    app.register_blueprint(pedidos_bp(pedido_controller))

    @app.get("/api/estado")
    def estado():
        return {"servicio": "Tienda CRUD", "estado": "operativo"}

    return app


if __name__ == "__main__":
    if not os.path.exists(RUTA_TIENDA_DB):
        app = crear_app(sembrar=True)
    else:
        app = crear_app()
    app.run(debug=True, port=5000)