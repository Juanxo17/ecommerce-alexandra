-- Datos iniciales de demostracion de la Tienda CRUD.
-- Categorias, productos y clientes de ejemplo para iniciar la tienda.

INSERT INTO categorias (nombre, descripcion) VALUES
    ('Abarrotes', 'Despensa y alimentacion'),
    ('Lacteos', 'Leche y derivados'),
    ('Aseo', 'Limpieza e higiene');

INSERT INTO productos (nombre, descripcion, precio_compra, precio_venta, stock, categoria_id, imagen) VALUES
    ('Arroz 1 kg',        'Arroz blanco de grano largo',          2500, 3200,  40, 1, 'https://picsum.photos/seed/arroz/600/400'),
    ('Aceite 900 ml',     'Aceite vegetal para cocinar',           7000, 9200, 400, 1, 'https://picsum.photos/seed/aceite/600/400'),
    ('Leche entera 1 L',  'Leche de vaca entera',                  3000, 3800, 120, 2, 'https://picsum.photos/seed/leche/600/400'),
    ('Jabon de manos',    'Jabon liquido para las manos',          4500, 5900, 200, 3, 'https://picsum.photos/seed/jabon/600/400');

INSERT INTO clientes (nombre, email, telefono, puntos) VALUES
    ('Ana Torres', 'ana.torres@correo.com', '3000000001',  40),
    ('Luis Mora',  'luis.mora@correo.com',  '3000000002', 150),
    ('Perla Rios', 'perla.rios@correo.com', '3000000003',   0);