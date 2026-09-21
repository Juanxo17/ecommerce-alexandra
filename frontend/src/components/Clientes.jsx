import { useEffect, useState } from "react";
import { apiClientes } from "../api";

export default function Clientes() {
  const [clientes, setClientes] = useState([]);
  const [form, setForm] = useState({ id: null, nombre: "", email: "", telefono: "" });
  const [mensaje, setMensaje] = useState("");

  const cargar = async () => {
    const { datos } = await apiClientes.listar();
    setClientes(datos);
  };

  useEffect(() => {
    cargar();
  }, []);

  const guardar = async (e) => {
    e.preventDefault();
    const cuerpo = { nombre: form.nombre, email: form.email, telefono: form.telefono };
    const resultado = form.id
      ? await apiClientes.actualizar(form.id, cuerpo)
      : await apiClientes.crear(cuerpo);
    if (resultado.estado === 200 || resultado.estado === 201) {
      setMensaje(form.id ? "Cliente actualizado" : "Cliente creado");
      setForm({ id: null, nombre: "", email: "", telefono: "" });
      cargar();
    } else {
      setMensaje(resultado.datos.error || "No se pudo guardar el cliente");
    }
  };

  const editar = (c) => setForm({ id: c.id, nombre: c.nombre, email: c.email, telefono: c.telefono });

  const eliminar = async (id) => {
    const resultado = await apiClientes.eliminar(id);
    setMensaje(resultado.estado === 200 ? "Cliente eliminado" : resultado.datos.error);
    cargar();
  };

  return (
    <div className="card shadow-sm border-0">
      <div className="card-body">
        <h2 className="mb-3">Clientes</h2>
        <form onSubmit={guardar} className="row g-2 mb-3">
          <div className="col-md-4">
            <input
              className="form-control"
              placeholder="Nombre"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            />
          </div>
          <div className="col-md-4">
            <input
              className="form-control"
              placeholder="Correo electronico"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </div>
          <div className="col-md-4">
            <input
              className="form-control"
              placeholder="Telefono"
              value={form.telefono}
              onChange={(e) => setForm({ ...form, telefono: e.target.value })}
            />
          </div>
          <div className="col-12 d-flex gap-2">
            <button type="submit" className="btn btn-primary">
              {form.id ? "Actualizar" : "Crear"}
            </button>
            {form.id && (
              <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={() => setForm({ id: null, nombre: "", email: "", telefono: "" })}
              >
                Cancelar
              </button>
            )}
          </div>
        </form>
        {mensaje && <div className="alert alert-primary py-2">{mensaje}</div>}
        <div className="table-responsive">
          <table className="table table-striped table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Email</th>
                <th>Telefono</th>
                <th>Puntos</th>
                <th>Frecuente</th>
                <th className="text-end">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {clientes.map((c) => (
                <tr key={c.id}>
                  <td>{c.id}</td>
                  <td>{c.nombre}</td>
                  <td>{c.email}</td>
                  <td>{c.telefono}</td>
                  <td>{c.puntos}</td>
                  <td>
                    {c.es_frecuente ? (
                      <span className="badge text-bg-success">Si</span>
                    ) : (
                      <span className="badge text-bg-secondary">No</span>
                    )}
                  </td>
                  <td className="text-end tabla-acciones">
                    <button type="button" className="btn btn-sm btn-outline-primary" onClick={() => editar(c)}>
                      Editar
                    </button>
                    <button
                      type="button"
                      className="btn btn-sm btn-outline-danger"
                      onClick={() => eliminar(c.id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}