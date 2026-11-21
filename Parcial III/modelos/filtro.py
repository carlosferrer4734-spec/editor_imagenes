"""Clase abstracta Filtro: el contrato que cumplen todos los filtros."""

from abc import ABC, abstractmethod

from PIL import Image


class Filtro(ABC):
    """Contrato común de los filtros de imagen.

    Cada filtro concreto recibe una imagen y devuelve una NUEVA imagen,
    sin modificar la original. El editor no necesita saber qué filtro es:
    solo llama a ``aplicar()`` (polimorfismo).
    """

    def __init__(self, nombre: str):
        self._nombre = nombre

    @property
    def nombre(self) -> str:
        """Nombre legible del filtro (solo lectura)."""
        return self._nombre

    @abstractmethod
    def aplicar(self, imagen: Image.Image) -> Image.Image:
        """Aplica el filtro y devuelve una imagen nueva."""

    def __str__(self) -> str:
        return self._nombre
