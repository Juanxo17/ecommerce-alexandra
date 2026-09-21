const BASE = "/api";

async function pedir(url, opciones = {}) {
  const respuesta = await fetch(`${BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  const datos = await respuesta.json();
  return { estado: respuesta.status, datos };
}

export const apiCategorias = {
  listar: () => pedir("/categorias"),
  obtener: (id) => pedir(`/categorias/${id}`),
  crear: (cuerpo) => pedir("/categorias", { method: "POST", body: JSON.stringify(cuerpo) }),
  actualizar: (id, cuerpo) => pedir(`/categorias/${id}`, { method: "PUT", body: JSON.stringify(cuerpo) }),
  eliminar: (id) => pedir(`/categorias/${id}`, { method: "DELETE" }),
};

export const apiProductos = {
  listar: () => pedir("/productos"),
  listarPorCategoria: (id) => pedir(`/productos?categoria=${id}`),
  obtener: (id) => pedir(`/productos/${id}`),
  crear: (cuerpo) => pedir("/productos", { method: "POST", body: JSON.stringify(cuerpo) }),
  actualizar: (id, cuerpo) => pedir(`/productos/${id}`, { method: "PUT", body: JSON.stringify(cuerpo) }),
  eliminar: (id) => pedir(`/productos/${id}`, { method: "DELETE" }),
};

export const apiClientes = {
  listar: () => pedir("/clientes"),
  obtener: (id) => pedir(`/clientes/${id}`),
  crear: (cuerpo) => pedir("/clientes", { method: "POST", body: JSON.stringify(cuerpo) }),
  actualizar: (id, cuerpo) => pedir(`/clientes/${id}`, { method: "PUT", body: JSON.stringify(cuerpo) }),
  eliminar: (id) => pedir(`/clientes/${id}`, { method: "DELETE" }),
};

export const apiPedidos = {
  listar: () => pedir("/pedidos"),
  obtener: (id) => pedir(`/pedidos/${id}`),
  crear: (cuerpo) => pedir("/pedidos", { method: "POST", body: JSON.stringify(cuerpo) }),
  agregarProducto: (id, cuerpo) =>
    pedir(`/pedidos/${id}/productos`, { method: "POST", body: JSON.stringify(cuerpo) }),
  confirmar: (id) => pedir(`/pedidos/${id}/confirmar`, { method: "POST" }),
  cambiarEstado: (id, cuerpo) =>
    pedir(`/pedidos/${id}/estado`, { method: "PUT", body: JSON.stringify(cuerpo) }),
  eliminar: (id) => pedir(`/pedidos/${id}`, { method: "DELETE" }),
};