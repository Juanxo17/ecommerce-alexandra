"""Rutas del CRUD de clientes: conectan HTTP con ClienteController."""

from flask import Blueprint, jsonify, request


def crear_blueprint(cliente_controller):
    """Fabrica el Blueprint de clientes con endpoints REST."""

    bp = Blueprint("clientes", __name__, url_prefix="/api/clientes")

    def serializar(cliente):
        return {
            "id": cliente.get_id(),
            "nombre": cliente.get_nombre(),
            "email": cliente.get_email(),
            "telefono": cliente.get_telefono(),
            "puntos": cliente.get_puntos(),
            "es_frecuente": cliente.es_cliente_frecuente(),
        }

    @bp.get("")
    def listar():
        return jsonify([serializar(c) for c in cliente_controller.listar()])

    @bp.get("/<int:cliente_id>")
    def obtener(cliente_id):
        cliente = cliente_controller.obtener_por_id(cliente_id)
        if cliente is None:
            return jsonify({"error": "Cliente no encontrado"}), 404
        return jsonify(serializar(cliente))

    @bp.post("")
    def crear():
        datos = request.get_json(silent=True) or {}
        cliente = cliente_controller.crear(
            datos.get("nombre"),
            datos.get("email"),
            datos.get("telefono", ""),
            datos.get("puntos", 0),
        )
        if cliente is None:
            return jsonify({"error": "Datos del cliente invalidos o correo duplicado"}), 400
        return jsonify(serializar(cliente)), 201

    @bp.put("/<int:cliente_id>")
    def actualizar(cliente_id):
        datos = request.get_json(silent=True) or {}
        cliente = cliente_controller.actualizar(
            cliente_id,
            datos.get("nombre"),
            datos.get("email"),
            datos.get("telefono"),
            datos.get("puntos"),
        )
        if cliente is None:
            return jsonify({"error": "Cliente no encontrado o datos invalidos"}), 400
        return jsonify(serializar(cliente))

    @bp.delete("/<int:cliente_id>")
    def eliminar(cliente_id):
        if cliente_controller.eliminar(cliente_id):
            return jsonify({"ok": True, "mensaje": "Cliente eliminado"})
        return jsonify({"error": "Cliente no encontrado"}), 404

    return bp