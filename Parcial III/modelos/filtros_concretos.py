"""Filtros concretos. Cada uno especializa el método aplicar()."""

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from modelos.excepciones import ParametroInvalidoError
from modelos.filtro import Filtro


class FiltroGrises(Filtro):
    """Convierte la imagen a escala de grises."""

    def __init__(self):
        super().__init__("Escala de grises")

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        # Se vuelve a RGB para que el resto de filtros puedan encadenarse.
        return ImageOps.grayscale(imagen).convert("RGB")


class FiltroInvertir(Filtro):
    """Invierte los colores (efecto negativo)."""

    def __init__(self):
        super().__init__("Invertir colores")

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        return ImageOps.invert(imagen.convert("RGB"))


class FiltroSepia(Filtro):
    """Aplica un tono sepia."""

    def __init__(self):
        super().__init__("Sepia")

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        gris = ImageOps.grayscale(imagen)
        return ImageOps.colorize(gris, black="#2b1a0a", white="#f4e3c1").convert("RGB")


class FiltroConIntensidad(Filtro):
    """Clase intermedia para filtros con un parámetro numérico validado.

    Evita repetir la validación del rango en cada filtro parametrizado
    (reutilización por herencia). Sigue siendo abstracta porque no
    implementa ``aplicar()``.
    """

    MINIMO = 0.0
    MAXIMO = 1.0

    def __init__(self, nombre: str, valor: float):
        super().__init__(nombre)
        self._valor = 0.0
        self.valor = valor  # pasa por el setter para validar

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, nuevo: float) -> None:
        try:
            nuevo = float(nuevo)
        except (TypeError, ValueError):
            raise ParametroInvalidoError(f"{self._nombre}: el valor debe ser numérico.")
        if not (self.MINIMO <= nuevo <= self.MAXIMO):
            raise ParametroInvalidoError(
                f"{self._nombre}: el valor debe estar entre "
                f"{self.MINIMO} y {self.MAXIMO} (recibido: {nuevo})."
            )
        self._valor = nuevo


class FiltroDesenfoque(FiltroConIntensidad):
    """Desenfoque gaussiano. El valor es el radio (0 a 20)."""

    MINIMO = 0.0
    MAXIMO = 20.0

    def __init__(self, radio: float = 3.0):
        super().__init__("Desenfoque", radio)

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        return imagen.convert("RGB").filter(ImageFilter.GaussianBlur(self._valor))


class FiltroContraste(FiltroConIntensidad):
    """Ajusta el contraste. 1.0 = sin cambio, 0 = gris, 3 = muy alto."""

    MINIMO = 0.0
    MAXIMO = 3.0

    def __init__(self, factor: float = 1.5):
        super().__init__("Contraste", factor)

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        return ImageEnhance.Contrast(imagen.convert("RGB")).enhance(self._valor)


class FiltroBrillo(FiltroConIntensidad):
    """Ajusta el brillo. 1.0 = sin cambio, 0 = negro, 3 = muy brillante."""

    MINIMO = 0.0
    MAXIMO = 3.0

    def __init__(self, factor: float = 1.3):
        super().__init__("Brillo", factor)

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        return ImageEnhance.Brightness(imagen.convert("RGB")).enhance(self._valor)
