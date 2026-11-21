"""Excepciones propias de la aplicación.

Tener excepciones específicas permite que la interfaz distinga entre
"el usuario hizo algo inválido" y "ocurrió un error inesperado", y muestre
un mensaje claro sin que el programa se cierre.
"""


class ErrorEditor(Exception):
    """Clase base de todos los errores previsibles del editor."""


class ImagenNoCargadaError(ErrorEditor):
    """Se intentó operar sin haber cargado una imagen."""


class ArchivoInvalidoError(ErrorEditor):
    """El archivo no existe, no es una imagen o no se puede leer/guardar."""


class ParametroInvalidoError(ErrorEditor):
    """Un parámetro numérico está fuera del rango permitido."""
