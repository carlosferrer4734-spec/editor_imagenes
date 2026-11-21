"""Punto de entrada: crea los objetos y los conecta entre sí."""

from interfaz.ventana_principal import VentanaPrincipal
from modelos.editor_imagen import EditorImagen
from servicios.gestor_filtros import GestorFiltros


def main():
    editor = EditorImagen()
    gestor = GestorFiltros()
    ventana = VentanaPrincipal(editor, gestor)
    ventana.mainloop()


if __name__ == "__main__":
    main()
