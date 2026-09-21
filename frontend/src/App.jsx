import { useState } from "react";
import logo from "./assets/logo.jpg";
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
            <img className="marca-logo" src={logo} alt="Verde Mercado" />
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