"""Rutas de pedidos: conectan HTTP con PedidoController.

Además del CRUD expone las operaciones de negocio del pedido: agregar
productos, confirmar y cambiar el estado.
"""

from flask import Blueprint, jsonify, request


def crear_blueprint(pedido_controller):
    """Fabrica el Blueprint de pedidos con endpoints REST."""

    bp = Blueprint("pedidos", __name__, url_prefix="/api/pedidos")

    def serializar(pedido):
        detalles = []
        for detalle in pedido.get_detalles():
            producto = detalle.get_producto()
            detalles.append({
                "producto_id": producto.get_id(),
                "producto": producto.get_nombre(),
                "cantidad": detalle.get_cantidad(),
                "precio_unitario": detalle.get_precio_unitario(),
                "subtotal": detalle.calcular_subtotal(),
            })
        return {
            "id": pedido.get_id(),
            "cliente_id": pedido.get_cliente().get_id(),
            "cliente": pedido.get_cliente().get_nombre(),
            "fecha": pedido.get_fecha(),
            "estado": pedido.get_estado(),
            "total": pedido.calcular_total(),
            "detalles": detalles,
        }

    @bp.get("")
    def listar():
        return jsonify([serializar(p) for p in pedido_controller.listar()])

    @bp.get("/<int:pedido_id>")
    def obtener(pedido_id):
        pedido = pedido_controller.obtener_por_id(pedido_id)
        if pedido is None:
            return jsonify({"error": "Pedido no encontrado"}), 404
        return jsonify(serializar(pedido))

    @bp.post("")
    def crear():
        datos = request.get_json(silent=True) or {}
        pedido = pedido_controller.crear(datos.get("cliente_id"), datos.get("fecha"))
        if pedido is None:
            return jsonify({"error": "Cliente inexistente o fecha vacia"}), 400
        return jsonify(serializar(pedido)), 201

    @bp.post("/<int:pedido_id>/productos")
    def agregar_producto(pedido_id):
        datos = request.get_json(silent=True) or {}
        if pedido_controller.agregar_producto(
            pedido_id, datos.get("producto_id"), datos.get("cantidad", 0),
        ):
            return jsonify(serializar(pedido_controller.obtener_por_id(pedido_id)))
        return jsonify({"error": "Stock insuficiente, pedido confirmado o datos invalidos"}), 400

    @bp.post("/<int:pedido_id>/confirmar")
    def confirmar(pedido_id):
        if pedido_controller.confirmar(pedido_id):
            return jsonify(serializar(pedido_controller.obtener_por_id(pedido_id)))
        return jsonify({"error": "El pedido no puede confirmarse"}), 400

    @bp.put("/<int:pedido_id>/estado")
    def cambiar_estado(pedido_id):
        datos = request.get_json(silent=True) or {}
        if pedido_controller.cambiar_estado(pedido_id, datos.get("estado")):
            return jsonify(serializar(pedido_controller.obtener_por_id(pedido_id)))
        return jsonify({"error": "Estado invalido o pedido inexistente"}), 400

    @bp.delete("/<int:pedido_id>")
    def eliminar(pedido_id):
        if pedido_controller.eliminar(pedido_id):
            return jsonify({"ok": True, "mensaje": "Pedido eliminado"})
        return jsonify({"error": "Pedido no encontrado"}), 404

    return bp