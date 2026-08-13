from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import threading

import customtkinter as ctk

from repositorios.sistema_repositorio import SistemaRepositorio


RUTA_LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo.png"


class LoginVista(ctk.CTkFrame):
    def __init__(self, master, ingresar):
        super().__init__(master)

        self.repo = SistemaRepositorio()
        self.ingresar = ingresar
        self.imagen_logo = None
        self.iniciando_sesion = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            self,
            corner_radius=50
        )
        card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=350,
            pady=40
        )

        contenido = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        contenido.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        if RUTA_LOGO.exists():
            self.imagen_logo = tk.PhotoImage(
                file=str(RUTA_LOGO)
            ).subsample(4, 4)

            ctk.CTkLabel(
                contenido,
                image=self.imagen_logo,
                text=""
            ).pack(pady=(15, 15))

        ctk.CTkLabel(
            contenido,
            text="Bienvenido a VetCare",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(pady=(5, 25))

        self.usuario = ctk.CTkEntry(
            contenido,
            width=520,
            height=48,
            placeholder_text="Usuario"
        )
        self.usuario.pack(pady=10)

        self.password = ctk.CTkEntry(
            contenido,
            width=520,
            height=48,
            placeholder_text="Contraseña",
            show="•"
        )
        self.password.pack(pady=10)

        self.password.bind(
            "<Return>",
            lambda _event: self.validar()
        )

        self.mostrar_password = ctk.CTkCheckBox(
            contenido,
            text="Mostrar contraseña",
            command=self.cambiar_visibilidad
        )
        self.mostrar_password.pack(pady=(12, 8))

        self.estado = ctk.CTkLabel(
            contenido,
            text=""
        )
        self.estado.pack(pady=(4, 0))

        self.boton_login = ctk.CTkButton(
            contenido,
            text="Iniciar sesión",
            width=520,
            height=48,
            command=self.validar
        )
        self.boton_login.pack(pady=20)

        self.usuario.focus_set()

    def cambiar_visibilidad(self):
        self.password.configure(
            show="" if self.mostrar_password.get() else "•"
        )

    def validar(self):
        if self.iniciando_sesion:
            return

        usuario = self.usuario.get().strip()
        password = self.password.get()

        if not usuario or not password:
            messagebox.showwarning(
                "Aviso",
                "Escribe el usuario y la contraseña."
            )
            return

        self.iniciando_sesion = True
        self.boton_login.configure(
            state="disabled",
            text="Verificando..."
        )
        self.estado.configure(
            text="Conectando con MySQL..."
        )

        hilo = threading.Thread(
            target=self._validar_en_segundo_plano,
            args=(usuario, password),
            daemon=True
        )
        hilo.start()

    def _validar_en_segundo_plano(self, usuario, password):
        try:
            dato = self.repo.login(usuario, password)
            self.after(0, self._finalizar_login, dato)
        except Exception as error:
            self.after(
                0,
                self._mostrar_error_conexion,
                str(error)
            )

    def _finalizar_login(self, dato):
        self.iniciando_sesion = False
        self.boton_login.configure(
            state="normal",
            text="Iniciar sesión"
        )
        self.estado.configure(text="")

        if dato:
            self.ingresar(dato)
        else:
            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos, o MySQL no está disponible."
            )

    def _mostrar_error_conexion(self, error):
        self.iniciando_sesion = False
        self.boton_login.configure(
            state="normal",
            text="Iniciar sesión"
        )
        self.estado.configure(text="")

        messagebox.showerror(
            "Error de conexión",
            "No se pudo conectar con MySQL.\n\n"
            "Verifica que MySQL esté iniciado en XAMPP y que exista "
            "la base de datos 'veterinaria'.\n\n"
            f"Detalle: {error}"
        )
