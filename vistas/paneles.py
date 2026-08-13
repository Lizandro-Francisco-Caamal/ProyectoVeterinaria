import customtkinter as ctk
from tkinter import ttk, messagebox
from repositorios.sistema_repositorio import SistemaRepositorio

def tabla(parent, columnas, titulos):
    t = ttk.Treeview(parent,columns=columnas,show="headings")
    for c,ti in zip(columnas,titulos):
        t.heading(c,text=ti)
        t.column(c,width=125)
    t.pack(fill="both",expand=True,padx=15,pady=15)
    return t

class RegistroVista(ctk.CTkFrame):
    def __init__(self,master,solo_clientes=False):
        super().__init__(master)
        self.repo=SistemaRepositorio()
        tabs=ctk.CTkTabview(self)
        tabs.pack(fill="both",expand=True,padx=20,pady=20)
        self.crear_cliente(tabs.add("Nuevo cliente"))
        if not solo_clientes:
            self.crear_vet(tabs.add("Nuevo veterinario"))

    def campo(self,parent,texto,fila,clave,dic,password=False):
        ctk.CTkLabel(parent,text=texto).grid(row=fila,column=0,sticky="w",padx=12,pady=8)
        e=ctk.CTkEntry(parent,width=350,show="•" if password else "")
        e.grid(row=fila,column=1,padx=12,pady=8)
        dic[clave]=e

    def crear_cliente(self,parent):
        f=ctk.CTkScrollableFrame(parent)
        f.pack(fill="both",expand=True,padx=10,pady=10)
        self.cc={}
        datos=[
            ("Nombre completo","nombre"),("Correo","correo"),("Teléfono","telefono"),
            ("Dirección","direccion"),("Mascota","mascota"),("Especie","especie"),
            ("Raza","raza"),("Nacimiento AAAA-MM-DD","fecha_nacimiento"),
            ("Peso","peso"),("Color","color"),("Usuario","usuario"),("Contraseña","password")
        ]
        for i,(t,k) in enumerate(datos): self.campo(f,t,i,k,self.cc,k=="password")
        ctk.CTkLabel(f,text="Sexo").grid(row=len(datos),column=0,sticky="w",padx=12,pady=8)
        self.sexo=ctk.CTkOptionMenu(f,values=["Macho","Hembra"])
        self.sexo.grid(row=len(datos),column=1,sticky="w",padx=12)
        ctk.CTkButton(f,text="Crear cliente, mascota y acceso",height=42,command=self.guardar_cliente).grid(
            row=len(datos)+1,column=0,columnspan=2,pady=20)

    def guardar_cliente(self):
        d={k:e.get().strip() for k,e in self.cc.items()}
        d["sexo"]=self.sexo.get()
        if any(not d[k] for k in ("nombre","correo","telefono","mascota","especie","usuario","password")):
            messagebox.showwarning("Aviso","Completa los campos obligatorios."); return
        if self.repo.usuario_existe(d["usuario"]):
            messagebox.showerror("Error","El usuario ya existe."); return
        try:
            d["peso"]=float(d["peso"]) if d["peso"] else None
        except ValueError:
            messagebox.showerror("Error","El peso debe ser numérico."); return
        if self.repo.crear_cliente_con_mascota(d):
            messagebox.showinfo("Correcto","Cliente, mascota y cuenta creados.")
            for e in self.cc.values(): e.delete(0,"end")

    def crear_vet(self,parent):
        f=ctk.CTkFrame(parent,fg_color="transparent")
        f.pack(fill="both",expand=True,padx=20,pady=20)
        self.cv={}
        datos=[("Nombre completo","nombre"),("Especialidad","especialidad"),("Correo","correo"),
               ("Teléfono","telefono"),("Usuario","usuario"),("Contraseña","password")]
        for i,(t,k) in enumerate(datos): self.campo(f,t,i,k,self.cv,k=="password")
        ctk.CTkButton(f,text="Crear veterinario y acceso",height=42,command=self.guardar_vet).grid(
            row=len(datos),column=0,columnspan=2,pady=20)

    def guardar_vet(self):
        d={k:e.get().strip() for k,e in self.cv.items()}
        if any(not d[k] for k in ("nombre","especialidad","usuario","password")):
            messagebox.showwarning("Aviso","Completa los campos obligatorios."); return
        if self.repo.usuario_existe(d["usuario"]):
            messagebox.showerror("Error","El usuario ya existe."); return
        if self.repo.crear_veterinario(d):
            messagebox.showinfo("Correcto","Veterinario y cuenta creados.")
            for e in self.cv.values(): e.delete(0,"end")

class CitasVista(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master); self.repo=SistemaRepositorio()
        self.mascotas={}; self.vets={}
        ctk.CTkLabel(self,text="Gestión de citas",font=ctk.CTkFont(size=26,weight="bold")).pack(anchor="w",padx=25,pady=18)
        f=ctk.CTkFrame(self); f.pack(fill="x",padx=20,pady=8)
        self.om=ctk.CTkOptionMenu(f,values=["Sin mascotas"]); self.om.grid(row=0,column=0,padx=8,pady=12)
        self.ov=ctk.CTkOptionMenu(f,values=["Sin veterinarios"]); self.ov.grid(row=0,column=1,padx=8,pady=12)
        self.fecha=ctk.CTkEntry(f,placeholder_text="Fecha AAAA-MM-DD"); self.fecha.grid(row=0,column=2,padx=8)
        self.hora=ctk.CTkEntry(f,placeholder_text="Hora HH:MM:SS"); self.hora.grid(row=0,column=3,padx=8)
        self.motivo=ctk.CTkEntry(f,placeholder_text="Motivo",width=260); self.motivo.grid(row=1,column=0,columnspan=2,padx=8,pady=12)
        self.info=ctk.CTkLabel(f,text="Consulta la disponibilidad."); self.info.grid(row=1,column=2,padx=8)
        ctk.CTkButton(f,text="Ver disponibilidad",command=self.disponibilidad).grid(row=1,column=3,padx=8)
        ctk.CTkButton(f,text="Crear cita",command=self.crear).grid(row=2,column=0,columnspan=4,pady=12)
        self.t=tabla(self,("id","fecha","hora","mascota","cliente","vet","motivo","estado"),
                     ("ID","Fecha","Hora","Mascota","Cliente","Veterinario","Motivo","Estado"))
        self.cargar()

    def cargar(self):
        ms=self.repo.listar_mascotas(); self.mascotas={x["descripcion"]:x["id_mascota"] for x in ms}
        self.om.configure(values=list(self.mascotas) or ["Sin mascotas"])
        vs=self.repo.listar_veterinarios()
        self.vets={f'{x["nombre"]} - {x["especialidad"]}':x["id_veterinario"] for x in vs}
        self.ov.configure(values=list(self.vets) or ["Sin veterinarios"])
        for i in self.t.get_children(): self.t.delete(i)
        for c in self.repo.citas_todas():
            self.t.insert("", "end", values=(c["id_cita"],c["fecha"],c["hora"],c["mascota"],
                c["cliente"],c["veterinario"],c["motivo"],c["estado"]))

    def disponibilidad(self):
        if self.ov.get() not in self.vets or not self.fecha.get():
            self.info.configure(text="Falta fecha o veterinario."); return
        a=self.repo.horarios_ocupados(self.vets[self.ov.get()],self.fecha.get())
        self.info.configure(text="Disponible todo el día." if not a else "Ocupado: "+", ".join(str(x["hora"]) for x in a))

    def crear(self):
        if self.om.get() not in self.mascotas or self.ov.get() not in self.vets:
            messagebox.showwarning("Aviso","Selecciona mascota y veterinario."); return
        r=self.repo.crear_cita(self.mascotas[self.om.get()],self.vets[self.ov.get()],
                               self.fecha.get(),self.hora.get(),self.motivo.get())
        if r=="ocupado": messagebox.showerror("Ocupado","El veterinario ya tiene cita en ese horario.")
        elif r: messagebox.showinfo("Correcto","Cita creada."); self.cargar(); self.disponibilidad()

class HistorialVista(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master); self.repo=SistemaRepositorio(); self.clientes={}; self.mascotas={}; self.vacunas={}
        ctk.CTkLabel(self,text="Historial y vacunas",font=ctk.CTkFont(size=26,weight="bold")).pack(anchor="w",padx=25,pady=18)
        f=ctk.CTkFrame(self); f.pack(fill="x",padx=20,pady=8)
        self.oc=ctk.CTkOptionMenu(f,values=["Sin clientes"],command=lambda _v:self.cargar_historial()); self.oc.pack(side="left",padx=8,pady=12)
        self.om=ctk.CTkOptionMenu(f,values=["Sin mascotas"]); self.om.pack(side="left",padx=8)
        self.ov=ctk.CTkOptionMenu(f,values=["Sin vacunas"]); self.ov.pack(side="left",padx=8)
        self.fa=ctk.CTkEntry(f,placeholder_text="Aplicación"); self.fa.pack(side="left",padx=8)
        self.fp=ctk.CTkEntry(f,placeholder_text="Próxima dosis"); self.fp.pack(side="left",padx=8)
        ctk.CTkButton(f,text="Registrar vacuna y alerta",command=self.registrar).pack(side="left",padx=8)
        self.t=tabla(self,("mascota","fecha","motivo","estado","diagnostico","tratamiento","vet"),
                     ("Mascota","Fecha","Motivo","Estado","Diagnóstico","Tratamiento","Veterinario"))
        cs=self.repo.listar_clientes(); self.clientes={x["nombre"]:x["id_dueno"] for x in cs}
        self.oc.configure(values=list(self.clientes) or ["Sin clientes"])
        vs=self.repo.catalogo_vacunas(); self.vacunas={x["nombre"]:x["id_vacuna"] for x in vs}
        self.ov.configure(values=list(self.vacunas) or ["Sin vacunas"])

    def cargar_historial(self):
        if self.oc.get() not in self.clientes:return
        idc=self.clientes[self.oc.get()]
        ms=self.repo.listar_mascotas_cliente(idc); self.mascotas={x["nombre"]:x["id_mascota"] for x in ms}
        self.om.configure(values=list(self.mascotas) or ["Sin mascotas"])
        for i in self.t.get_children(): self.t.delete(i)
        for h in self.repo.historial_cliente(idc):
            self.t.insert("", "end", values=(h["mascota"],h["fecha"] or "",h["motivo"] or "",h["estado"] or "",
                h["diagnostico"] or "",h["tratamiento"] or "",h["veterinario"] or ""))

    def registrar(self):
        if self.om.get() not in self.mascotas or self.ov.get() not in self.vacunas:
            messagebox.showwarning("Aviso","Selecciona mascota y vacuna."); return
        if self.repo.registrar_vacuna(self.mascotas[self.om.get()],self.vacunas[self.ov.get()],self.fa.get(),self.fp.get()):
            messagebox.showinfo("Correcto","Vacuna registrada y alerta creada para el cliente.")

class ClienteVista(ctk.CTkFrame):
    def __init__(self,master,id_cliente):
        super().__init__(master); self.repo=SistemaRepositorio(); self.id=id_cliente; self.vets={}
        tabs=ctk.CTkTabview(self); tabs.pack(fill="both",expand=True,padx=20,pady=20)
        a=tabs.add("Mis citas"); b=tabs.add("Alertas y vacunas"); c=tabs.add("Disponibilidad")
        self.t=tabla(a,("fecha","hora","mascota","vet","motivo","estado"),("Fecha","Hora","Mascota","Veterinario","Motivo","Estado"))
        self.texto=ctk.CTkTextbox(b); self.texto.pack(fill="both",expand=True,padx=12,pady=12)
        f=ctk.CTkFrame(c); f.pack(fill="x",padx=10,pady=10)
        self.ov=ctk.CTkOptionMenu(f,values=["Sin veterinarios"]); self.ov.pack(side="left",padx=8)
        self.fecha=ctk.CTkEntry(f,placeholder_text="Fecha AAAA-MM-DD"); self.fecha.pack(side="left",padx=8)
        ctk.CTkButton(f,text="Consultar",command=self.ver_disponibilidad).pack(side="left",padx=8)
        self.disp=ctk.CTkTextbox(c); self.disp.pack(fill="both",expand=True,padx=12,pady=12)
        self.cargar()

    def cargar(self):
        for x in self.repo.citas_cliente(self.id):
            self.t.insert("", "end", values=(x["fecha"],x["hora"],x["mascota"],x["veterinario"],x["motivo"],x["estado"]))
        for a in self.repo.alertas_cliente(self.id):
            self.texto.insert("end",f'{a["titulo"]}\n{a["mensaje"]}\nFecha: {a["fecha_alerta"]}\n\n')
        for v in self.repo.vacunas_proximas(self.id):
            self.texto.insert("end",f'VACUNA PRÓXIMA: {v["mascota"]} - {v["vacuna"]}\n{v["proxima_dosis"]} ({v["dias"]} días)\n\n')
        vs=self.repo.listar_veterinarios(); self.vets={f'{x["nombre"]} - {x["especialidad"]}':x["id_veterinario"] for x in vs}
        self.ov.configure(values=list(self.vets) or ["Sin veterinarios"])

    def ver_disponibilidad(self):
        self.disp.delete("1.0","end")
        if self.ov.get() not in self.vets or not self.fecha.get(): return
        a=self.repo.horarios_ocupados(self.vets[self.ov.get()],self.fecha.get())
        if not a:self.disp.insert("end","No hay citas registradas. Consulta con recepción para reservar.")
        else:
            self.disp.insert("end","HORARIOS OCUPADOS:\n\n")
            for x in a:self.disp.insert("end",f'{x["hora"]} - {x["motivo"]}\n')

class VeterinarioVista(ctk.CTkFrame):
    def __init__(self,master,id_vet):
        super().__init__(master); self.repo=SistemaRepositorio(); self.id=id_vet
        ctk.CTkLabel(self,text="Mi agenda",font=ctk.CTkFont(size=26,weight="bold")).pack(anchor="w",padx=25,pady=18)
        f=ctk.CTkFrame(self); f.pack(fill="x",padx=20)
        ctk.CTkButton(f,text="Marcar atendida",command=lambda:self.estado("Atendida")).pack(side="left",padx=8,pady=10)
        ctk.CTkButton(f,text="Cancelar",command=lambda:self.estado("Cancelada")).pack(side="left",padx=8)
        self.t=tabla(self,("id","fecha","hora","mascota","cliente","motivo","estado"),
                     ("ID","Fecha","Hora","Mascota","Cliente","Motivo","Estado")); self.cargar()

    def cargar(self):
        for i in self.t.get_children():self.t.delete(i)
        for x in self.repo.agenda_veterinario(self.id):
            self.t.insert("", "end", values=(x["id_cita"],x["fecha"],x["hora"],x["mascota"],x["cliente"],x["motivo"],x["estado"]))

    def estado(self,e):
        s=self.t.selection()
        if not s: messagebox.showwarning("Aviso","Selecciona una cita."); return
        if self.repo.cambiar_estado(self.t.item(s[0],"values")[0],e): self.cargar()
