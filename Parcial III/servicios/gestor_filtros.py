"""GestorFiltros: catálogo que crea filtros a partir de su nombre."""

from typing import Dict, List, Optional

from modelos.excepciones import ParametroInvalidoError
from modelos.filtro import Filtro
from modelos.filtros_concretos import (
    FiltroBrillo,
    FiltroContraste,
    FiltroDesenfoque,
    FiltroGrises,
    FiltroInvertir,
    FiltroSepia,
)


class GestorFiltros:
    """Conoce los filtros disponibles y los construye bajo demanda.

    La interfaz le pide un filtro por nombre y no necesita importar ni
    conocer las clases concretas (bajo acoplamiento).
    """

    def __init__(self):
        # nombre -> (clase del filtro, valor por defecto o None si no tiene parámetro)
        self._catalogo: Dict[str, tuple] = {
            "Escala de grises": (FiltroGrises, None),
            "Invertir colores": (FiltroInvertir, None),
            "Sepia": (FiltroSepia, None),
            "Desenfoque": (FiltroDesenfoque, 3.0),
            "Contraste": (FiltroContraste, 1.5),
            "Brillo": (FiltroBrillo, 1.3),
        }

    def nombres(self) -> List[str]:
        return list(self._catalogo.keys())

    def requiere_valor(self, nombre: str) -> bool:
        return self._buscar(nombre)[1] is not None

    def valor_por_defecto(self, nombre: str) -> Optional[float]:
        return self._buscar(nombre)[1]

    def rango(self, nombre: str) -> tuple:
        """Devuelve (mínimo, máximo) del filtro parametrizado."""
        clase = self._buscar(nombre)[0]
        return clase.MINIMO, clase.MAXIMO

    def crear(self, nombre: str, valor: Optional[float] = None) -> Filtro:
        clase, defecto = self._buscar(nombre)
        if defecto is None:
            return clase()
        return clase(defecto if valor is None else valor)

    def _buscar(self, nombre: str) -> tuple:
        if nombre not in self._catalogo:
            raise ParametroInvalidoError(f"Filtro desconocido: {nombre}")
        return self._catalogo[nombre]
