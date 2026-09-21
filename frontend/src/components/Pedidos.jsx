import { useEffect, useState } from "react";
import { apiClientes, apiPedidos, apiProductos } from "../api";

const ESTADOS = ["Pendiente", "Confirmado", "Entregado", "Cancelado"];

const CLASE_ESTADO = {
  Pendiente: "text-bg-warning",
  Confirmado: "text-bg-success",
  Entregado: "text-bg-primary",
  Cancelado: "text-bg-secondary",
};

function TarjetaPedido({ pedido, productos, onCambio, setMensaje }) {
  const [productoId, setProductoId] = useState("");
  const [cantidad, setCantidad] = useState("1");
  const [estadoNuevo, setEstadoNuevo] = useState(pedido.estado);

  const agregarProducto = async (e) => {
    e.preventDefault();
    const resultado = await apiPedidos.agregarProducto(pedido.id, {
      producto_id: Number(productoId),
      cantidad: Number(cantidad),
    });
    if (resultado.estado === 200) {
      setMensaje("Producto agregado al pedido");
      setCantidad("1");
      onCambio();
    } else {
      setMensaje(resultado.datos.error || "No se pudo agregar el producto");
    }
  };

  const confirmar = async () => {
    const resultado = await apiPedidos.confirmar(pedido.id);
    setMensaje(resultado.estado === 200 ? "Pedido confirmado" : resultado.datos.error);
    onCambio();
  };

  const cambiarEstado = async () => {
    const resultado = await apiPedidos.cambiarEstado(pedido.id, { estado: estadoNuevo });
    setMensaje(resultado.estado === 200 ? "Estado actualizado" : resultado.datos.error);
    onCambio();
  };

  const eliminar = async () => {
    const resultado = await apiPedidos.eliminar(pedido.id);
    setMensaje(resultado.estado === 200 ? "Pedido eliminado" : resultado.datos.error);
    onCambio();
  };

  return (
    <div className="card shadow-sm border-0 mb-3">
      <div className="card-header bg-white d-flex justify-content-between align-items-center flex-wrap gap-2">
        <h5 className="mb-0">Pedido #{pedido.id} — {pedido.cliente}</h5>
        <span className={`badge estado-badge ${CLASE_ESTADO[pedido.estado] || "text-bg-secondary"}`}>
          {pedido.estado}
        </span>
      </div>
      <div className="card-body">
        <p className="text-muted mb-2">
          Fecha: {pedido.fecha} | Total: <strong>{pedido.total}</strong>
        </p>

        <ul className="list-group list-group-flush mb-3">
          {pedido.detalles.length === 0 && (
            <li className="list-group-item">Sin productos aun</li>
          )}
          {pedido.detalles.map((d, i) => (
            <li className="list-group-item" key={i}>
              {d.cantidad} x {d.producto} (a {d.precio_unitario}) = <strong>{d.subtotal}</strong>
            </li>
          ))}
        </ul>

        {pedido.estado === "Pendiente" && (
          <form onSubmit={agregarProducto} className="row g-2 mb-3">
            <div className="col-md-6">
              <select
                className="form-select"
                value={productoId}
                onChange={(e) => setProductoId(e.target.value)}
                required
              >
                <option value="">Elegir producto</option>
                {productos.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.nombre} (stock {p.stock})
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-2">
              <input
                className="form-control"
                type="number"
                min="1"
                value={cantidad}
                onChange={(e) => setCantidad(e.target.value)}
              />
            </div>
            <div className="col-md-4 d-flex gap-2">
              <button type="submit" className="btn btn-primary btn-sm">Agregar</button>
              <button type="button" className="btn btn-success btn-sm" onClick={confirmar}>
                Confirmar
              </button>
            </div>
          </form>
        )}
        <div className="d-flex gap-2 flex-wrap">
          <select
            className="form-select w-auto"
            value={estadoNuevo}
            onChange={(e) => setEstadoNuevo(e.target.value)}
          >
            {ESTADOS.map((e) => (
              <option key={e} value={e}>{e}</option>
            ))}
          </select>
          <button
            type="button"
            className="btn btn-outline-primary btn-sm"
            onClick={cambiarEstado}
          >
            Cambiar estado
          </button>
          <button type="button" className="btn btn-outline-danger btn-sm" onClick={eliminar}>
            Eliminar
          </button>
        </div>
      </div>
    </div>
  );
}

export default function Pedidos() {
  const [pedidos, setPedidos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [productos, setProductos] = useState([]);
  const [clienteId, setClienteId] = useState("");
  const [fecha, setFecha] = useState("");
  const [mensaje, setMensaje] = useState("");

  const cargar = async () => {
    const [respPedidos, respClientes, respProductos] = await Promise.all([
      apiPedidos.listar(),
      apiClientes.listar(),
      apiProductos.listar(),
    ]);
    setPedidos(respPedidos.datos);
    setClientes(respClientes.datos);
    setProductos(respProductos.datos);
  };

  useEffect(() => {
    cargar();
  }, []);

  const crearPedido = async (e) => {
    e.preventDefault();
    const resultado = await apiPedidos.crear({ cliente_id: Number(clienteId), fecha });
    if (resultado.estado === 201) {
      setMensaje("Pedido creado");
      setClienteId("");
      setFecha("");
      cargar();
    } else {
      setMensaje(resultado.datos.error || "No se pudo crear el pedido");
    }
  };

  return (
    <div className="card shadow-sm border-0">
      <div className="card-body">
        <h2 className="mb-3">Nuevo pedido</h2>
        <form onSubmit={crearPedido} className="row g-2 mb-4">
          <div className="col-md-6">
            <select className="form-select" value={clienteId} onChange={(e) => setClienteId(e.target.value)} required>
              <option value="">Elegir cliente</option>
              {clientes.map((c) => (
                <option key={c.id} value={c.id}>{c.nombre}</option>
              ))}
            </select>
          </div>
          <div className="col-md-4">
            <input
              className="form-control"
              type="date"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
              required
            />
          </div>
          <div className="col-md-2">
            <button type="submit" className="btn btn-primary w-100">Crear pedido</button>
          </div>
        </form>
        {mensaje && <div className="alert alert-primary py-2">{mensaje}</div>}

        <h5 className="mb-3">Pedidos ({pedidos.length})</h5>
        {pedidos.map((p) => (
          <TarjetaPedido
            key={p.id}
            pedido={p}
            productos={productos}
            onCambio={cargar}
            setMensaje={setMensaje}
          />
        ))}
      </div>
    </div>
  );
}