#!/usr/bin/env python3
"""
PixForge - Herramienta avanzada de procesamiento de imágenes
Aplicación completa de manipulación de imágenes construida con Pillow y Tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
import os
from pathlib import Path

# ─── Ícono de la aplicación (base64 PNG 64×64) ───────────────────────────────
import base64, io as _io
_ICONO_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAEaklEQVR4nO2bX2hTVxzHvzfeOAis2tgoXeYedH/qCn0waouitNCtuhWGIKHVh72OgbNjoMJgouBLYaBO9EUFYeYhL1VWRSP4NjASCivT1rHZTRqKW6pDsYMmzfUhPXJyc3PzO+fc3Nwk+5RLm5xzzz3f3+/8zrn313O1d7Z/DgEMkco1RKNW1A2joqZ6Ec3D99nWGD6BhuoVWw16mfJGEM7D9JSMBt1CaqOJ5zFgMoJuFOttZPGMIiNUmgMaHj4EmsH7jNejgE2CzSSeYQDQ9GZUzlNuGWwadBhyFphNXkk63RlV3u4+0C14iuErjACxw4viAeYUMS0+UfmzyZgnxTNmk7GkiB7tra3D5BBI3ysRP+hEpx1inP8Q3rafFA4qk+Dg6PXsXdmTnebwp/4eFBmBpktXueiSyskeQUflfEBZPG0Aoi6lG6FqG+BYR7SN/X18Op4ROZeqS+lGqFoGOMEJZzBjfEc2BE2X0tPgkgPHN/3+gPk7mWvK4hO6CTCRVzwO9/sDWP7Nvjtp4X2ekx3RNqu2SiBq8hmg/5hR8fxEIhrg25pIRANUT1JGAFVTzUIgPjpW1FZ8dAy/mIwicl1ZarIMTiWigWjCumxkOp45ZRMGI9RJkLoMkmqVQcYAv1Xw8lQiGkCHs9e0w5P3AQNnsLDx4/jCOW4kfFm1+wCFELCcfW2YIcY4APyRiAa+gJjoIrwWAo8FxMu0L4tgQqS0g9RDhsfLS6Nc+1VIiMgaIC3hfUaaaAQ5+S4sg/8oiBe5TgluzAE/FpIQtgwkMKlyDaBgxFunx7pU27Giqv8aGzi0V1l8tfHBMEA+aoiwMYmaqvafoVp7n6pLaRl0GzGjEpdBx3uJ2ntfhLqZAxhk49ZqDvCK9wXmgPrDSSMr3Qma8Yr3AZBDti5HAOCcsc27xKTxlPcByySuFVb7BB3H73/Tt6vv4jr2OZd7mf/32dTi9IMLz/P5rMGXAYBh5HHn9tBcpXYHDu2dLPuMQNSl9DDEd4RSL/37RPrMSM/Zrp37ug4ciQ23B589mfnr8hJfxupqmqZ9dPCzg070zw7X9wi1rF29NrxlRR8ABNd9sOpm7Nef+gexgZX1DPUOibRXfhQQQ0BVvkzst4U2vwEAczOTcy/nX8wDQPjdzeFvL/39NQC8eP4oe+/uUfl8IFxKiorCROZyC0b6z5+fXjv/1bWW9pYwUBoCIqPBchS4kRAR9T4vUl/pX9kaXhN+f0fndlYuEwKqqMwB49QszX+LCP5wO/sQACKRSCaVSl3lyr5nZe+t3/hAIfMzXvyRpksLfrhHyALz929I7RLLZDKLoVDoRiQSWZ1KpXqpZTKs6fyEvF9QaxU0AAA8lTSCGwQFxAOFhIgmlhQxEOzcI7oj0xUK/RLSommtm3YDXkj31Abt/83Sy/I1NJ8lil6YYF80ixFevzPkytOglzEnRMivnNYxtq/NsQqNOi5IL07yFRvFEGVHdqVlsBFGg21YU54G+QbqxRjkuewVuwodWEtu77YAAAAASUVORK5CYII="
)
def _cargar_icono():
    datos = base64.b64decode(_ICONO_B64)
    from PIL import Image, ImageTk
    img = Image.open(_io.BytesIO(datos))
    return ImageTk.PhotoImage(img)



# ─── Formatos soportados ──────────────────────────────────────────────────────
FORMATOS_ENTRADA = [
    ("Todas las imágenes", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.tif *.webp *.ico *.ppm *.pgm *.pbm"),
    ("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg"), ("BMP", "*.bmp"),
    ("GIF", "*.gif"), ("TIFF", "*.tiff *.tif"), ("WebP", "*.webp"),
    ("ICO", "*.ico"), ("PPM/PGM/PBM", "*.ppm *.pgm *.pbm"),
    ("Todos los archivos", "*.*"),
]
FORMATOS_SALIDA = ["PNG", "JPEG", "BMP", "GIF", "TIFF", "WEBP", "ICO", "PPM"]

FILTROS = {
    "Desenfoque": ImageFilter.BLUR,
    "Contorno": ImageFilter.CONTOUR,
    "Detalle": ImageFilter.DETAIL,
    "Realce de bordes": ImageFilter.EDGE_ENHANCE,
    "Realce de bordes +": ImageFilter.EDGE_ENHANCE_MORE,
    "Relieve": ImageFilter.EMBOSS,
    "Detectar bordes": ImageFilter.FIND_EDGES,
    "Enfocar": ImageFilter.SHARPEN,
    "Suavizar": ImageFilter.SMOOTH,
    "Suavizar +": ImageFilter.SMOOTH_MORE,
    "Desenfoque gaussiano": ImageFilter.GaussianBlur(radius=2),
    "Desenfoque de caja": ImageFilter.BoxBlur(radius=2),
    "Filtro mínimo": ImageFilter.MinFilter(size=3),
    "Filtro máximo": ImageFilter.MaxFilter(size=3),
    "Filtro mediana": ImageFilter.MedianFilter(size=3),
    "Filtro moda": ImageFilter.ModeFilter(size=3),
    "Máscara de enfoque": ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3),
}


# ─── Tooltip ──────────────────────────────────────────────────────────────────
class Tooltip:
    def __init__(self, widget, texto):
        self.widget = widget
        self.texto = texto
        self.ventana = None
        widget.bind("<Enter>", self.mostrar)
        widget.bind("<Leave>", self.ocultar)

    def mostrar(self, _=None):
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, "bbox") else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.ventana = tk.Toplevel(self.widget)
        self.ventana.wm_overrideredirect(True)
        self.ventana.wm_geometry(f"+{x}+{y}")
        tk.Label(self.ventana, text=self.texto, background="#ffffe0", relief="solid",
                 borderwidth=1, font=("Segoe UI", 9)).pack()

    def ocultar(self, _=None):
        if self.ventana:
            self.ventana.destroy()
            self.ventana = None


# ─── Aplicación principal ─────────────────────────────────────────────────────
class PixForge(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PixForge — Herramienta de Procesamiento de Imágenes")
        self.geometry("1200x800")
        self.minsize(900, 650)
        self.configure(bg="#1e1e2e")

        # Establecer ícono de la ventana
        try:
            self._icono_app = _cargar_icono()
            self.iconphoto(True, self._icono_app)
        except Exception:
            pass

        # Estado interno
        self.imagen_original: Image.Image | None = None
        self.imagen_actual: Image.Image | None = None
        self.ruta_archivo: str | None = None
        self.historial: list[Image.Image] = []
        self.indice_historial: int = -1
        self.nivel_zoom: float = 1.0
        self._foto_ref = None

        self._construir_estilos()
        self._construir_interfaz()
        self._enlazar_atajos()

    # ── Estilos visuales ───────────────────────────────────────────────────────
    def _construir_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        fondo, texto, acento = "#1e1e2e", "#cdd6f4", "#89b4fa"
        estilo.configure(".", background=fondo, foreground=texto, font=("Segoe UI", 10))
        estilo.configure("TFrame", background=fondo)
        estilo.configure("TLabel", background=fondo, foreground=texto)
        estilo.configure("TButton", background="#313244", foreground=texto,
                         relief="flat", padding=(8, 4))
        estilo.map("TButton",
                   background=[("active", acento), ("pressed", "#7aa2f7")],
                   foreground=[("active", "#1e1e2e")])
        estilo.configure("Acento.TButton", background=acento, foreground="#1e1e2e",
                         font=("Segoe UI", 10, "bold"))
        estilo.map("Acento.TButton", background=[("active", "#7aa2f7")])
        estilo.configure("TNotebook", background="#181825", tabmargins=[2, 5, 0, 0])
        estilo.configure("TNotebook.Tab", background="#313244", foreground=texto,
                         padding=[12, 5], font=("Segoe UI", 10))
        estilo.map("TNotebook.Tab",
                   background=[("selected", acento)],
                   foreground=[("selected", "#1e1e2e")])
        estilo.configure("TScale", background=fondo, troughcolor="#313244", sliderlength=16)
        estilo.configure("TCombobox", fieldbackground="#313244", background="#313244",
                         foreground=texto, selectbackground=acento)
        estilo.configure("TLabelframe", background=fondo, foreground=acento,
                         font=("Segoe UI", 10, "bold"))
        estilo.configure("TLabelframe.Label", background=fondo, foreground=acento)
        estilo.configure("TProgressbar", troughcolor="#313244", background=acento)

    # ── Construcción de la interfaz ────────────────────────────────────────────
    def _construir_interfaz(self):
        # ── Barra de menú ──────────────────────────────────────────────────────
        barra_menu = tk.Menu(self, bg="#313244", fg="#cdd6f4",
                             activebackground="#89b4fa", activeforeground="#1e1e2e", bd=0)

        menu_archivo = tk.Menu(barra_menu, tearoff=0, bg="#313244", fg="#cdd6f4",
                               activebackground="#89b4fa", activeforeground="#1e1e2e")
        menu_archivo.add_command(label="Abrir…  Ctrl+A", command=self.abrir_imagen)
        menu_archivo.add_command(label="Guardar  Ctrl+G", command=self.guardar_imagen)
        menu_archivo.add_command(label="Guardar como…  Ctrl+Mayús+G", command=self.guardar_como)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Conversión por lotes…", command=self.convertir_lote)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir  Ctrl+Q", command=self.quit)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        menu_editar = tk.Menu(barra_menu, tearoff=0, bg="#313244", fg="#cdd6f4",
                              activebackground="#89b4fa", activeforeground="#1e1e2e")
        menu_editar.add_command(label="Deshacer  Ctrl+Z", command=self.deshacer)
        menu_editar.add_command(label="Rehacer  Ctrl+Y", command=self.rehacer)
        menu_editar.add_separator()
        menu_editar.add_command(label="Restaurar original", command=self.restaurar_imagen)
        barra_menu.add_cascade(label="Editar", menu=menu_editar)

        menu_ayuda = tk.Menu(barra_menu, tearoff=0, bg="#313244", fg="#cdd6f4",
                             activebackground="#89b4fa", activeforeground="#1e1e2e")
        menu_ayuda.add_command(label="Acerca de PixForge", command=self._mostrar_acerca)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        self.config(menu=barra_menu)

        # ── Barra de herramientas ──────────────────────────────────────────────
        barra = tk.Frame(self, bg="#181825", pady=4)
        barra.pack(fill="x", side="top")
        botones = [
            ("📂 Abrir",    self.abrir_imagen,    "Abrir imagen (Ctrl+A)"),
            ("💾 Guardar",  self.guardar_imagen,  "Guardar imagen (Ctrl+G)"),
            ("↩ Deshacer", self.deshacer,         "Deshacer (Ctrl+Z)"),
            ("↪ Rehacer",  self.rehacer,          "Rehacer (Ctrl+Y)"),
            ("🔄 Restaurar", self.restaurar_imagen, "Restaurar imagen original"),
            ("📦 Lotes",    self.convertir_lote,  "Conversión por lotes"),
        ]
        for txt, cmd, tip in botones:
            b = ttk.Button(barra, text=txt, command=cmd)
            b.pack(side="left", padx=3, pady=2)
            Tooltip(b, tip)

        # ── Barra de estado ────────────────────────────────────────────────────
        self.var_estado = tk.StringVar(value="Listo — Abre una imagen para comenzar")
        barra_estado = tk.Frame(self, bg="#181825")
        barra_estado.pack(fill="x", side="bottom")
        tk.Label(barra_estado, textvariable=self.var_estado, bg="#181825", fg="#a6adc8",
                 font=("Segoe UI", 9), anchor="w", padx=8).pack(side="left", fill="x")
        self.progreso = ttk.Progressbar(barra_estado, length=150, mode="determinate")
        self.progreso.pack(side="right", padx=8, pady=3)

        # ── Divisor principal ──────────────────────────────────────────────────
        panel = ttk.PanedWindow(self, orient="horizontal")
        panel.pack(fill="both", expand=True)

        # Panel izquierdo: pestañas de herramientas
        izquierda = ttk.Frame(panel, width=320)
        panel.add(izquierda, weight=0)
        pestanas = ttk.Notebook(izquierda)
        pestanas.pack(fill="both", expand=True, padx=4, pady=4)
        pestanas.add(self._pestana_transformar(pestanas), text="✂ Transformar")
        pestanas.add(self._pestana_ajustar(pestanas),    text="🎨 Ajustar")
        pestanas.add(self._pestana_filtros(pestanas),    text="🌀 Filtros")
        pestanas.add(self._pestana_convertir(pestanas),  text="🔁 Convertir")
        pestanas.add(self._pestana_info(pestanas),       text="ℹ Info")

        # Panel derecho: lienzo de previsualización
        derecha = ttk.Frame(panel)
        panel.add(derecha, weight=1)

        barra_zoom = ttk.Frame(derecha)
        barra_zoom.pack(fill="x", padx=4, pady=(4, 0))
        ttk.Button(barra_zoom, text="−", width=3, command=self.zoom_reducir).pack(side="left", padx=2)
        self.etiqueta_zoom = ttk.Label(barra_zoom, text="100%", width=7, anchor="center")
        self.etiqueta_zoom.pack(side="left")
        ttk.Button(barra_zoom, text="+", width=3, command=self.zoom_aumentar).pack(side="left", padx=2)
        ttk.Button(barra_zoom, text="Ajustar", command=self.zoom_ajustar).pack(side="left", padx=4)
        ttk.Button(barra_zoom, text="1:1", command=self.zoom_original).pack(side="left")

        marco_lienzo = ttk.Frame(derecha)
        marco_lienzo.pack(fill="both", expand=True, padx=4, pady=4)
        self.lienzo = tk.Canvas(marco_lienzo, bg="#11111b", cursor="crosshair",
                                highlightthickness=0)
        bh = ttk.Scrollbar(marco_lienzo, orient="horizontal", command=self.lienzo.xview)
        bv = ttk.Scrollbar(marco_lienzo, orient="vertical", command=self.lienzo.yview)
        self.lienzo.configure(xscrollcommand=bh.set, yscrollcommand=bv.set)
        bh.pack(side="bottom", fill="x")
        bv.pack(side="right", fill="y")
        self.lienzo.pack(fill="both", expand=True)
        self.lienzo.create_text(400, 300, text="🖼  Abre una imagen para comenzar",
                                fill="#585b70", font=("Segoe UI", 16), tags="placeholder")
        self.lienzo.bind("<MouseWheel>", self._rueda_raton)

    # ── Pestaña Transformar ────────────────────────────────────────────────────
    def _pestana_transformar(self, parent):
        f = ttk.Frame(parent)
        f.columnconfigure(0, weight=1)

        # Redimensionar
        gf = ttk.LabelFrame(f, text="Redimensionar", padding=8)
        gf.grid(row=0, column=0, padx=8, pady=6, sticky="ew")
        gf.columnconfigure((0, 1), weight=1)
        ttk.Label(gf, text="Ancho (px):").grid(row=0, column=0, sticky="w")
        ttk.Label(gf, text="Alto (px):").grid(row=0, column=1, sticky="w")
        self.entrada_ancho = ttk.Entry(gf, width=8)
        self.entrada_alto  = ttk.Entry(gf, width=8)
        self.entrada_ancho.grid(row=1, column=0, padx=2)
        self.entrada_alto.grid(row=1,  column=1, padx=2)
        self.mantener_ratio = tk.BooleanVar(value=True)
        ttk.Checkbutton(gf, text="Mantener proporción",
                        variable=self.mantener_ratio).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=2)
        self.var_remuestreo = tk.StringVar(value="LANCZOS")
        ttk.Label(gf, text="Remuestreo:").grid(row=3, column=0, sticky="w")
        ttk.Combobox(gf, textvariable=self.var_remuestreo, width=10,
                     values=["LANCZOS", "BICUBIC", "BILINEAR", "NEAREST"],
                     state="readonly").grid(row=3, column=1)
        ttk.Button(gf, text="Aplicar redimensión", style="Acento.TButton",
                   command=self.aplicar_redimension).grid(
            row=4, column=0, columnspan=2, pady=(6, 0), sticky="ew")
        self.entrada_ancho.bind("<FocusOut>", self._sincronizar_ratio)

        # Rotar y voltear
        gf2 = ttk.LabelFrame(f, text="Rotar y Voltear", padding=8)
        gf2.grid(row=1, column=0, padx=8, pady=6, sticky="ew")
        fila = ttk.Frame(gf2)
        fila.pack(fill="x")
        for txt, cmd in [("↺ 90°", lambda: self.rotar(90)),
                         ("↻ 90°", lambda: self.rotar(-90)),
                         ("180°",  lambda: self.rotar(180))]:
            ttk.Button(fila, text=txt, command=cmd).pack(side="left", padx=2, pady=2)
        fila2 = ttk.Frame(gf2)
        fila2.pack(fill="x", pady=(4, 0))
        ttk.Button(fila2, text="↔ Voltear H", command=self.voltear_horizontal).pack(side="left", padx=2)
        ttk.Button(fila2, text="↕ Voltear V", command=self.voltear_vertical).pack(side="left", padx=2)
        self.var_angulo = tk.DoubleVar(value=0)
        ttk.Label(gf2, text="Ángulo personalizado:").pack(anchor="w", pady=(6, 0))
        ttk.Scale(gf2, from_=-180, to=180, variable=self.var_angulo,
                  orient="horizontal").pack(fill="x")
        self.var_expandir = tk.BooleanVar(value=True)
        ttk.Checkbutton(gf2, text="Expandir lienzo",
                        variable=self.var_expandir).pack(anchor="w")
        ttk.Button(gf2, text="Aplicar rotación", style="Acento.TButton",
                   command=self.aplicar_rotacion_personalizada).pack(fill="x", pady=4)

        # Recortar
        gf3 = ttk.LabelFrame(f, text="Recortar (izq, sup, der, inf)", padding=8)
        gf3.grid(row=2, column=0, padx=8, pady=6, sticky="ew")
        self.entradas_recorte = {}
        for i, lado in enumerate(["Izquierda", "Superior", "Derecha", "Inferior"]):
            ttk.Label(gf3, text=lado + ":").grid(row=i // 2, column=(i % 2) * 2,
                                                  sticky="e", padx=2)
            e = ttk.Entry(gf3, width=7)
            e.insert(0, "0")
            e.grid(row=i // 2, column=(i % 2) * 2 + 1, sticky="w", padx=2, pady=2)
            self.entradas_recorte[lado] = e
        ttk.Button(gf3, text="Aplicar recorte", style="Acento.TButton",
                   command=self.aplicar_recorte).grid(
            row=2, column=0, columnspan=4, sticky="ew", pady=4)

        # Transponer
        gf4 = ttk.LabelFrame(f, text="Transponer", padding=8)
        gf4.grid(row=3, column=0, padx=8, pady=6, sticky="ew")
        for txt, op in [("Transponer",  Image.Transpose.TRANSPOSE),
                        ("Transversal", Image.Transpose.TRANSVERSE)]:
            ttk.Button(gf4, text=txt,
                       command=lambda o=op: self._aplicar(lambda img: img.transpose(o))
                       ).pack(side="left", padx=4)
        return f

    # ── Pestaña Ajustar ────────────────────────────────────────────────────────
    def _pestana_ajustar(self, parent):
        f = ttk.Frame(parent)
        f.columnconfigure(0, weight=1)

        mejoras = [
            ("Brillo",          "brillo",    0.0, 3.0, 1.0),
            ("Contraste",       "contraste", 0.0, 3.0, 1.0),
            ("Saturación",      "saturacion",0.0, 3.0, 1.0),
            ("Nitidez",         "nitidez",   0.0, 3.0, 1.0),
            ("Balance de color","color",     0.0, 3.0, 1.0),
        ]
        self.vars_mejora    = {}
        self.etiquetas_mejora = {}

        gf = ttk.LabelFrame(f, text="Mejoras de imagen", padding=8)
        gf.grid(row=0, column=0, padx=8, pady=6, sticky="ew")
        for i, (etq, clave, lo, hi, val) in enumerate(mejoras):
            var = tk.DoubleVar(value=val)
            lbl = ttk.Label(gf, text=f"{etq}: {val:.2f}", width=22, anchor="w")
            lbl.grid(row=i * 2, column=0, sticky="w")
            sl = ttk.Scale(gf, from_=lo, to=hi, variable=var, orient="horizontal")
            sl.grid(row=i * 2 + 1, column=0, sticky="ew", pady=(0, 4))
            sl.bind("<ButtonRelease-1>", lambda e, k=clave: self.aplicar_mejora(k))
            var.trace_add("write", lambda *a, k=clave, v=var, l=lbl, etq=etq:
                          l.config(text=f"{etq}: {v.get():.2f}"))
            self.vars_mejora[clave]     = var
            self.etiquetas_mejora[clave] = lbl
        ttk.Button(gf, text="Restablecer todo",
                   command=self._restablecer_mejoras).grid(
            row=len(mejoras) * 2, column=0, sticky="ew", pady=4)

        # Operaciones de color
        gf2 = ttk.LabelFrame(f, text="Operaciones de color", padding=8)
        gf2.grid(row=1, column=0, padx=8, pady=6, sticky="ew")
        ops = [
            ("Escala de grises",  self.a_escala_grises),
            ("Invertir colores",  self.invertir_imagen),
            ("Solarizar",         self.solarizar),
            ("Posterizar",        self.posterizar),
            ("Ecualizar",         self.ecualizar),
            ("Autocontraste",     self.autocontraste),
        ]
        for i, (txt, cmd) in enumerate(ops):
            ttk.Button(gf2, text=txt, command=cmd).grid(
                row=i // 2, column=i % 2, padx=3, pady=2, sticky="ew")
        gf2.columnconfigure((0, 1), weight=1)

        # Extractor de canales
        gf3 = ttk.LabelFrame(f, text="Extractor de canales RGB", padding=8)
        gf3.grid(row=2, column=0, padx=8, pady=6, sticky="ew")
        for c in ["R", "G", "B"]:
            ttk.Button(gf3, text=f"Extraer canal {c}",
                       command=lambda ch=c: self._extraer_canal(ch)).pack(side="left", padx=3)
        return f

    # ── Pestaña Filtros ────────────────────────────────────────────────────────
    def _pestana_filtros(self, parent):
        f = ttk.Frame(parent)
        f.columnconfigure(0, weight=1)

        gf = ttk.LabelFrame(f, text="Aplicar filtro", padding=8)
        gf.grid(row=0, column=0, padx=8, pady=6, sticky="ew")
        self.lista_filtros = tk.Listbox(
            gf, listvariable=tk.StringVar(value=list(FILTROS.keys())),
            height=16, bg="#313244", fg="#cdd6f4", selectbackground="#89b4fa",
            activestyle="none", font=("Segoe UI", 10), bd=0, highlightthickness=0)
        self.lista_filtros.pack(fill="both", expand=True)
        self.lista_filtros.select_set(0)
        ttk.Button(gf, text="Aplicar filtro seleccionado", style="Acento.TButton",
                   command=self.aplicar_filtro).pack(fill="x", pady=4)

        gf2 = ttk.LabelFrame(f, text="Dibujo y efectos", padding=8)
        gf2.grid(row=1, column=0, padx=8, pady=6, sticky="ew")
        ttk.Button(gf2, text="Agregar marca de agua",
                   command=self.agregar_marca_agua).pack(fill="x", pady=2)
        ttk.Button(gf2, text="Agregar borde de color",
                   command=self.agregar_borde).pack(fill="x", pady=2)
        return f

    # ── Pestaña Convertir ──────────────────────────────────────────────────────
    def _pestana_convertir(self, parent):
        f = ttk.Frame(parent)
        f.columnconfigure(0, weight=1)

        gf = ttk.LabelFrame(f, text="Conversión de formato", padding=8)
        gf.grid(row=0, column=0, padx=8, pady=6, sticky="ew")
        ttk.Label(gf, text="Formato de salida:").pack(anchor="w")
        self.var_formato = tk.StringVar(value="PNG")
        cb = ttk.Combobox(gf, textvariable=self.var_formato,
                          values=FORMATOS_SALIDA, state="readonly")
        cb.pack(fill="x", pady=4)
        cb.bind("<<ComboboxSelected>>", self._al_cambiar_formato)

        # Opciones JPEG
        self.marco_jpeg = ttk.LabelFrame(gf, text="Opciones JPEG", padding=6)
        self.jpeg_calidad = tk.IntVar(value=90)
        ttk.Label(self.marco_jpeg, text="Calidad:").pack(anchor="w")
        ttk.Scale(self.marco_jpeg, from_=1, to=100, variable=self.jpeg_calidad,
                  orient="horizontal").pack(fill="x")
        self.etiq_calidad = ttk.Label(self.marco_jpeg, text="90")
        self.etiq_calidad.pack(anchor="e")
        self.jpeg_calidad.trace_add("write", lambda *a: self.etiq_calidad.config(
            text=str(self.jpeg_calidad.get())))
        self.jpeg_optimizar  = tk.BooleanVar(value=True)
        self.jpeg_progresivo = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.marco_jpeg, text="Optimizar",
                        variable=self.jpeg_optimizar).pack(anchor="w")
        ttk.Checkbutton(self.marco_jpeg, text="Progresivo",
                        variable=self.jpeg_progresivo).pack(anchor="w")

        # Opciones PNG
        self.marco_png    = ttk.LabelFrame(gf, text="Opciones PNG", padding=6)
        self.png_compresion = tk.IntVar(value=6)
        ttk.Label(self.marco_png, text="Nivel de compresión (0–9):").pack(anchor="w")
        ttk.Scale(self.marco_png, from_=0, to=9, variable=self.png_compresion,
                  orient="horizontal").pack(fill="x")

        self.marco_jpeg.pack(fill="x", pady=4)
        self._al_cambiar_formato()

        ttk.Button(gf, text="Convertir y guardar como…", style="Acento.TButton",
                   command=self.guardar_como).pack(fill="x", pady=6)

        # Conversión por lotes
        gf2 = ttk.LabelFrame(f, text="Conversión por lotes", padding=8)
        gf2.grid(row=1, column=0, padx=8, pady=6, sticky="ew")
        ttk.Label(gf2,
                  text="Convierte todas las imágenes de una carpeta al formato seleccionado.",
                  wraplength=280, foreground="#a6adc8").pack(anchor="w")
        ttk.Button(gf2, text="📦 Abrir conversor por lotes",
                   command=self.convertir_lote).pack(fill="x", pady=6)

        # Miniatura
        gf3 = ttk.LabelFrame(f, text="Generar miniatura", padding=8)
        gf3.grid(row=2, column=0, padx=8, pady=6, sticky="ew")
        gf3.columnconfigure((0, 1), weight=1)
        ttk.Label(gf3, text="Tamaño máximo (px):").grid(row=0, column=0, sticky="w")
        self.entrada_miniatura = ttk.Entry(gf3, width=8)
        self.entrada_miniatura.insert(0, "256")
        self.entrada_miniatura.grid(row=0, column=1, sticky="w")
        ttk.Button(gf3, text="Generar y guardar",
                   command=self.generar_miniatura).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=4)
        return f

    # ── Pestaña Info ───────────────────────────────────────────────────────────
    def _pestana_info(self, parent):
        f = ttk.Frame(parent)
        self.texto_info = tk.Text(f, bg="#181825", fg="#cdd6f4", font=("Courier", 9),
                                  relief="flat", state="disabled", wrap="word",
                                  padx=8, pady=8)
        self.texto_info.pack(fill="both", expand=True, padx=4, pady=4)
        ttk.Button(f, text="Actualizar información",
                   command=self.actualizar_info).pack(fill="x", padx=4, pady=4)
        return f

    # ── Abrir / Guardar ────────────────────────────────────────────────────────
    def abrir_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=FORMATOS_ENTRADA,
                                          title="Abrir imagen")
        if not ruta:
            return
        try:
            img = Image.open(ruta)
            img.load()
            self.ruta_archivo   = ruta
            self.imagen_original = img.copy()
            self.imagen_actual   = img.copy()
            self.historial       = [img.copy()]
            self.indice_historial = 0
            self.nivel_zoom      = 1.0
            self._actualizar_lienzo()
            self.actualizar_info()
            self._set_estado(
                f"Abierto: {Path(ruta).name}  —  {img.size[0]}×{img.size[1]} px  |  {img.mode}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la imagen:\n{e}")

    def guardar_imagen(self):
        if not self.imagen_actual or not self.ruta_archivo:
            self.guardar_como()
            return
        self._guardar_en(self.ruta_archivo)

    def guardar_como(self):
        if not self.imagen_actual:
            return
        fmt = self.var_formato.get()
        ext = fmt.lower().replace("jpeg", "jpg")
        ruta = filedialog.asksaveasfilename(
            defaultextension=f".{ext}",
            filetypes=[(fmt, f"*.{ext}"), ("Todos los archivos", "*.*")],
            title="Guardar imagen como…",
        )
        if ruta:
            self._guardar_en(ruta)

    def _guardar_en(self, ruta: str):
        try:
            ext = Path(ruta).suffix.lower().lstrip(".")
            fmt = {"jpg": "JPEG", "jpeg": "JPEG", "tif": "TIFF"}.get(ext, ext.upper())
            img = self.imagen_actual.copy()
            kwargs = {}
            if fmt == "JPEG":
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                kwargs = {"quality": self.jpeg_calidad.get(),
                          "optimize": self.jpeg_optimizar.get(),
                          "progressive": self.jpeg_progresivo.get()}
            elif fmt == "PNG":
                kwargs = {"compress_level": self.png_compresion.get()}
            img.save(ruta, format=fmt, **kwargs)
            self.ruta_archivo = ruta
            tam = os.path.getsize(ruta) / 1024
            self._set_estado(f"Guardado: {Path(ruta).name}  ({tam:.1f} KB)")
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    # ── Lienzo y zoom ──────────────────────────────────────────────────────────
    def _actualizar_lienzo(self):
        if not self.imagen_actual:
            return
        w = int(self.imagen_actual.width  * self.nivel_zoom)
        h = int(self.imagen_actual.height * self.nivel_zoom)
        vista = self.imagen_actual.resize((w, h), Image.Resampling.LANCZOS)
        self._foto_ref = ImageTk.PhotoImage(vista)
        self.lienzo.delete("all")
        self.lienzo.create_image(0, 0, anchor="nw", image=self._foto_ref)
        self.lienzo.configure(scrollregion=(0, 0, w, h))
        self.etiqueta_zoom.config(text=f"{int(self.nivel_zoom * 100)}%")

    def zoom_aumentar(self):
        self.nivel_zoom = min(self.nivel_zoom * 1.25, 8.0)
        self._actualizar_lienzo()

    def zoom_reducir(self):
        self.nivel_zoom = max(self.nivel_zoom / 1.25, 0.05)
        self._actualizar_lienzo()

    def zoom_ajustar(self):
        if not self.imagen_actual:
            return
        aw = self.lienzo.winfo_width()  or 800
        ah = self.lienzo.winfo_height() or 600
        self.nivel_zoom = min(aw / self.imagen_actual.width,
                              ah / self.imagen_actual.height)
        self._actualizar_lienzo()

    def zoom_original(self):
        self.nivel_zoom = 1.0
        self._actualizar_lienzo()

    def _rueda_raton(self, ev):
        if ev.delta > 0:
            self.zoom_aumentar()
        else:
            self.zoom_reducir()

    # ── Historial ──────────────────────────────────────────────────────────────
    def _empujar(self, img: Image.Image):
        self.historial = self.historial[:self.indice_historial + 1]
        self.historial.append(img.copy())
        self.indice_historial += 1
        self.imagen_actual = img

    def deshacer(self):
        if self.indice_historial > 0:
            self.indice_historial -= 1
            self.imagen_actual = self.historial[self.indice_historial].copy()
            self._actualizar_lienzo()
            self._set_estado("Acción deshecha")

    def rehacer(self):
        if self.indice_historial < len(self.historial) - 1:
            self.indice_historial += 1
            self.imagen_actual = self.historial[self.indice_historial].copy()
            self._actualizar_lienzo()
            self._set_estado("Acción rehecha")

    def restaurar_imagen(self):
        if self.imagen_original:
            self._empujar(self.imagen_original.copy())
            self._actualizar_lienzo()
            self._set_estado("Imagen restaurada al original")

    def _aplicar(self, fn):
        if not self.imagen_actual:
            return
        try:
            self._empujar(fn(self.imagen_actual.copy()))
            self._actualizar_lienzo()
            self.actualizar_info()
        except Exception as e:
            messagebox.showerror("Error en operación", str(e))

    # ── Transformaciones ───────────────────────────────────────────────────────
    def aplicar_redimension(self):
        if not self.imagen_actual:
            return
        try:
            w, h = int(self.entrada_ancho.get()), int(self.entrada_alto.get())
        except ValueError:
            messagebox.showwarning("Valor inválido", "Ingresa dimensiones válidas en píxeles.")
            return
        rs = getattr(Image.Resampling, self.var_remuestreo.get())
        self._aplicar(lambda img: img.resize((w, h), rs))
        self._set_estado(f"Redimensionado a {w}×{h} px")

    def _sincronizar_ratio(self, _=None):
        if not self.imagen_actual or not self.mantener_ratio.get():
            return
        try:
            w = int(self.entrada_ancho.get())
            h = int(self.imagen_actual.height * w / self.imagen_actual.width)
            self.entrada_alto.delete(0, "end")
            self.entrada_alto.insert(0, str(h))
        except Exception:
            pass

    def rotar(self, angulo):
        self._aplicar(lambda img: img.rotate(angulo, expand=True))
        self._set_estado(f"Rotado {angulo}°")

    def aplicar_rotacion_personalizada(self):
        self._aplicar(lambda img: img.rotate(self.var_angulo.get(),
                                              expand=self.var_expandir.get()))
        self._set_estado(f"Rotado {self.var_angulo.get():.1f}°")

    def voltear_horizontal(self):
        self._aplicar(lambda img: img.transpose(Image.Transpose.FLIP_LEFT_RIGHT))
        self._set_estado("Volteado horizontalmente")

    def voltear_vertical(self):
        self._aplicar(lambda img: img.transpose(Image.Transpose.FLIP_TOP_BOTTOM))
        self._set_estado("Volteado verticalmente")

    def aplicar_recorte(self):
        if not self.imagen_actual:
            return
        try:
            caja = (
                int(self.entradas_recorte["Izquierda"].get()),
                int(self.entradas_recorte["Superior"].get()),
                int(self.entradas_recorte["Derecha"].get()),
                int(self.entradas_recorte["Inferior"].get()),
            )
        except ValueError:
            messagebox.showwarning("Valor inválido", "Ingresa coordenadas de recorte válidas.")
            return
        self._aplicar(lambda img: img.crop(caja))
        self._set_estado(f"Recortado: {caja}")

    # ── Ajustes de imagen ──────────────────────────────────────────────────────
    def aplicar_mejora(self, clave):
        if not self.imagen_actual:
            return
        val = self.vars_mejora[clave].get()
        mapa = {
            "brillo":    ImageEnhance.Brightness,
            "contraste": ImageEnhance.Contrast,
            "saturacion": ImageEnhance.Color,
            "nitidez":   ImageEnhance.Sharpness,
            "color":     ImageEnhance.Color,
        }
        self._aplicar(lambda img: mapa[clave](img).enhance(val))

    def _restablecer_mejoras(self):
        for v in self.vars_mejora.values():
            v.set(1.0)

    def a_escala_grises(self):
        self._aplicar(lambda img: img.convert("L").convert("RGB"))
        self._set_estado("Convertido a escala de grises")

    def invertir_imagen(self):
        def _inv(img):
            if img.mode == "RGBA":
                r, g, b, a = img.split()
                inv = ImageOps.invert(Image.merge("RGB", (r, g, b)))
                r2, g2, b2 = inv.split()
                return Image.merge("RGBA", (r2, g2, b2, a))
            return ImageOps.invert(img.convert("RGB"))
        self._aplicar(_inv)
        self._set_estado("Colores invertidos")

    def solarizar(self):
        self._aplicar(lambda img: ImageOps.solarize(img.convert("RGB"), threshold=128))
        self._set_estado("Solarización aplicada")

    def posterizar(self):
        self._aplicar(lambda img: ImageOps.posterize(img.convert("RGB"), bits=2))
        self._set_estado("Posterización aplicada")

    def ecualizar(self):
        self._aplicar(lambda img: ImageOps.equalize(img.convert("RGB")))
        self._set_estado("Histograma ecualizado")

    def autocontraste(self):
        self._aplicar(lambda img: ImageOps.autocontrast(img.convert("RGB")))
        self._set_estado("Autocontraste aplicado")

    def _extraer_canal(self, canal):
        idx = {"R": 0, "G": 1, "B": 2}[canal]
        def _ext(img):
            canales = list(img.convert("RGB").split())
            for i in range(3):
                if i != idx:
                    canales[i] = canales[i].point(lambda x: 0)
            return Image.merge("RGB", canales)
        self._aplicar(_ext)
        self._set_estado(f"Canal {canal} extraído")

    # ── Filtros ────────────────────────────────────────────────────────────────
    def aplicar_filtro(self):
        sel = self.lista_filtros.curselection()
        if not sel:
            return
        nombre = list(FILTROS.keys())[sel[0]]
        self._aplicar(lambda img: img.filter(FILTROS[nombre]))
        self._set_estado(f"Filtro aplicado: {nombre}")

    def agregar_marca_agua(self):
        if not self.imagen_actual:
            return
        dlg = tk.Toplevel(self)
        dlg.title("Agregar marca de agua")
        dlg.configure(bg="#1e1e2e")
        dlg.grab_set()

        ttk.Label(dlg, text="Texto de la marca:").pack(padx=16, pady=(12, 2), anchor="w")
        var_txt = tk.StringVar(value="© PixForge")
        ttk.Entry(dlg, textvariable=var_txt, width=30).pack(padx=16)

        ttk.Label(dlg, text="Opacidad (0–255):").pack(padx=16, pady=(8, 2), anchor="w")
        var_op = tk.IntVar(value=80)
        ttk.Scale(dlg, from_=0, to=255, variable=var_op,
                  orient="horizontal", length=250).pack(padx=16)

        def _aplicar():
            txt = var_txt.get()
            op  = var_op.get()

            def _dibujar(img):
                out  = img.convert("RGBA")
                capa = Image.new("RGBA", out.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(capa)
                try:
                    fuente = ImageFont.truetype(
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                        max(20, out.width // 20))
                except Exception:
                    fuente = ImageFont.load_default()
                bb = draw.textbbox((0, 0), txt, font=fuente)
                tw, th = bb[2] - bb[0], bb[3] - bb[1]
                draw.text((out.width - tw - 20, out.height - th - 20),
                          txt, font=fuente, fill=(255, 255, 255, op))
                return Image.alpha_composite(out, capa).convert(img.mode)

            self._aplicar(_dibujar)
            dlg.destroy()

        ttk.Button(dlg, text="Aplicar", style="Acento.TButton",
                   command=_aplicar).pack(padx=16, pady=12, fill="x")

    def agregar_borde(self):
        if not self.imagen_actual:
            return
        color = colorchooser.askcolor(title="Elige el color del borde",
                                      initialcolor="#000000")
        if not color[1]:
            return
        tam = 10
        self._aplicar(lambda img: ImageOps.expand(img, border=tam, fill=color[1]))
        self._set_estado(f"Borde agregado ({tam}px, {color[1]})")

    # ── Generar miniatura / Lotes ──────────────────────────────────────────────
    def generar_miniatura(self):
        if not self.imagen_actual:
            return
        try:
            tam = int(self.entrada_miniatura.get())
        except ValueError:
            messagebox.showwarning("Valor inválido", "Ingresa un tamaño válido en píxeles.")
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("WebP", "*.webp")],
            title="Guardar miniatura como…",
        )
        if not ruta:
            return
        img = self.imagen_actual.copy()
        img.thumbnail((tam, tam), Image.Resampling.LANCZOS)
        img.save(ruta)
        self._set_estado(
            f"Miniatura guardada: {Path(ruta).name}  ({img.size[0]}×{img.size[1]} px)")

    def convertir_lote(self):
        carpeta = filedialog.askdirectory(title="Selecciona carpeta con imágenes")
        if not carpeta:
            return
        destino = filedialog.askdirectory(title="Selecciona carpeta de destino")
        if not destino:
            return
        fmt = self.var_formato.get()
        ext = fmt.lower().replace("jpeg", "jpg")
        archivos = [p for p in Path(carpeta).iterdir()
                    if p.suffix.lower() in
                    {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".tif", ".webp"}]
        if not archivos:
            messagebox.showinfo("Lotes", "No se encontraron imágenes en la carpeta seleccionada.")
            return

        self.progreso["maximum"] = len(archivos)
        self.progreso["value"]   = 0
        ok, errores = 0, []
        for i, arch in enumerate(archivos, 1):
            try:
                img = Image.open(arch)
                if fmt == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                kwargs = ({"quality": self.jpeg_calidad.get(),
                           "optimize": self.jpeg_optimizar.get()}
                          if fmt == "JPEG" else {})
                img.save(Path(destino) / (arch.stem + f".{ext}"), format=fmt, **kwargs)
                ok += 1
            except Exception as e:
                errores.append(f"{arch.name}: {e}")
            self.progreso["value"] = i
            self.update_idletasks()

        self.progreso["value"] = 0
        msg = f"Convertidas {ok}/{len(archivos)} imágenes a {fmt}."
        if errores:
            msg += "\n\nErrores:\n" + "\n".join(errores[:10])
        messagebox.showinfo("Conversión completada", msg)
        self._set_estado(f"Lotes: {ok} imagen(es) convertida(s) a {fmt}")

    def _al_cambiar_formato(self, _=None):
        self.marco_jpeg.pack_forget()
        self.marco_png.pack_forget()
        fmt = self.var_formato.get()
        if fmt == "JPEG":
            self.marco_jpeg.pack(fill="x", pady=4)
        elif fmt == "PNG":
            self.marco_png.pack(fill="x", pady=4)

    # ── Panel de información ───────────────────────────────────────────────────
    def actualizar_info(self):
        self.texto_info.config(state="normal")
        self.texto_info.delete("1.0", "end")
        if not self.imagen_actual:
            self.texto_info.insert("end", "No hay imagen cargada.")
        else:
            img = self.imagen_actual
            info = (
                f"Archivo:    {Path(self.ruta_archivo).name if self.ruta_archivo else 'Sin guardar'}\n"
                f"Ruta:       {self.ruta_archivo or '—'}\n"
                f"Modo:       {img.mode}\n"
                f"Tamaño:     {img.width} × {img.height} px\n"
                f"Formato:    {img.format or 'Modificado'}\n"
                f"Historial:  {len(self.historial)} pasos (índice {self.indice_historial})\n"
                f"Zoom:       {int(self.nivel_zoom * 100)}%\n"
            )
            if hasattr(img, "_getexif") and img._getexif():
                info += "\nDatos EXIF presentes."
            try:
                rng = img.convert("L").getextrema()
                info += f"\nRango de grises: {rng[0]} – {rng[1]}"
            except Exception:
                pass
            self.texto_info.insert("end", info)
        self.texto_info.config(state="disabled")

    # ── Misc ───────────────────────────────────────────────────────────────────
    def _set_estado(self, msg: str):
        self.var_estado.set(msg)

    def _mostrar_acerca(self):
        messagebox.showinfo(
            "Acerca de PixForge",
            "PixForge v1.0.0\n\n"
            "Herramienta avanzada de procesamiento de imágenes\n"
            "construida con Python · Pillow · Tkinter\n\n"
            "Funciones: convertir, redimensionar, recortar,\n"
            "rotar, filtros, ajustes de color,\n"
            "marca de agua y conversión por lotes.\n\n"
            "Licencia MIT — github.com/tuusuario/pixforge",
        )

    def _enlazar_atajos(self):
        self.bind("<Control-a>", lambda _: self.abrir_imagen())
        self.bind("<Control-g>", lambda _: self.guardar_imagen())
        self.bind("<Control-G>", lambda _: self.guardar_como())
        self.bind("<Control-z>", lambda _: self.deshacer())
        self.bind("<Control-y>", lambda _: self.rehacer())
        self.bind("<Control-q>", lambda _: self.quit())


if __name__ == "__main__":
    app = PixForge()
    app.mainloop()
