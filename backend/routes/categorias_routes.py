"""Rutas del CRUD de categorias: conectan HTTP con CategoriaController."""

from flask import Blueprint, jsonify, request


def crear_blueprint(categoria_controller):
    """Fabrica el Blueprint de categorias con endpoints REST."""

    bp = Blueprint("categorias", __name__, url_prefix="/api/categorias")

    def serializar(categoria):
        return {
            "id": categoria.get_id(),
            "nombre": categoria.get_nombre(),
            "descripcion": categoria.get_descripcion(),
        }

    @bp.get("")
    def listar():
        return jsonify([serializar(c) for c in categoria_controller.listar()])

    @bp.get("/<int:categoria_id>")
    def obtener(categoria_id):
        categoria = categoria_controller.obtener_por_id(categoria_id)
        if categoria is None:
            return jsonify({"error": "Categoria no encontrada"}), 404
        return jsonify(serializar(categoria))

    @bp.post("")
    def crear():
        datos = request.get_json(silent=True) or {}
        categoria = categoria_controller.crear(
            datos.get("nombre"), datos.get("descripcion", ""),
        )
        if categoria is None:
            return jsonify({"error": "Nombre invalido o vacio"}), 400
        return jsonify(serializar(categoria)), 201

    @bp.put("/<int:categoria_id>")
    def actualizar(categoria_id):
        datos = request.get_json(silent=True) or {}
        categoria = categoria_controller.actualizar(
            categoria_id, datos.get("nombre"), datos.get("descripcion"),
        )
        if categoria is None:
            return jsonify({"error": "Categoria no encontrada o datos invalidos"}), 400
        return jsonify(serializar(categoria))

    @bp.delete("/<int:categoria_id>")
    def eliminar(categoria_id):
        if categoria_controller.eliminar(categoria_id):
            return jsonify({"ok": True, "mensaje": "Categoria eliminada"})
        return jsonify({"error": "Categoria no encontrada"}), 404

    return bp