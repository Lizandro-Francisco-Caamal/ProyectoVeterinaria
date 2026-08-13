from pathlib import Path
import tkinter as tk

import customtkinter as ctk

from vistas.login import LoginVista
from vistas.menu import Menu


RUTA_LOGO = Path(__file__).resolve().parent / "assets" / "logo.png"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.title("VetCare - Sistema Veterinario")
        self.geometry("1280x760")
        self.minsize(1100, 680)

        self.icono_ventana = None
        self.configurar_icono()
        self.login()

    def configurar_icono(self):
        if RUTA_LOGO.exists():
            self.icono_ventana = tk.PhotoImage(file=str(RUTA_LOGO))
            self.iconphoto(True, self.icono_ventana)

    def limpiar(self):
        for widget in self.winfo_children():
            widget.destroy()

    def login(self):
        self.limpiar()
        LoginVista(self, self.menu).pack(fill="both", expand=True)

    def menu(self, usuario):
        self.limpiar()
        Menu(self, usuario, self.login).pack(fill="both", expand=True)


if __name__ == "__main__":
    App().mainloop()
