"""Ventana principal (CustomTkinter).

La ventana SOLO se encarga de mostrar controles y reaccionar a eventos
(callbacks). Toda la lógica de imágenes está en EditorImagen y GestorFiltros,
que recibe por el constructor.
"""

import os
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from modelos.editor_imagen import EditorImagen
from modelos.excepciones import ErrorEditor
from servicios.gestor_filtros import GestorFiltros


class VentanaPrincipal(ctk.CTk):
    ANCHO_VISTA = 720
    ALTO_VISTA = 520

    def __init__(self, editor: EditorImagen, gestor: GestorFiltros):
        super().__init__()
        self._editor = editor
        self._gestor = gestor
        self._imagen_tk = None  # referencia para que Tk no libere la imagen

        self.title("Editor de Imágenes POO")
        self.geometry("1050x640")
        self.minsize(900, 600)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._construir_panel_controles()
        self._construir_zona_vista()
        self._actualizar_controles_filtro(self._gestor.nombres()[0])

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def _construir_panel_controles(self):
        panel = ctk.CTkScrollableFrame(self, width=250, label_text="Herramientas")
        panel.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # --- Archivo ---
        ctk.CTkButton(panel, text="Abrir imagen", command=self._al_abrir).pack(fill="x", pady=3)
        ctk.CTkButton(panel, text="Guardar como...", command=self._al_guardar).pack(fill="x", pady=3)

        # --- Filtros ---
        ctk.CTkLabel(panel, text="Filtros", font=ctk.CTkFont(weight="bold")).pack(pady=(14, 2))
        self._combo_filtros = ctk.CTkOptionMenu(
            panel, values=self._gestor.nombres(), command=self._actualizar_controles_filtro
        )
        self._combo_filtros.pack(fill="x", pady=3)

        self._etiqueta_valor = ctk.CTkLabel(panel, text="")
        self._etiqueta_valor.pack()
        self._deslizador = ctk.CTkSlider(panel, command=self._al_mover_deslizador)
        self._deslizador.pack(fill="x", pady=3)

        ctk.CTkButton(panel, text="Aplicar filtro", command=self._al_aplicar_filtro).pack(fill="x", pady=3)

        # --- Transformaciones ---
        ctk.CTkLabel(panel, text="Rotar", font=ctk.CTkFont(weight="bold")).pack(pady=(14, 2))
        fila = ctk.CTkFrame(panel, fg_color="transparent")
        fila.pack(fill="x")
        ctk.CTkButton(fila, text="↺ 90°", width=70, command=lambda: self._al_rotar(-90)).pack(side="left", expand=True, padx=2)
        ctk.CTkButton(fila, text="↻ 90°", width=70, command=lambda: self._al_rotar(90)).pack(side="left", expand=True, padx=2)
        ctk.CTkButton(fila, text="180°", width=70, command=lambda: self._al_rotar(180)).pack(side="left", expand=True, padx=2)

        ctk.CTkLabel(panel, text="Redimensionar (px)", font=ctk.CTkFont(weight="bold")).pack(pady=(14, 2))
        fila2 = ctk.CTkFrame(panel, fg_color="transparent")
        fila2.pack(fill="x")
        self._entrada_ancho = ctk.CTkEntry(fila2, width=90, placeholder_text="Ancho")
        self._entrada_ancho.pack(side="left", expand=True, padx=2)
        self._entrada_alto = ctk.CTkEntry(fila2, width=90, placeholder_text="Alto")
        self._entrada_alto.pack(side="left", expand=True, padx=2)
        ctk.CTkButton(panel, text="Aplicar tamaño", command=self._al_redimensionar).pack(fill="x", pady=3)

        # --- Historial ---
        ctk.CTkLabel(panel, text="Historial", font=ctk.CTkFont(weight="bold")).pack(pady=(14, 2))
        ctk.CTkButton(panel, text="Deshacer", command=self._al_deshacer).pack(fill="x", pady=3)
        ctk.CTkButton(panel, text="Restaurar original", command=self._al_restaurar).pack(fill="x", pady=3)

    def _construir_zona_vista(self):
        zona = ctk.CTkFrame(self)
        zona.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        zona.grid_rowconfigure(0, weight=1)
        zona.grid_columnconfigure(0, weight=1)

        self._vista = ctk.CTkLabel(zona, text="Abra una imagen para comenzar")
        self._vista.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self._estado = ctk.CTkLabel(zona, text="Listo.", anchor="w")
        self._estado.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))

    # ------------------------------------------------------------------
    # Callbacks de eventos
    # ------------------------------------------------------------------
    def _al_abrir(self):
        ruta = filedialog.askopenfilename(
            title="Seleccione una imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")],
        )
        if not ruta:  # el usuario canceló el diálogo
            return
        self._ejecutar(lambda: self._editor.cargar(ruta), f"Imagen cargada: {os.path.basename(ruta)}")

    def _al_guardar(self):
        if not self._editor.tiene_imagen:
            self._mostrar_error("Primero debe cargar una imagen.")
            return
        ruta = filedialog.asksaveasfilename(
            title="Guardar imagen",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")],
        )
        if not ruta:
            return
        self._ejecutar(lambda: self._editor.exportar(ruta), f"Imagen guardada en {ruta}", redibujar=False)

    def _al_aplicar_filtro(self):
        nombre = self._combo_filtros.get()

        def operacion():
            valor = self._deslizador.get() if self._gestor.requiere_valor(nombre) else None
            self._editor.aplicar_filtro(self._gestor.crear(nombre, valor))

        self._ejecutar(operacion, f"Filtro aplicado: {nombre}")

    def _al_rotar(self, grados: int):
        self._ejecutar(lambda: self._editor.rotar(grados), f"Imagen rotada {grados}°")

    def _al_redimensionar(self):
        ancho, alto = self._entrada_ancho.get(), self._entrada_alto.get()
        self._ejecutar(lambda: self._editor.redimensionar(ancho, alto), "Imagen redimensionada")

    def _al_deshacer(self):
        self._ejecutar(self._editor.deshacer, "Cambio deshecho")

    def _al_restaurar(self):
        self._ejecutar(self._editor.restaurar, "Imagen original restaurada")

    def _al_mover_deslizador(self, valor):
        self._etiqueta_valor.configure(text=f"Valor: {float(valor):.2f}")

    # ------------------------------------------------------------------
    # Apoyo
    # ------------------------------------------------------------------
    def _ejecutar(self, operacion, mensaje_exito: str, redibujar: bool = True):
        """Ejecuta una operación del modelo y maneja los errores previsibles."""
        try:
            operacion()
        except ErrorEditor as error:
            self._mostrar_error(str(error))
            return
        self._estado.configure(text=mensaje_exito)
        if redibujar:
            self._mostrar_imagen()

    def _mostrar_error(self, mensaje: str):
        self._estado.configure(text=f"Error: {mensaje}")
        messagebox.showwarning("Aviso", mensaje)

    def _actualizar_controles_filtro(self, nombre: str):
        """Muestra u oculta el deslizador según el filtro elegido."""
        if self._gestor.requiere_valor(nombre):
            minimo, maximo = self._gestor.rango(nombre)
            defecto = self._gestor.valor_por_defecto(nombre)
            self._deslizador.configure(from_=minimo, to=maximo)
            self._deslizador.set(defecto)
            self._al_mover_deslizador(defecto)
            self._deslizador.pack(fill="x", pady=3, after=self._etiqueta_valor)
        else:
            self._etiqueta_valor.configure(text="Este filtro no tiene parámetros")
            self._deslizador.pack_forget()

    def _mostrar_imagen(self):
        imagen = self._editor.imagen_actual
        ancho, alto = imagen.size
        # Se escala solo la vista previa; la imagen real conserva su tamaño.
        vista = imagen.copy()
        vista.thumbnail((self.ANCHO_VISTA, self.ALTO_VISTA), Image.LANCZOS)
        self._imagen_tk = ctk.CTkImage(light_image=vista, dark_image=vista, size=vista.size)
        self._vista.configure(image=self._imagen_tk, text="")

        self._entrada_ancho.delete(0, "end")
        self._entrada_ancho.insert(0, str(ancho))
        self._entrada_alto.delete(0, "end")
        self._entrada_alto.insert(0, str(alto))
        self.title(f"Editor de Imágenes POO — {os.path.basename(self._editor.ruta)} ({ancho}x{alto})")
