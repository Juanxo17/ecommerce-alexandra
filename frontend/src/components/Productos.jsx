import { useEffect, useState } from "react";
import { apiCategorias, apiProductos } from "../api";

function Miniatura({ src, nombre }) {
  const [fallo, setFallo] = useState(false);
  const inicial = (nombre || "?").trim().charAt(0).toUpperCase();

  if (!src || fallo) {
    return (
      <span className="mini-lugar" role="img" aria-label={nombre}>
        {inicial}
      </span>
    );
  }
  return (
    <img className="mini-foto" src={src} alt={nombre} loading="lazy" onError={() => setFallo(true)} />
  );
}

const FORM_VACIO = {
  id: null,
  nombre: "",
  descripcion: "",
  precio_compra: "",
  precio_venta: "",
  stock: "",
  categoria_id: "",
  imagen: "",
};

export default function Productos() {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [filtro, setFiltro] = useState("");
  const [form, setForm] = useState(FORM_VACIO);
  const [mensaje, setMensaje] = useState("");

  const cargar = async (categoria) => {
    const { datos } = categoria
      ? await apiProductos.listarPorCategoria(categoria)
      : await apiProductos.listar();
    setProductos(datos);
  };

  useEffect(() => {
    cargar("");
    const iniciar = async () => {
      const { datos } = await apiCategorias.listar();
      setCategorias(datos);
    };
    iniciar();
  }, []);

  const cambiarFiltro = (e) => {
    setFiltro(e.target.value);
    cargar(e.target.value);
  };

  const onElegirFoto = (e) => {
    const archivo = e.target.files?.[0];
    if (!archivo) return;
    const lector = new FileReader();
    lector.onload = () => setForm((prev) => ({ ...prev, imagen: lector.result }));
    lector.readAsDataURL(archivo);
  };

  const guardar = async (e) => {
    e.preventDefault();
    const cuerpo = {
      nombre: form.nombre,
      descripcion: form.descripcion,
      precio_compra: Number(form.precio_compra),
      precio_venta: Number(form.precio_venta),
      stock: Number(form.stock),
      categoria_id: form.categoria_id ? Number(form.categoria_id) : null,
      imagen: form.imagen,
    };
    const resultado = form.id
      ? await apiProductos.actualizar(form.id, cuerpo)
      : await apiProductos.crear(cuerpo);
    if (resultado.estado === 200 || resultado.estado === 201) {
      setMensaje(form.id ? "Producto actualizado" : "Producto creado");
      setForm(FORM_VACIO);
      cargar(filtro);
    } else {
      setMensaje(resultado.datos.error || "No se pudo guardar el producto");
    }
  };

  const editar = (p) =>
    setForm({
      id: p.id,
      nombre: p.nombre,
      descripcion: p.descripcion,
      precio_compra: String(p.precio_compra),
      precio_venta: String(p.precio_venta),
      stock: String(p.stock),
      categoria_id: String(p.categoria_id ?? ""),
      imagen: p.imagen ?? "",
    });

  const eliminar = async (id) => {
    const resultado = await apiProductos.eliminar(id);
    setMensaje(resultado.estado === 200 ? "Producto eliminado" : resultado.datos.error);
    cargar(filtro);
  };

  const inicialForm = (form.nombre || "?").trim().charAt(0).toUpperCase();

  return (
    <div className="card shadow-sm border-0">
      <div className="card-body">
        <h2 className="mb-3">Productos</h2>
        <div className="d-flex gap-3 align-items-center mb-3">
          <label className="form-label mb-0">Filtrar por categoria:</label>
          <select className="form-select w-auto" value={filtro} onChange={cambiarFiltro}>
            <option value="">Todas</option>
            {categorias.map((c) => (
              <option key={c.id} value={c.id}>{c.nombre}</option>
            ))}
          </select>
        </div>

        <form onSubmit={guardar} className="row g-3 mb-3">
          <div className="col-md-6">
            <label className="form-label" htmlFor="prod-nombre">Nombre</label>
            <input
              id="prod-nombre"
              className="form-control"
              placeholder="Ej: Harina 1 kg"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            />
          </div>
          <div className="col-md-6">
            <label className="form-label" htmlFor="prod-descripcion">Descripcion</label>
            <input
              id="prod-descripcion"
              className="form-control"
              placeholder="Breve detalle del producto"
              value={form.descripcion}
              onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
            />
          </div>
          <div className="col-md-3">
            <label className="form-label" htmlFor="prod-compra">Precio de compra</label>
            <input
              id="prod-compra"
              className="form-control"
              type="number"
              min="0"
              placeholder="2500"
              value={form.precio_compra}
              onChange={(e) => setForm({ ...form, precio_compra: e.target.value })}
            />
          </div>
          <div className="col-md-3">
            <label className="form-label" htmlFor="prod-venta">Precio de venta</label>
            <input
              id="prod-venta"
              className="form-control"
              type="number"
              min="0"
              placeholder="3200"
              value={form.precio_venta}
              onChange={(e) => setForm({ ...form, precio_venta: e.target.value })}
            />
          </div>
          <div className="col-md-3">
            <label className="form-label" htmlFor="prod-stock">Stock</label>
            <input
              id="prod-stock"
              className="form-control"
              type="number"
              min="0"
              placeholder="40"
              value={form.stock}
              onChange={(e) => setForm({ ...form, stock: e.target.value })}
            />
          </div>
          <div className="col-md-3">
            <label className="form-label" htmlFor="prod-categoria">Categoria</label>
            <select
              id="prod-categoria"
              className="form-select"
              value={form.categoria_id}
              onChange={(e) => setForm({ ...form, categoria_id: e.target.value })}
            >
              <option value="">Sin categoria</option>
              {categorias.map((c) => (
                <option key={c.id} value={c.id}>{c.nombre}</option>
              ))}
            </select>
          </div>
          <div className="col-md-6">
            <label className="form-label" htmlFor="foto-producto">Foto del producto</label>
            <label className="selector-foto d-flex align-items-center gap-3 w-100" htmlFor="foto-producto">
              {form.imagen ? (
                <img className="vista-previa" src={form.imagen} alt="Vista previa del producto" />
              ) : (
                <span className="mini-lugar" role="img" aria-hidden="true">{inicialForm}</span>
              )}
              <span className="small text-secondary">
                {form.imagen
                  ? "Listo: tu foto quedo adjunta"
                  : "Haz click y elige una imagen para el producto"}
              </span>
            </label>
            <input
              id="foto-producto"
              type="file"
              accept="image/*"
              className="d-none"
              onChange={onElegirFoto}
            />
            {form.imagen && (
              <button
                type="button"
                className="btn btn-sm btn-outline-secondary mt-2"
                onClick={() => setForm({ ...form, imagen: "" })}
              >
                Quitar foto
              </button>
            )}
          </div>
          <div className="col-12 d-flex gap-2 align-items-end">
            <button type="submit" className="btn btn-primary">
              {form.id ? "Actualizar" : "Crear"}
            </button>
            {form.id && (
              <button type="button" className="btn btn-outline-secondary" onClick={() => setForm(FORM_VACIO)}>
                Cancelar
              </button>
            )}
          </div>
        </form>

        {mensaje && <div className="alert alert-primary py-2">{mensaje}</div>}

        <div className="table-responsive">
          <table className="table table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>ID</th>
                <th>Foto</th>
                <th>Nombre</th>
                <th>Categoria</th>
                <th>Compra</th>
                <th>Venta</th>
                <th>Stock</th>
                <th className="text-end">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {productos.map((p) => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td><Miniatura src={p.imagen} nombre={p.nombre} /></td>
                  <td>{p.nombre}</td>
                  <td>{p.categoria ?? "-"}</td>
                  <td>{p.precio_compra}</td>
                  <td>{p.precio_venta}</td>
                  <td>{p.stock}</td>
                  <td className="text-end tabla-acciones">
                    <button type="button" className="btn btn-sm btn-outline-primary" onClick={() => editar(p)}>
                      Editar
                    </button>
                    <button
                      type="button"
                      className="btn btn-sm btn-outline-danger"
                      onClick={() => eliminar(p.id)}
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