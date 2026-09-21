import { useEffect, useState } from "react";
import { apiCategorias } from "../api";

export default function Categorias() {
  const [categorias, setCategorias] = useState([]);
  const [form, setForm] = useState({ id: null, nombre: "", descripcion: "" });
  const [mensaje, setMensaje] = useState("");

  const cargar = async () => {
    const { datos } = await apiCategorias.listar();
    setCategorias(datos);
  };

  useEffect(() => {
    cargar();
  }, []);

  const guardar = async (e) => {
    e.preventDefault();
    const cuerpo = { nombre: form.nombre, descripcion: form.descripcion };
    const resultado = form.id
      ? await apiCategorias.actualizar(form.id, cuerpo)
      : await apiCategorias.crear(cuerpo);
    if (resultado.estado === 200 || resultado.estado === 201) {
      setMensaje(form.id ? "Categoria actualizada" : "Categoria creada");
      setForm({ id: null, nombre: "", descripcion: "" });
      cargar();
    } else {
      setMensaje(resultado.datos.error || "No se pudo guardar la categoria");
    }
  };

  const editar = (c) => setForm({ id: c.id, nombre: c.nombre, descripcion: c.descripcion });

  const eliminar = async (id) => {
    const resultado = await apiCategorias.eliminar(id);
    setMensaje(resultado.estado === 200 ? "Categoria eliminada" : resultado.datos.error);
    cargar();
  };

  return (
    <div className="card shadow-sm border-0">
      <div className="card-body">
        <h2 className="mb-3">Categorias</h2>
        <form onSubmit={guardar} className="row g-2 mb-3">
          <div className="col-md-6">
            <input
              className="form-control"
              placeholder="Nombre"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            />
          </div>
          <div className="col-md-6">
            <input
              className="form-control"
              placeholder="Descripcion"
              value={form.descripcion}
              onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
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
                onClick={() => setForm({ id: null, nombre: "", descripcion: "" })}
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
                <th>Descripcion</th>
                <th className="text-end">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {categorias.map((c) => (
                <tr key={c.id}>
                  <td>{c.id}</td>
                  <td>{c.nombre}</td>
                  <td>{c.descripcion}</td>
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