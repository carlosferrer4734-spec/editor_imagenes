"""Pruebas de la lógica (sin interfaz). Ejecutar: python -m unittest discover -s pruebas -t ."""

import os
import tempfile
import unittest

from PIL import Image

from modelos.editor_imagen import EditorImagen
from modelos.excepciones import (
    ArchivoInvalidoError,
    ImagenNoCargadaError,
    ParametroInvalidoError,
)
from modelos.filtro import Filtro
from modelos.filtros_concretos import FiltroContraste, FiltroGrises
from servicios.gestor_filtros import GestorFiltros


class PruebasBase(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(self.carpeta.cleanup)
        self.ruta = os.path.join(self.carpeta.name, "roja.png")
        Image.new("RGB", (40, 20), (200, 30, 30)).save(self.ruta)
        self.editor = EditorImagen()


class PruebasEditor(PruebasBase):
    def test_cargar_imagen_valida(self):
        self.editor.cargar(self.ruta)
        self.assertTrue(self.editor.tiene_imagen)
        self.assertEqual(self.editor.tamano, (40, 20))

    def test_cargar_archivo_inexistente(self):
        with self.assertRaises(ArchivoInvalidoError):
            self.editor.cargar("no_existe.png")

    def test_cargar_archivo_que_no_es_imagen(self):
        falso = os.path.join(self.carpeta.name, "falso.png")
        with open(falso, "w") as f:
            f.write("esto no es una imagen")
        with self.assertRaises(ArchivoInvalidoError):
            self.editor.cargar(falso)

    def test_operar_sin_imagen(self):
        with self.assertRaises(ImagenNoCargadaError):
            self.editor.rotar(90)

    def test_rotar_intercambia_dimensiones(self):
        self.editor.cargar(self.ruta)
        self.editor.rotar(90)
        self.assertEqual(self.editor.tamano, (20, 40))

    def test_rotacion_invalida(self):
        self.editor.cargar(self.ruta)
        with self.assertRaises(ParametroInvalidoError):
            self.editor.rotar(45)

    def test_redimensionar(self):
        self.editor.cargar(self.ruta)
        self.editor.redimensionar(10, 5)
        self.assertEqual(self.editor.tamano, (10, 5))

    def test_redimensionar_invalido(self):
        self.editor.cargar(self.ruta)
        with self.assertRaises(ParametroInvalidoError):
            self.editor.redimensionar("abc", 5)
        with self.assertRaises(ParametroInvalidoError):
            self.editor.redimensionar(0, 5)

    def test_deshacer_y_restaurar(self):
        self.editor.cargar(self.ruta)
        self.editor.rotar(90)
        self.editor.deshacer()
        self.assertEqual(self.editor.tamano, (40, 20))
        self.editor.rotar(90)
        self.editor.restaurar()
        self.assertEqual(self.editor.tamano, (40, 20))

    def test_deshacer_sin_cambios(self):
        self.editor.cargar(self.ruta)
        with self.assertRaises(ParametroInvalidoError):
            self.editor.deshacer()

    def test_imagen_actual_devuelve_copia(self):
        self.editor.cargar(self.ruta)
        copia = self.editor.imagen_actual
        copia.putpixel((0, 0), (0, 0, 0))
        self.assertNotEqual(self.editor.imagen_actual.getpixel((0, 0)), (0, 0, 0))

    def test_exportar(self):
        self.editor.cargar(self.ruta)
        salida = os.path.join(self.carpeta.name, "salida.jpg")
        self.editor.exportar(salida)
        self.assertTrue(os.path.isfile(salida))

    def test_exportar_extension_invalida(self):
        self.editor.cargar(self.ruta)
        with self.assertRaises(ArchivoInvalidoError):
            self.editor.exportar(os.path.join(self.carpeta.name, "salida.txt"))


class PruebasFiltros(PruebasBase):
    def test_filtro_es_abstracto(self):
        with self.assertRaises(TypeError):
            Filtro("x")  # no se puede instanciar una clase abstracta

    def test_grises_deja_canales_iguales(self):
        self.editor.cargar(self.ruta)
        self.editor.aplicar_filtro(FiltroGrises())
        r, g, b = self.editor.imagen_actual.getpixel((0, 0))
        self.assertEqual((r, g), (g, b))

    def test_contraste_fuera_de_rango(self):
        with self.assertRaises(ParametroInvalidoError):
            FiltroContraste(10)
        with self.assertRaises(ParametroInvalidoError):
            FiltroContraste("alto")

    def test_polimorfismo_todos_los_filtros(self):
        """Todos los filtros del gestor se aplican con la misma llamada."""
        gestor = GestorFiltros()
        self.editor.cargar(self.ruta)
        for nombre in gestor.nombres():
            self.editor.aplicar_filtro(gestor.crear(nombre))
        self.assertEqual(self.editor.tamano, (40, 20))

    def test_gestor_filtro_desconocido(self):
        with self.assertRaises(ParametroInvalidoError):
            GestorFiltros().crear("Inexistente")


if __name__ == "__main__":
    unittest.main()
