import tkinter as tk
from vistas.login_vista import LoginVista
from vistas.menu_vista import MenuVista
class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('Sistema Veterinaria'); self.geometry('1100x650'); self.login()
    def limpiar(self):
        for w in self.winfo_children(): w.destroy()
    def login(self): self.limpiar(); v=LoginVista(self,self.menu); v.pack(fill='both',expand=True)
    def menu(self,usuario): self.limpiar(); v=MenuVista(self,usuario,self.login); v.pack(fill='both',expand=True)
if __name__=='__main__': Aplicacion().mainloop()
