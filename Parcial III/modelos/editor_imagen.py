"""EditorImagen: guarda el estado de la imagen y coordina las operaciones."""

import os
from typing import List, Optional

from PIL import Image, UnidentifiedImageError

from modelos.excepciones import (
    ArchivoInvalidoError,
    ImagenNoCargadaError,
    ParametroInvalidoError,
)
from modelos.filtro import Filtro


class EditorImagen:
    """Mantiene la imagen original, la imagen actual y un historial.

    Encapsulamiento: los atributos son privados; desde afuera solo se
    consulta con propiedades de solo lectura y se modifica mediante métodos
    que validan los datos. Así la imagen nunca queda en un estado inválido.
    """

    LIMITE_HISTORIAL = 20
    TAMANO_MAXIMO = 8000  # píxeles por lado
    EXTENSIONES_VALIDAS = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")

    def __init__(self):
        self._original: Optional[Image.Image] = None
        self._actual: Optional[Image.Image] = None
        self._historial: List[Image.Image] = []
        self._ruta: Optional[str] = None

    # ---------- Propiedades de solo lectura ----------
    @property
    def tiene_imagen(self) -> bool:
        return self._actual is not None

    @property
    def imagen_actual(self) -> Image.Image:
        """Devuelve una COPIA para que nadie modifique el estado interno."""
        self._exigir_imagen()
        return self._actual.copy()

    @property
    def ruta(self) -> Optional[str]:
        return self._ruta

    @property
    def tamano(self) -> tuple:
        self._exigir_imagen()
        return self._actual.size

    @property
    def puede_deshacer(self) -> bool:
        return len(self._historial) > 0

    # ---------- Operaciones ----------
    def cargar(self, ruta: str) -> None:
        """Carga una imagen desde disco validando el archivo."""
        if not ruta or not os.path.isfile(ruta):
            raise ArchivoInvalidoError("El archivo seleccionado no existe.")
        if not ruta.lower().endswith(self.EXTENSIONES_VALIDAS):
            raise ArchivoInvalidoError(
                "Formato no soportado. Use: " + ", ".join(self.EXTENSIONES_VALIDAS)
            )
        try:
            with Image.open(ruta) as img:
                imagen = img.convert("RGB")
        except (UnidentifiedImageError, OSError):
            raise ArchivoInvalidoError("El archivo está dañado o no es una imagen válida.")

        self._original = imagen
        self._actual = imagen.copy()
        self._historial.clear()
        self._ruta = ruta

    def aplicar_filtro(self, filtro: Filtro) -> None:
        """Aplica cualquier filtro. Polimorfismo: no importa cuál sea."""
        self._exigir_imagen()
        nueva = filtro.aplicar(self._actual)
        self._guardar_historial()
        self._actual = nueva

    def rotar(self, grados: int) -> None:
        self._exigir_imagen()
        if grados not in (90, 180, 270, -90):
            raise ParametroInvalidoError("La rotación debe ser 90, 180 o 270 grados.")
        nueva = self._actual.rotate(-grados, expand=True)
        self._guardar_historial()
        self._actual = nueva

    def redimensionar(self, ancho, alto) -> None:
        self._exigir_imagen()
        try:
            ancho, alto = int(ancho), int(alto)
        except (TypeError, ValueError):
            raise ParametroInvalidoError("Ancho y alto deben ser números enteros.")
        if not (1 <= ancho <= self.TAMANO_MAXIMO and 1 <= alto <= self.TAMANO_MAXIMO):
            raise ParametroInvalidoError(
                f"Ancho y alto deben estar entre 1 y {self.TAMANO_MAXIMO} píxeles."
            )
        nueva = self._actual.resize((ancho, alto), Image.LANCZOS)
        self._guardar_historial()
        self._actual = nueva

    def deshacer(self) -> None:
        if not self._historial:
            raise ParametroInvalidoError("No hay cambios para deshacer.")
        self._actual = self._historial.pop()

    def restaurar(self) -> None:
        """Vuelve a la imagen original cargada."""
        self._exigir_imagen()
        self._guardar_historial()
        self._actual = self._original.copy()

    def exportar(self, ruta: str) -> None:
        self._exigir_imagen()
        if not ruta:
            raise ArchivoInvalidoError("No se indicó dónde guardar la imagen.")
        if not ruta.lower().endswith(self.EXTENSIONES_VALIDAS):
            raise ArchivoInvalidoError("Use una extensión válida (.png, .jpg, ...).")
        try:
            self._actual.save(ruta)
        except (OSError, ValueError) as error:
            raise ArchivoInvalidoError(f"No se pudo guardar la imagen: {error}")

    # ---------- Métodos internos ----------
    def _exigir_imagen(self) -> None:
        if self._actual is None:
            raise ImagenNoCargadaError("Primero debe cargar una imagen.")

    def _guardar_historial(self) -> None:
        self._historial.append(self._actual.copy())
        if len(self._historial) > self.LIMITE_HISTORIAL:
            self._historial.pop(0)
