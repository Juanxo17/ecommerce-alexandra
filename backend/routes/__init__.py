"""Paquete de rutas HTTP (capa de Controlador de alto nivel) de la tienda.

Cada modulo expone una fabrica crear_blueprint(controlador) que conecta un
endpoint REST con un metodo del controlador correspondiente. Las rutas
reciben los datos en JSON, los pasan al controlador (paso de parametros de
capa a capa) y devuelven la respuesta como JSON.
"""