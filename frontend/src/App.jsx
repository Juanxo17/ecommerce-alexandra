import { useState } from "react";
import "./theme.css";
import Categorias from "./components/Categorias";
import Clientes from "./components/Clientes";
import Pedidos from "./components/Pedidos";
import Productos from "./components/Productos";

const PESTANAS = [
  { id: "categorias", nombre: "Categorias", componente: Categorias, descripcion: "Organiza la despensa" },
  { id: "productos", nombre: "Productos", componente: Productos, descripcion: "Catalogo e inventario" },
  { id: "clientes", nombre: "Clientes", componente: Clientes, descripcion: "Tus compradores habituales" },
  { id: "pedidos", nombre: "Pedidos", componente: Pedidos, descripcion: "Ventas y estados" },
];

function App() {
  const [activa, setActiva] = useState("categorias");

  const pestanaActual = PESTANAS.find((p) => p.id === activa);
  const Vista = pestanaActual.componente;

  return (
    <div className="d-flex flex-column min-vh-100">
      <nav className="navbar navbar-expand navbar-dark shadow">
        <div className="container">
          <span className="navbar-brand">
            <span className="marca-icono" aria-hidden="true">
              <svg viewBox="0 0 32 32" width="21" height="21" fill="none" aria-hidden="true">
                <g stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M16 20.8 V 15.6" />
                  <path d="M16 16 C 12.5 15.6 10.3 13.8 9.1 10.8" />
                  <path d="M16 16 C 19.5 15.6 21.7 13.8 22.9 10.8" />
                  <path d="M10.4 21 H 21.6" />
                  <path d="M11.4 21 L 12.1 24.8" />
                  <path d="M20.6 21 L 19.9 24.8" />
                  <path d="M12.1 24.8 Q 16 26.1 19.9 24.8" />
                  <path d="M12.4 22.8 H 19.6" />
                </g>
              </svg>
            </span>
            Verde <span className="marca-acento">Mercado</span>
          </span>
          <ul className="navbar-nav ms-auto gap-1">
            {PESTANAS.map((p) => (
              <li className="nav-item" key={p.id}>
                <button
                  type="button"
                  className={`nav-link btn ${p.id === activa ? "active" : ""}`}
                  onClick={() => setActiva(p.id)}
                >
                  {p.nombre}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </nav>

      <main className="container flex-grow-1">
        <section className="hero-band">
          <h1 className="hero-titulo">{pestanaActual.nombre}</h1>
          <p className="hero-subtitulo">{pestanaActual.descripcion}</p>
        </section>
        <section className="py-4">
          <div className="pestana-contenido">
            <Vista />
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;