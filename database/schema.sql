-- Esquema de la base de datos SQLite de la Tienda CRUD.
-- Traduccion en tablas de las cinco clases POO del sistema.

CREATE TABLE IF NOT EXISTS categorias (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL,
    descripcion TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS productos (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT NOT NULL,
    descripcion   TEXT NOT NULL DEFAULT '',
    precio_compra INTEGER NOT NULL,
    precio_venta  INTEGER NOT NULL,
    stock         INTEGER NOT NULL DEFAULT 0,
    categoria_id  INTEGER,
    imagen        TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE IF NOT EXISTS clientes (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre   TEXT NOT NULL,
    email    TEXT NOT NULL UNIQUE,
    telefono TEXT NOT NULL DEFAULT '',
    puntos   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pedidos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    fecha      TEXT NOT NULL,
    estado     TEXT NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS detalle_pedidos (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id      INTEGER NOT NULL,
    producto_id    INTEGER NOT NULL,
    cantidad       INTEGER NOT NULL,
    precio_unitario INTEGER NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);