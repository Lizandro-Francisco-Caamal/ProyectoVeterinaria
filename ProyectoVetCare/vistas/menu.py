from pathlib import Path
import tkinter as tk

import customtkinter as ctk

from vistas.paneles import (
    RegistroVista,
    CitasVista,
    HistorialVista,
    ClienteVista,
    VeterinarioVista
)


RUTA_LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo.png"


class Menu(ctk.CTkFrame):
    def __init__(self, master, usuario, salir):
        super().__init__(master)
        self.usuario = usuario
        self.actual = None
        self.imagen_logo = None

        lateral = ctk.CTkFrame(self, width=245, corner_radius=0)
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)

        self.area = ctk.CTkFrame(self, corner_radius=0)
        self.area.pack(side="right", fill="both", expand=True)

        if RUTA_LOGO.exists():
            self.imagen_logo = tk.PhotoImage(file=str(RUTA_LOGO)).subsample(8, 8)
            ctk.CTkLabel(lateral, image=self.imagen_logo, text="").pack(pady=(18, 0))

        ctk.CTkLabel(
            lateral,
            text="VetCare",
            font=ctk.CTkFont(size=27, weight="bold")
        ).pack(pady=(0, 4))

        ctk.CTkLabel(
            lateral,
            text=f'{usuario["nombre"]}\n{usuario["rol"].capitalize()}',
            justify="center",
            wraplength=210
        ).pack(pady=(0, 25))

        rol = usuario["rol"]

        if rol == "administrador":
            self.boton(lateral, "Registrar personas", lambda: self.ver(RegistroVista(self.area)))
            self.ver(RegistroVista(self.area))

        elif rol == "recepcionista":
            self.boton(lateral, "Citas", lambda: self.ver(CitasVista(self.area)))
            self.boton(lateral, "Nuevo cliente", lambda: self.ver(RegistroVista(self.area, True)))
            self.boton(lateral, "Historial y vacunas", lambda: self.ver(HistorialVista(self.area)))
            self.ver(CitasVista(self.area))

        elif rol == "veterinario":
            self.boton(
                lateral,
                "Mi agenda",
                lambda: self.ver(VeterinarioVista(self.area, usuario["referencia_id"]))
            )
            self.boton(lateral, "Historial y vacunas", lambda: self.ver(HistorialVista(self.area)))
            self.ver(VeterinarioVista(self.area, usuario["referencia_id"]))

        else:
            self.boton(
                lateral,
                "Mi portal",
                lambda: self.ver(ClienteVista(self.area, usuario["referencia_id"]))
            )
            self.ver(ClienteVista(self.area, usuario["referencia_id"]))

        ctk.CTkButton(
            lateral,
            text="Cerrar sesión",
            fg_color="#B3261E",
            hover_color="#8C1D18",
            height=42,
            command=salir
        ).pack(side="bottom", fill="x", padx=18, pady=20)

    def boton(self, parent, texto, comando):
        ctk.CTkButton(
            parent,
            text=texto,
            anchor="w",
            height=42,
            command=comando
        ).pack(fill="x", padx=18, pady=6)

    def ver(self, vista):
        if self.actual:
            self.actual.destroy()
        self.actual = vista
        vista.pack(fill="both", expand=True)
