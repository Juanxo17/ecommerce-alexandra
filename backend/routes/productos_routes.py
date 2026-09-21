"""Rutas del CRUD de productos: conectan HTTP con ProductoController."""

from flask import Blueprint, jsonify, request


def crear_blueprint(producto_controller):
    """Fabrica el Blueprint de productos con endpoints REST."""

    bp = Blueprint("productos", __name__, url_prefix="/api/productos")

    def serializar(producto):
        categoria = producto.get_categoria()
        return {
            "id": producto.get_id(),
            "nombre": producto.get_nombre(),
            "descripcion": producto.get_descripcion(),
            "precio_compra": producto.get_precio_compra(),
            "precio_venta": producto.get_precio_venta(),
            "stock": producto.get_stock(),
            "categoria_id": categoria.get_id() if categoria is not None else None,
            "categoria": categoria.get_nombre() if categoria is not None else None,
            "imagen": producto.get_imagen(),
        }

    @bp.get("")
    def listar():
        ids = request.args.get("categoria")
        if ids is not None:
            try:
                lista = producto_controller.listar_por_categoria(int(ids))
            except ValueError:
                return jsonify({"error": "Parametro categoria invalido"}), 400
        else:
            lista = producto_controller.listar()
        return jsonify([serializar(p) for p in lista])

    @bp.get("/<int:producto_id>")
    def obtener(producto_id):
        producto = producto_controller.obtener_por_id(producto_id)
        if producto is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify(serializar(producto))

    @bp.post("")
    def crear():
        datos = request.get_json(silent=True) or {}
        producto = producto_controller.crear(
            datos.get("nombre"),
            datos.get("descripcion", ""),
            datos.get("precio_compra", 0),
            datos.get("precio_venta", 0),
            datos.get("stock", 0),
            datos.get("categoria_id"),
            datos.get("imagen", ""),
        )
        if producto is None:
            return jsonify({"error": "Datos del producto invalidos"}), 400
        return jsonify(serializar(producto)), 201

    @bp.put("/<int:producto_id>")
    def actualizar(producto_id):
        datos = request.get_json(silent=True) or {}
        producto = producto_controller.actualizar(
            producto_id,
            datos.get("nombre"),
            datos.get("descripcion"),
            datos.get("precio_compra"),
            datos.get("precio_venta"),
            datos.get("stock"),
            datos.get("imagen"),
        )
        if producto is None:
            return jsonify({"error": "Producto no encontrado o datos invalidos"}), 400
        return jsonify(serializar(producto))

    @bp.delete("/<int:producto_id>")
    def eliminar(producto_id):
        if producto_controller.eliminar(producto_id):
            return jsonify({"ok": True, "mensaje": "Producto eliminado"})
        return jsonify({"error": "Producto no encontrado"}), 404

    return bp