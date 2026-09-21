# Documentación de los diagramas del proyecto

Este documento explica los tres artefactos de diseño que precedieron a la implementación,
dónde encontrarlos y cómo leerlos. Los tres describen el mismo sistema visto desde tres
ángulos complementarios: las clases (visión POO), la base de datos (visión de datos) y la
arquitectura (visión de capas).

| Archivo | Herramienta | Qué representa |
|---|---|---|
| `diagrama_clases_plantuml.puml` | plantuml.com | Las clases POO del Modelo y sus relaciones |
| `diagrama_bd.dbml` | dbdiagram.io | Las tablas de la base de datos SQLite |
| `diagrama_arquitectura.html` | navegador | La arquitectura MVC del sistema completo |

---

## 1. Diagrama de clases (PlantUML) — `diagrama_clases_plantuml.puml`


El diagrama muestra las cinco clases que forman el Modelo del sistema. Es la pieza central
del diseño porque es la evidencia directa de los conceptos de POO pedidos en el enunciado.
Cada clase se dibuja como una caja con tres zonas:

1. Nombre de la clase en la parte superior.
2. Atributos en el centro, precedidos del signo `-` (privados) o `+` (públicos).
3. Métodos en la parte inferior.

### Las cinco clases y su responsabilidad

**Categoria**
- Atributos: `id`, `nombre`, `descripcion` (privados).
- Métodos de acceso (`get_`/`set_`) y `es_valida()` que retorna un valor lógico.
- Agrupa los productos del catálogo. Un producto pertenece a una sola categoría.

**Producto**
- Atributos: `id`, `nombre`, `descripcion`, `precio_compra`, `precio_venta`, `stock` y una
  referencia a su `categoria` (acceso a un objeto ajeno).
- Métodos numéricos: `calcular_ganancia()` (precio_venta menos precio_compra) y
  `aplicar_descuento(porcentaje)` (retorna el precio con descuento).
- Métodos lógicos: `hay_stock_disponible(cantidad)` y `es_valido()`.
- Método mutador con efecto: `actualizar_stock(cantidad)` (resta existencias si hay).
- Destructor `__del__()`: deja evidencia en consola de cuándo el objeto se descarta.
- Es la clase del reabastecimiento y del precio; sobre ella se apoya el inventario.

**Cliente**
- Atributos: `id`, `nombre`, `email`, `telefono`, `puntos`.
- Métodos lógicos: `es_valido()` (datos básicos correctos) y `es_cliente_frecuente()`
  (alcanzó cierto umbral de puntos).
- Método numérico: `acumular_puntos(monto)` (calcula el nuevo saldo de puntos).

**Pedido**
- Atributos: `id`, `cliente` (referencia a un objeto Cliente), `fecha`, `estado`, `detalles`
  (lista de objetos DetallePedido).
- Métodos de composición: `agregar_producto(producto, cantidad)` y `confirmar()`, que
  reciben y manipulan objetos (uso explícito de objetos).
- Método numérico con condición: `calcular_total()` (aplica descuento si el cliente es
  frecuente).
- Método lógico: `cambiar_estado(nuevo_estado)` (valida las transiciones de estado).

**DetallePedido**
- Atributos: `id`, `producto` (referencia a un objeto Producto), `cantidad`,
  `precio_unitario`.
- Método numérico: `calcular_subtotal()` (cantidad por precio unitario).
- Representa una línea dentro de un pedido; es la pieza que une Pedido con Producto.

### Relaciones representadas

| Relación | Significado |
|---|---|
| `Categoria 1 — 0..* Producto` | Una categoría agrupa de cero a muchos productos |
| `Producto 1 — 0..* DetallePedido` | Un producto figura en muchas líneas de pedido |
| `Pedido 1 — 1..* DetallePedido` | Un pedido contiene una o más líneas |
| `Cliente 1 — 0..* Pedido` | Un cliente realiza de cero a muchos pedidos |

El signo `--` con asterisco indica el extremo "muchos" de la relación (cardinalidad). Los
rombitos `o--` y `*--` distinguen agregación (referencia opcional) de composición (el
DetallePedido no existe sin su Pedido).

---

## 2. Diagrama de base de datos (DBML) — `diagrama_bd.dbml`


Representa la persistencia real del sistema en SQLite: cinco tablas que son la traducción en
datos de las cinco clases del diagrama anterior.

| Tabla | Campos clave | Relación |
|---|---|---|
| `categorias` | `id`, `nombre`, `descripcion` | origen de la FK de productos |
| `productos` | `id`, `nombre`, `descripcion`, `precio_compra`, `precio_venta`, `stock`, `categoria_id` | `categoria_id` apunta a `categorias.id` |
| `clientes` | `id`, `nombre`, `email` (único), `telefono`, `puntos` | origen de la FK de pedidos |
| `pedidos` | `id`, `cliente_id`, `fecha`, `estado` | `cliente_id` apunta a `clientes.id` |
| `detalle_pedidos` | `id`, `pedido_id`, `producto_id`, `cantidad`, `precio_unitario` | FK a `pedidos.id` y `productos.id` |

La columna `puntos` de `clientes` alimenta el método `es_cliente_frecuente()`; la columna
`estado` de `pedidos` se controla desde la clase `Pedido`. El dbdiagram permitirá ver las
llaves primarias (PK) y foráneas (FK) y los enlaces entre tablas.

---

## 3. Diagrama de arquitectura (archify) — `diagrama_arquitectura.html`


Representa el sistema completo en tres capas MVC:

```
Frontend React (Vista)            -> navegador, consume la API
  Rutas Flask (Controlador HTTP)  -> recibe las peticiones y responde JSON
  Controladores                   -> lógica CRUD y validaciones
  Modelos POO                     -> las 5 clases de negocio
  Repositorio SQLite              -> traduce objetos a filas y viceversa
  Base de datos (tienda.db)       -> archivo local
```

Lectura: la petición viaja desde la Vista (frontend) hacia el backend, atraviesa la capa de
Controlador, se resuelve en los Modelos y termina en la base de datos. Las dos cajas sombreadas
del lado derecho resumen qué evidencia cada grupo de capas: la separación Modelo-Vista-Controlador
y la persistencia.

Este diagrama es la evidencia del requisito de arquitectura MVC y de ampliabilidad: cada capa
se puede modificar o crecer sin tocar las demás.

---

## 4. Cómo se relacionan los tres diagramas

- El diagrama de clases dice qué objetos existen y qué pueden hacer (visión de código).
- El diagrama de base de datos dice dónde y cómo se guardan esos objetos (visión de datos).
- El diagrama de arquitectura dice en qué capa vive cada pieza y cómo fluye una petición
  (visión de sistema).

La coherencia entre los tres es lo que permite que un cambio de diseño (por ejemplo, agregar
una nueva categoría o un nuevo estado de pedido) se pueda rastrear desde la clase hasta la
tabla y hasta la capa correspondiente sin romper el resto.