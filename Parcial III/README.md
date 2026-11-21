# 🖼️ Editor de Imágenes POO

Aplicación de escritorio en Python para abrir imágenes, aplicarles filtros, transformarlas y exportar el resultado. Desarrollada como proyecto integrador de **Programación Orientada a Objetos**.

## 1. Descripción del problema

Editar una foto de forma rápida (pasarla a blanco y negro, ajustar el brillo, rotarla o cambiarle el tamaño) normalmente requiere programas pesados o complejos. Esta aplicación ofrece esas operaciones básicas en una interfaz sencilla, y a la vez sirve como ejemplo de un diseño orientado a objetos donde cada filtro es una clase intercambiable.

## 2. Objetivos

- Permitir cargar, modificar y guardar imágenes desde una interfaz gráfica.
- Aplicar los conceptos de POO: clases, encapsulamiento, herencia, polimorfismo, abstracción y relaciones entre objetos.
- Mantener separadas la lógica (modelos y servicios) y la interfaz.

## 3. Funcionalidades

| # | Funcionalidad | Descripción |
|---|---------------|-------------|
| 1 | Abrir y visualizar imagen | Carga PNG, JPG, BMP, GIF o WEBP y muestra una vista previa. |
| 2 | Aplicar filtros | Escala de grises, invertir, sepia, desenfoque, contraste y brillo (con deslizador de intensidad). |
| 3 | Rotar y redimensionar | Giros de 90°/180° y cambio de tamaño en píxeles. |
| 4 | Guardar imagen | Exporta el resultado como PNG, JPG o BMP. |
| 5 | Deshacer / Restaurar | Revierte el último cambio o vuelve a la imagen original. |

Los errores previsibles (archivo inválido, valores fuera de rango, operar sin imagen) se muestran con mensajes claros sin cerrar el programa.

## 4. Tecnologías utilizadas

- **Python 3.10 o superior**
- **Pillow**: procesamiento de imágenes.
- **CustomTkinter**: interfaz gráfica moderna basada en Tkinter.
- **unittest** (incluido en Python): pruebas automatizadas.
- Git y GitHub para el control de versiones.

## 5. Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/carlosferrer4734-spec/editor_imagenes.git
cd editor_imagenes

# 2. (Recomendado) crear un entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

> En algunas distribuciones de Linux hay que instalar Tkinter aparte: `sudo apt install python3-tk`.

## 6. Ejecución

```bash
python main.py
```

Para ejecutar las pruebas:

```bash
python -m unittest discover -s pruebas -t . -v
```

## 7. Manual de usuario

1. **Abrir imagen:** pulse *Abrir imagen* y elija un archivo. Aparecerá la vista previa.
   ![Abrir imagen](docs/imagenes/01_abrir.png)
2. **Aplicar un filtro:** elija el filtro en la lista, ajuste el deslizador si lo tiene y pulse *Aplicar filtro*.
   ![Filtro aplicado](docs/imagenes/02_filtro.png)
3. **Rotar o redimensionar:** use los botones de giro o escriba ancho y alto y pulse *Aplicar tamaño*.
   ![Transformaciones](docs/imagenes/03_transformar.png)
4. **Deshacer o restaurar:** *Deshacer* revierte el último cambio; *Restaurar original* vuelve al inicio.
5. **Guardar:** pulse *Guardar como...*, elija nombre y formato.

## 8. Estructura del proyecto

```
editor_imagenes/
├── main.py                      # Punto de entrada: crea los objetos y abre la ventana
├── modelos/
│   ├── excepciones.py           # Errores propios de la aplicación
│   ├── filtro.py                # Clase abstracta Filtro (contrato)
│   ├── filtros_concretos.py     # Filtros: grises, invertir, sepia, desenfoque, contraste, brillo
│   └── editor_imagen.py         # EditorImagen: estado de la imagen y operaciones
├── servicios/
│   └── gestor_filtros.py        # GestorFiltros: catálogo que crea filtros por nombre
├── interfaz/
│   └── ventana_principal.py     # VentanaPrincipal (CustomTkinter)
├── pruebas/
│   └── test_editor.py           # Pruebas automatizadas
├── recursos/                    # Imágenes de ejemplo
├── docs/
│   ├── INFORME_TECNICO.md       # Informe técnico del diseño y construcción
│   └── imagenes/                # Capturas y diagramas
├── requirements.txt
└── README.md
```

## 9. Autor

- **Nombre:** Carlos Andres Ferrer Calvo
- **Curso:** Programación Orientada a Objetos con Python
- **Contacto:** carlos_ferrer4734@americana.edu.co
