# Tienda CRUD (POO)

Taller académico de **Programación Orientada a Objetos**: sistema CRUD de una tienda
(categorías, productos, clientes y pedidos) construido en capas **MVC**.

```
Vista (React/Vite)  →  API REST (Flask)  →  Controladores  →  Modelos (POO)  →  Base de datos (SQLite)
```

## Características

- **Modelo** en Python con 5 clases orientadas a objetos: `Categoria`, `Producto`,
  `Cliente`, `Pedido` y `DetallePedido` (atributos, constructor, métodos, sobrecarga de
  `__str__`/`__repr__`, destructor de demostración y cálculo de totales y descuentos).
- **Controladores** con CRUD completo y validaciones (correo, precios, stock, estados).
- **Persistencia en SQLite**: clases que se guardan y se reconstruyen desde tablas
  relacionales (`clientes`, `productos`, `pedidos`, `detalle_pedidos`).
- **API REST** con Flask: `/api/categorias`, `/api/productos`, `/api/clientes` y
  `/api/pedidos`.
- **Vista** con Vite + React: pestañas para cada entidad, formularios crear/editar,
  filtros y flujo completo de pedidos.

## Requisitos

- Python 3.10+ y Flask (`pip install flask`)
- Node.js 20+ (npm)
- SQLite: incluida en Python (no requiere instalación)

## Puesta en marcha

La base de datos se crea sola en el primer arranque (con datos de demostración), así que
solo hay que levantar los dos servidores.

Backend (terminal 1, desde la raíz del proyecto):

```
pip install flask
python -m backend.app
```

Debe quedar escuchando en `http://127.0.0.1:5000`. Para comprobar que responde:

```
curl http://127.0.0.1:5000/api/estado
```

Frontend (terminal 2, dentro de la carpeta `frontend/`):

```
npm install
npm run dev
```

Abrir `http://localhost:5173`. El puerto 5173 reenvía las llamadas `/api/*` al backend
(configurado en `frontend/vite.config.js`). La primera vez que se arranca, `backend/app.py`
crea `database/tienda.db` aplicando `database/schema.sql` y la rellena con `database/seed.sql`
(categorías, productos, clientes y pedidos de demostración).

## Estructura del aplicativo

```
Taller_CRUD_Tienda_POO/
├── README.md
├── Evidencias_Conceptos_POO.pdf   ← evidencias del enunciado (capturas)
├── backend/                       ← API REST, MVC
│   ├── app.py
│   ├── models/                    ← capa Modelo (clases POO)
│   ├── controllers/               ← validaciones y reglas de negocio
│   ├── data/                      ← repositorio SQLite
│   └── routes/                    ← endpoints de la API
├── frontend/                      ← capa Vista (React + Vite + Bootstrap)
│   ├── vite.config.js
│   └── src/
│       ├── api.js
│       ├── App.jsx
│       ├── theme.css
│       └── components/
├── database/
│   ├── schema.sql                 ← tablas relacionales
│   └── seed.sql                   ← datos de demostración
└── docs/
    └── diagramas/                 ← diagramas UML, de BD y de arquitectura
```

## Evidencias del enunciado

El archivo `Evidencias_Conceptos_POO.pdf` recorre los nueve temas pedidos (clase, atributos,
métodos, constructor, paso de parámetros, retorno numérico y lógico, uso de objetos, MVC y
condicionales) indicando dónde se demuestra cada uno en el código, con espacio para pegar la
captura de pantalla correspondiente.