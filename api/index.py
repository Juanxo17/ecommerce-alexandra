"""Punto de entrada del deploy en Vercel (modo demo).

En Vercel el preset de Flask (detectado por requirements.txt) atiende TODAS
las rutas del proyecto, asi que esta app:
  1. Expone el backend Flask de la tienda en /api/* (mismo codigo de
     backend.app, sin cambios).
  2. Sirve el frontend compilado (frontend/dist) desde Flask.

Modo demo de la base de datos: en serverless el filesystem es efimero, por
eso la base tienda.db del repo se copia a /tmp al arrancar. Asi la tienda
online se ve con los productos (y fotos) del repositorio, pero los cambios
(crear/editar/eliminar) se pierden al reiniciar la funcion, tal como se le
indicarias a un invitado en una demo. En local no se toca nada: usa
database/tienda.db igual que siempre.
"""

import os
import shutil

from flask import abort, send_from_directory

from backend.app import crear_app

RUTA_DB_REPO = os.path.join("database", "tienda.db")
RUTA_FRONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")

RUTA_DB = RUTA_DB_REPO
SEMBRAR = False

if os.environ.get("VERCEL"):
    copia_tmp = os.path.join("/tmp", "tienda.db")
    if os.path.exists(RUTA_DB_REPO) and not os.path.exists(copia_tmp):
        try:
            shutil.copyfile(RUTA_DB_REPO, copia_tmp)
        except OSError:
            copia_tmp = None
    if copia_tmp and os.path.exists(copia_tmp):
        RUTA_DB = copia_tmp
        SEMBRAR = False
    else:
        RUTA_DB = copia_tmp or RUTA_DB_REPO
        SEMBRAR = True

app = crear_app(ruta_base_datos=RUTA_DB, sembrar=SEMBRAR)


@app.get("/")
def _indice():
    return send_from_directory(RUTA_FRONT, "index.html")


@app.get("/<path:ruta_archivo>")
def _estaticos(ruta_archivo):
    if os.path.isfile(os.path.join(RUTA_FRONT, ruta_archivo)):
        return send_from_directory(RUTA_FRONT, ruta_archivo)
    if os.path.isfile(os.path.join(RUTA_FRONT, "index.html")):
        return send_from_directory(RUTA_FRONT, "index.html")
    abort(404)