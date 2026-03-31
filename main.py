#instalar  pip install  bcrypt

 #es similar a tkinter pero con mayor custom
 #python -m auto_py_to_exe


from customtkinter import CTk, CTkFrame, CTkEntry, CTkButton, CTkCheckBox, CTkLabel, CTkToplevel, CTkImage, CTkScrollableFrame
from PIL import Image
import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage, filedialog
import openpyxl
from openpyxl import Workbook

import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import mysql.connector
import pyodbc





# VENTANA
ventana = CTk()  
ventana.title("Emplex")
ventana.geometry("1000x600+450+120")
ventana.resizable(False, False)
ventana.config(bg="#F8F9FA")

# FRAME PRINCIPAL
frame = CTkFrame(ventana, fg_color="#F8F9FA")
frame.grid(column=0, row=0, sticky="nsew", padx=80, pady=60)

ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

frame.columnconfigure([0, 1], weight=1)
frame.rowconfigure(0, weight=1)

frame_login = CTkFrame(frame, fg_color="#F9F9F9")
frame_login.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            
# Configurar columnas y filas para centrado
frame_login.columnconfigure(0, weight=1)   # centro horizontal
frame_login.rowconfigure(5, weight=0)
frame_login.rowconfigure(6, weight=0)      

titulo = CTkLabel(frame_login, text="Iniciar Sesión",text_color="#00296F", font=("Arial", 20, "bold"))
titulo.grid(row=1, column=0, pady=(100, 10), sticky="n")





# -======== Cargar la imagen =========
img = CTkImage(
    light_image=Image.open(r"C:\Users\Elvi\phyton 1\imagenes\portada.png"),
    size=(500, 400) 
)


# FRAME DERECHA (IMAGEN)
frame_imagen = CTkFrame(frame, fg_color="#F8F9FA")
frame_imagen.grid(row=0, column=1, sticky="nsew", padx=10, pady=0)


 # --- Mostrar la imagen en el frame_imagen ---
label_img = CTkLabel(frame_imagen, image=img, text="")  
label_img.pack(expand=True)  # centra la imagen en el frame


#================================================================================ funciones de consultas ================================================================================================

def agregar_empleado_en_frame(frame_contenido, empresa_id):
    ventana.geometry("1000x600+450+120")

    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Frame del formulario
    formulario = CTkFrame(frame_contenido,fg_color="#F8F9FA", corner_radius=10)
    formulario.pack(pady=70, padx=30, fill="both", expand=False)

    CTkLabel(formulario, text="Agregar Empleado",text_color="#0A0A0A", font=("sans serif", 22, "bold")).grid(row=0, column=0, columnspan=2, pady=(20, 10))

    # Espaciado de columnas
    formulario.grid_columnconfigure(0, weight=1, uniform="a")
    formulario.grid_columnconfigure(1, weight=1, uniform="a")

    # Función para crear campos 1
    
    def campo(label_text, row, column):
        CTkLabel(formulario, text=label_text,text_color="#0A0A0A").grid(row=row, column=column, sticky="w", padx=14, pady=(10, 2))
        entry = CTkEntry(formulario, border_color="#0D6EFD",text_color="#0A0A0A",fg_color="#FFFFFF",)
        entry.grid(row=row + 1, column=column, padx=14, sticky="ew")
        return entry

    # Campos en dos columnas
    entry_nombre = campo("Nombre:", 1, 0)
    entry_apellido = campo("Apellido:", 1, 1)
    entry_correo = campo("Correo:", 3, 0)
    entry_telefono = campo("Teléfono:", 3, 1)
    entry_puesto = campo("Puesto:", 5, 0)
    entry_salario = campo("Salario:", 5, 1)
    entry_metodo_pago = campo("Método de Pago:", 7, 1)
    entry_fecha_registro = campo("Fecha Registro:(01/03/2025)", 7, 0)

    def guardar():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()
        puesto = entry_puesto.get()
        salario = entry_salario.get()
        metodo_pago = entry_metodo_pago.get()
        fecha_registro = entry_fecha_registro.get()

        if not nombre or not apellido or not correo or not telefono or not puesto or not salario or not metodo_pago or not fecha_registro:
            messagebox.showwarning("Campos vacíos", "Por favor, llena todos los campos obligatorios.")
            return

        try:
            conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost\\SQLEXPRESS;'
                'DATABASE=Emplex;'
                'Trusted_Connection=yes;'
            )
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO empleado (empresa_id, nombre, apellido, correo, telefono, puesto, salario,metodo_pago, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
            """, (empresa_id, nombre, apellido, correo, telefono, puesto, float(salario), metodo_pago, fecha_registro))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Empleado agregado correctamente.")

            # Limpiar campos 
            for entry in [entry_nombre, entry_apellido, entry_correo, entry_telefono, entry_puesto, entry_salario, entry_metodo_pago, entry_fecha_registro]:
                entry.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el empleado: {e}")

    # Botón Guardar centrado en ambas columnas
    CTkButton(formulario, text="Guardar", command=guardar, border_color="#0D6EFD",
    fg_color="#2478DE",
    hover_color="#cddaf6",
     text_color="#FFFFFF",)\
        .grid(row=9, column=0, columnspan=2, pady=25)


def actualizar_empleado(empleado_id, nombre, apellido, correo, telefono, puesto, salario, metodo_pago):
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=Emplex;'
            'Trusted_Connection=yes;'
        )
        cursor = conexion.cursor()
        query = """
        UPDATE empleado
        SET nombre = ?, apellido = ?, correo = ?, telefono = ?, puesto = ?, salario = ?, metodo_pago = ?
        WHERE id = ?
        """
        cursor.execute(query, (nombre, apellido, correo, telefono, puesto, salario, metodo_pago, empleado_id))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al actualizar empleado:", e)
        return False
    finally:
        if 'conexion' in locals():
            conexion.close()


def abrir_ventana_actualizacion(emp):
    ventana = CTkToplevel()
    ventana.title(f"Actualizar Empleado ID {emp['id']}")

    entradas = {}
    campos = ["nombre", "apellido", "correo", "telefono", "puesto", "salario", "metodo_pago"]
    for i, campo in enumerate(campos):
        CTkLabel(ventana, text=campo.capitalize()).grid(row=i, column=0, padx=5, pady=5)
        entry = CTkEntry(ventana)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entry.insert(0, emp[campo])
        entradas[campo] = entry

    def guardar_cambios():
        try:
            exito = actualizar_empleado(
                emp['id'],
                entradas["nombre"].get(),
                entradas["apellido"].get(),
                entradas["correo"].get(),
                entradas["telefono"].get(),
                entradas["puesto"].get(),
                float(entradas["salario"].get()),
                entradas["metodo_pago"].get()
            )
            if exito:
                CTkLabel(ventana, text="Empleado actualizado con éxito.").grid(row=len(campos), column=0, columnspan=2)
                ventana.after(1500, ventana.destroy)
            else:
                CTkLabel(ventana, text="Error al actualizar empleado.").grid(row=len(campos), column=0, columnspan=2)
        except Exception as e:
            CTkLabel(ventana, text=f"Error: {e}").grid(row=len(campos), column=0, columnspan=2)

    CTkButton(ventana, text="Guardar cambios", command=guardar_cambios).grid(row=len(campos)+1, column=0, columnspan=2, pady=10)



def buscar_empleado_en_frame(frame_contenido, empresa_id):
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=Emplex;'
            'Trusted_Connection=yes;'
        )
        cursor = conexion.cursor()
        query = """
        SELECT id, nombre, apellido, correo, telefono, puesto, salario, metodo_pago, fecha_registro
        FROM empleado WHERE empresa_id = ?
        """
        cursor.execute(query, (empresa_id,))
        empleados = cursor.fetchall()

        if empleados:
            # --- Frame de tabla ---
            tabla_frame = CTkFrame(frame_contenido)
            tabla_frame.pack(fill="both", expand=True, padx=2, pady=10)

            # Scrollbars
            scroll_y = tk.Scrollbar(tabla_frame, orient="vertical")
            scroll_y.pack(side="right", fill="y")
            scroll_x = tk.Scrollbar(tabla_frame, orient="horizontal")
            scroll_x.pack(side="bottom", fill="x")

            # Columnas
            columnas = ("ID", "Nombre", "Apellido", "Correo", "Teléfono", "Puesto", "Salario", "Método de pago", "Fecha registro")

            tabla = ttk.Treeview(
                tabla_frame,
                columns=columnas,
                show="headings",
                yscrollcommand=scroll_y.set,
                xscrollcommand=scroll_x.set
            )
            scroll_y.config(command=tabla.yview)
            scroll_x.config(command=tabla.xview)

            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=120, anchor="w")

            # Insertar datos
            for emp in empleados:
                tabla.insert("", "end", values=(
                    emp.id, emp.nombre, emp.apellido, emp.correo,
                    emp.telefono, emp.puesto, emp.salario,
                    emp.metodo_pago, emp.fecha_registro
                ))

            tabla.pack(fill="both", expand=True)

            # --- Botón para actualizar empleado seleccionado ---
            def actualizar_seleccionado():
                seleccion = tabla.selection()
                if seleccion:
                    valores = tabla.item(seleccion[0], "values")
                    empleado_dict = {
                        "id": valores[0],
                        "nombre": valores[1],
                        "apellido": valores[2],
                        "correo": valores[3],
                        "telefono": valores[4],
                        "puesto": valores[5],
                        "salario": valores[6],
                        "metodo_pago": valores[7],
                        "fecha_registro": valores[8],
                    }
                    abrir_ventana_actualizacion(empleado_dict)  # <- tu función de edición
                else:
                    messagebox.showwarning("Advertencia", "⚠️ Seleccione un empleado primero")

            btn_actualizar = CTkButton(frame_contenido, fg_color="#1170DD", text="Actualizar seleccionado", command=actualizar_seleccionado)
            btn_actualizar.pack(pady=10)

# Employee CRUD functionality

            # --- Botón para exportar a Excel ---
            def exportar_excel():
                archivo = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    title="Guardar como"
                )
                if archivo:
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Empleados"

                    # Escribir encabezados
                    ws.append(columnas)

                    # Escribir filas de empleados 
                    for emp in empleados:
                        ws.append(list(emp))

                    # Opcional: agregar total de salarios al final
                    total_salarios = sum([emp.salario for emp in empleados])
                    ws.append([])  # fila vacía
                    ws.append(["", "", "", "", "", "Total salarios:", total_salarios])

                    wb.save(archivo)
                    messagebox.showinfo("Éxito", f"Empleados exportados a {archivo}")

            btn_excel = CTkButton(frame_contenido, text="📊 Exportar a Excel", fg_color="#28A745", command=exportar_excel)
            btn_excel.pack(pady=10)

        else:
            CTkLabel(frame_contenido,text_color="#212529",text="No se encontraron empleados.").pack(pady=5)

    except Exception as e:
        CTkLabel(frame_contenido, text=f"Error: {e}").pack(pady=5)
    finally:
        if 'conexion' in locals():
            conexion.close()

# mejora en CRUD de empleados
print("CRUD de empleados optimizado")

def eliminar_empleado_en_frame(frame_contenido, empresa_id):
    ventana.geometry("1000x600+450+120")
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    formulario = CTkFrame(frame_contenido, fg_color="#F8F9FA", corner_radius=10)
    formulario.pack(pady=20, padx=30, fill="both", expand=False)

    CTkLabel(formulario, text_color="#000000", text="Despedir Empleado", font=("sans serif", 22, "bold"))\
        .grid(row=0, column=0, columnspan=2, pady=(20, 10))

    CTkLabel(formulario, text="ID del Empleado:", text_color="#000000").grid(row=1, column=0, sticky="w", padx=14, pady=(10, 2))
    entry_id = CTkEntry(formulario, text_color="#000000", border_color="#0D6EFD", fg_color="#FFFFFF")
    entry_id.grid(row=2, column=0, padx=14, sticky="ew")

    def despedir():
        empleado_id = entry_id.get()
        if not empleado_id:
            messagebox.showwarning("Campo vacío", "Ingresa el ID del empleado.")
            return

        try:
            conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost\\SQLEXPRESS;'
                'DATABASE=Emplex;'
                'Trusted_Connection=yes;'
            )
            cursor = conexion.cursor()

            # Obtener id_empresa del empleado
            cursor.execute("SELECT empresa_id FROM empleado WHERE id = ?", empleado_id)
            resultado = cursor.fetchone()
            if resultado is None:
                messagebox.showwarning("Advertencia", "Empleado no encontrado.")
                return

            id_empresa_empleado = resultado[0]

            # Verificar que el empleado pertenece a la misma empresa que el usuario
            if id_empresa_empleado != empresa_id:
                messagebox.showerror("Error", "Empleado no encontrado.")
                return

            # Eliminar empleado
            cursor.execute("DELETE FROM empleado WHERE id = ?", empleado_id)
            conexion.commit()
            messagebox.showinfo("Éxito", f"Empleado con ID {empleado_id} despedido correctamente.")
            entry_id.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo despedir el empleado.\n{e}")
        finally:
            cursor.close()
            conexion.close()

    CTkButton(formulario, text="Eliminar", command=despedir, fg_color="#e74c3c")\
        .grid(row=3, column=0, pady=25)



def calcular_total_pagos(frame_contenido, empresa_id):
    # Limpiar frame antes de mostrar resultado
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    try:
        # Conectar a SQL Server
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=Emplex;'
            'Trusted_Connection=yes;'
        )
        cursor = conexion.cursor()
        
        # Consulta SQL para sumar salarios por empresa
        cursor.execute("""
            SELECT ISNULL(SUM(salario), 0)
            FROM empleado
            WHERE empresa_id = ?
        """, (empresa_id,))
        
        total = cursor.fetchone()[0]  # Obtiene el total
        
        conexion.close()

        # Mostrar el resultado en la interfaz
        CTkLabel(frame_contenido, 
                 text=f"💰 Total a pagar a empleados: {total}", 
                 font=("sans serif", 20, "bold"),
                 text_color="#0A0A0A").pack(pady=50)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo calcular el total: {e}")


#================================================================================ funciones login y registro ================================================================================================

#def cambiar_contrasena_empresa(frame_login):

# User authentication module
#funcion de inicio
def mostrar_sesion():
    email = correo.get()
    clave = contraseña.get()

    if not email or not clave:
        messagebox.showwarning("Campos vacíos", "Por favor, completa los campos")
        return

    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=Emplex;'
            'Trusted_Connection=yes;'
        )
        cursor = conexion.cursor()
        consulta = "SELECT * FROM empresas WHERE correo = ? AND contrasena = ?"
        cursor.execute(consulta, (email, clave))
        resultado = cursor.fetchone()

        if resultado:
            empresa_id = resultado[0]

            # Oculta el login y ajusta la ventana
            frame.grid_forget()
            ventana.geometry("1000x600+450+120")

            # Configurar columnas y filas de la ventana
            ventana.grid_rowconfigure(0, weight=1)      # La fila 0 ocupa todo el alto
            ventana.grid_columnconfigure(0, weight=0)   # Columna del menú, fija
            ventana.grid_columnconfigure(1, weight=1)   



            # Frame izquierdo: menú lateral
            frame_botonera = CTkFrame(ventana, fg_color="#E0E9F4", width=200)
            frame_botonera.grid(row=0, column=0, sticky="nsw", padx=0, pady=0)



            # Frame derecho: contenido 
            frame_contenido = CTkFrame(ventana, fg_color="#FFFFFF")
            frame_contenido.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)




            # Función para mostrar mensaje de bienvenida
            def mostrar_bienvenida():
                for widget in frame_contenido.winfo_children():
                    widget.destroy()

                texto_bienvenida = """\

                    Administre la información de sus colaboradores de manera rápida y eficiente.

                    Funciones principales:
                    
                   •Agregar y registrar nuevos empleados.
                   •Consultar y actualizar información existente.
                   •Gestionar bajas o modificaciones de empleados.
                   •Mantener la base de datos siempre actualizada.

                   Seleccione una opción en el menú para comenzar."""
                
                mensaje_titulo = CTkLabel(frame_contenido,text="Bienvenido a Emplex",font=("inter", 32),text_color="#208ACD",justify="left")
                mensaje_titulo.pack(padx=20, pady=20, anchor="w")

                
                mensaje_bienvenida = CTkLabel(frame_contenido,text=texto_bienvenida,font=("inter", 18),text_color="#2A87D4",justify="left")
                mensaje_bienvenida.pack(padx=0, pady=20, anchor="w")

                 

            # Botones del menú lateral
            btn_inicio = CTkButton(frame_botonera, text="Inicio", command=mostrar_bienvenida,fg_color="#0D73C0" , width=120)
            btn_inicio.pack(pady=10, fill="x", padx=10)


            btn_agregar = CTkButton(frame_botonera, text="Agregar Empleado",command=lambda: agregar_empleado_en_frame(frame_contenido, empresa_id),
            fg_color="#0D73C0" , width=180)
            btn_agregar.pack(pady=10, fill="x", padx=10)


            btn_buscar = CTkButton(frame_botonera, text="Buscar Empleados",command=lambda: buscar_empleado_en_frame(frame_contenido, empresa_id),
            fg_color="#0D73C0" , width=180)
            btn_buscar.pack(pady=10, fill="x", padx=10)
            

            btn_eliminar = CTkButton(frame_botonera, text="Eliminar Empleado",command=lambda: eliminar_empleado_en_frame(frame_contenido,empresa_id),
            fg_color="#0D73C0" , width=180)
            btn_eliminar.pack(pady=10, fill="x", padx=10)

            btn_total = CTkButton(frame_botonera, text="Calcular Total a Pagar",command=lambda: calcular_total_pagos(frame_contenido, empresa_id),fg_color="#2478DE",      # Azul principal
                                  hover_color="#0D6EFD",   # Azul más intenso al pasar el mouse
                                  text_color="#FFFFFF",    # Texto blanco
                                  width=180)
            btn_total.pack(pady=10, fill="x", padx=10)


 



            # Botón de cerrar sesión abajo
            btn_atras = CTkButton(frame_botonera, text="Cerrar Sesión", font=('sans serif', 12),
                                  fg_color="#1c5ce7", hover_color="#1386c0",
                                  text_color="#FFFFFF",
                                  border_color="#1c5ce7", border_width=2,
                                  corner_radius=10, width=180,
                                  command=volver_inicio)
            btn_atras.pack(side="bottom", pady=20, padx=10)

            # Mostrar bienvenida inicial
            mostrar_bienvenida()

        else:
            messagebox.showerror("Error", "Contraseña o correo incorrecto")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


#funcion de registro
def mostrar_registro():

    global entry_empresa, entry_direccion, entry_correo, entry_contrasena
    frame.grid_forget()
    ventana.geometry("1000x600+450+120")
    frame_registro = CTkFrame(ventana, fg_color="#F8F9FA")
    frame_registro.grid(column=0, row=0, sticky="nsew", padx=50, pady=0)

    # Título del formulario
    etiqueta_registro = CTkLabel(
        frame_registro,
        text="Formulario de Registro",
        font=("sans serif", 18, "bold"),
        text_color="#00296F"
    )
    etiqueta_registro.pack(pady=10)

    # Nombre del negocio o empresa
    entry_empresa = CTkEntry(
        frame_registro,
        placeholder_text="Nombre del negocio o empresa",
        font=('sans serif', 12),
        border_color="#0D6EFD",
        text_color="#0A0A0A",
        fg_color="#FFFFFF",
        width=300,
        height=40
    )
    entry_empresa.pack(pady=6)

    #  direccio del negocio o empresa
    entry_direccion = CTkEntry(
        frame_registro,
        placeholder_text="Dirección de la empresa",
        font=('sans serif', 12),
        border_color="#0D6EFD",
        text_color="#0A0A0A",
        fg_color='#FFFFFF',
        width=300,
        height=40
    )
    entry_direccion.pack(pady=6)

    # Campo: Correo electrónico
    entry_correo = CTkEntry(
        frame_registro,
        placeholder_text="Correo electrónico",
        font=('sans serif', 12),
        border_color="#0D6EFD",
        text_color="#0A0A0A",
        fg_color='#FFFFFF',
        width=300,
        height=40
    )
    entry_correo.pack(pady=6)

    # Campo: Contraseña
    entry_contrasena = CTkEntry(
        frame_registro,
        placeholder_text="Contraseña",
        show="*",
        font=('sans serif', 12),
        text_color="#0A0A0A",
        border_color="#0D6EFD",
        fg_color='#FFFFFF',
        width=300,
        height=40
    )
    entry_contrasena.pack(pady=6)
    
    # Botón para registrar
    btn_guardar = CTkButton(
        frame_registro,
        text="Registrar Empresa",
        font=('sans serif', 12),
        fg_color='#FFFFFF',
        hover_color="#1d94d4",
        text_color="#0A0A0A",
        border_color='#0D6EFD',
        border_width=2,
        corner_radius=10,
        width=200,
        command= registrar_en_mysql
    )
    btn_guardar.pack(pady=15)
    etiqueta_registro.pack(pady=50)
    




	 # Botón para vorver al inicio
    btn_atras = CTkButton(
      frame_registro,  # ← Aquí debe ir el frame correcto, no 'frame_atras'
       text="Volver al inicio",
       font=('sans serif', 12),
       fg_color='#FFFFFF',
       hover_color="#3180d0",
       text_color="#000000",
       border_color='#0D6EFD',
       border_width=2,
       corner_radius=10,
       width=200,
       command=volver_inicio
)
    btn_atras.pack(pady=2)
    



def registrar_en_mysql(): 
    nombre = entry_empresa.get()
    direccion = entry_direccion.get()
    correo = entry_correo.get()
    contrasena = entry_contrasena.get()
    
    if not nombre or not direccion or not correo or not contrasena:
        messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
        return

    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=Emplex;'
            'Trusted_Connection=yes;'
        )

        cursor = conexion.cursor()

        consulta = "INSERT INTO empresas (nombre, direccion, correo, contrasena) VALUES (?, ?, ?, ?)"
        valores = (nombre, direccion, correo, contrasena)

        cursor.execute(consulta, valores)
        conexion.commit()

        messagebox.showinfo("Éxito", "Empresa registrada correctamente")

    except pyodbc.Error as error:  # Aquí se usa correctamente pyodbc.Error
        messagebox.showerror("Error", f"No se pudo registrar: {error}")

    finally:
        conexion.close()


# volver inicio
def volver_inicio():
    # Borra el frame actual 
    for widget in ventana.winfo_children():
        widget.grid_forget()

    # frame principal 
    frame.grid(row=0, column=0, sticky="nsew", padx=80, pady=70)


# -----------------------------
# Diccionario global para OTP
codigos_otp = {}



# -----------------------------
# Función para enviar código OTP por correo
def enviar_codigo(correo, codigo):
    remitente = "elviperezfrias01cash@gmail.com"
    password = "frzuqtkbdwouytgw"  # contraseña de app de Gmail
    asunto = "Código de Restablecimiento de Contraseña"

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = correo
    mensaje['Subject'] = Header(asunto, 'utf-8')

    cuerpo = f"Tu código de restablecimiento es: {codigo}"
    mensaje.attach(MIMEText(cuerpo, 'plain', 'utf-8'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.send_message(mensaje)
        servidor.quit()
        print("Correo enviado correctamente.")
    except Exception as e:
        print("Error al enviar correo:", e)
        messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")


# -----------------------------
# Función principal para restablecer contraseña
def restablecer_contraseña():
    ventana_rest = CTkToplevel()
    ventana_rest.title("Restablecer Contraseña")
    ventana_rest.geometry("250x400")

    CTkLabel(ventana_rest, text="Correo:").pack(pady=(20,5))
    entrada_correo = CTkEntry(ventana_rest)
    entrada_correo.pack(pady=5)

    # Enviar OTP
    def enviar_otp():
        correo = entrada_correo.get().strip()
        if correo == "":
            messagebox.showwarning("Advertencia", "Ingresa un correo válido")
            return
        codigo = str(random.randint(100000, 999999))
        codigos_otp[correo] = codigo
        enviar_codigo(correo, codigo)
        mostrar_campo_codigo()

    # Mostrar campos para OTP y nueva contraseña
    def mostrar_campo_codigo():
        CTkLabel(ventana_rest, text="Código recibido:").pack(pady=5)
        entrada_codigo = CTkEntry(ventana_rest)
        entrada_codigo.pack(pady=5)

        CTkLabel(ventana_rest, text="Nueva contraseña:").pack(pady=5)
        entrada_nueva = CTkEntry(ventana_rest, show="*")
        entrada_nueva.pack(pady=5)

        def confirmar():
            correo = entrada_correo.get().strip()
            codigo_ingresado = entrada_codigo.get().strip()
            nueva = entrada_nueva.get().strip()

            if codigos_otp.get(correo) == codigo_ingresado:
                try:
                    # Conectar a SQL Server
                    conexion = pyodbc.connect(
                        'DRIVER={ODBC Driver 17 for SQL Server};'
                        'SERVER=localhost\\SQLEXPRESS;'
                        'DATABASE=Emplex;'
                        'Trusted_Connection=yes;'
                    )
                    cursor = conexion.cursor()

                    # Guardar contraseña directamente SIN encriptar
                    sql = "UPDATE dbo.empresas SET contrasena=? WHERE correo=?"
                    cursor.execute(sql, (nueva, correo))
                    conexion.commit()

                    messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.")
                    print(f"Contraseña de {correo} actualizada en la base de datos.")

                except pyodbc.Error as err:
                    print("Error al actualizar la contraseña:", err)
                    messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {err}")

                finally:
                    cursor.close()
                    conexion.close()

                # Eliminar OTP
                del codigos_otp[correo]
                ventana_rest.destroy()
            else:
                messagebox.showerror("Error", "Código incorrecto. Intenta de nuevo.")
                print("Código incorrecto.")

        CTkButton(ventana_rest, text="Confirmar", command=confirmar).pack(pady=10)

    CTkButton(ventana_rest, text="Enviar código", command=enviar_otp).pack(pady=10)

#=============================================================================================================================================================================

# ENTRY CORREO
correo = CTkEntry(
    frame_login,
    font=('sans serif', 12),
    placeholder_text='Correo electrónico',
    placeholder_text_color="#6C757D",
    border_color="#0D6EFD",
    fg_color="#FFFFFF",
    text_color="#212529",
    width=220,
    height=40
)
correo.grid(row=2, column=0, pady=5, padx=20, sticky="ew")

# ENTRY CONTRASEÑA
contraseña = CTkEntry(
    frame_login,
    show="*",
    font=('sans serif', 12),
    placeholder_text='Contraseña',
    placeholder_text_color="#6C757D",
    text_color="#000000",
    border_color="#0D6EFD",
    fg_color="#FFFFFF",
    width=220,
    height=40
)
contraseña.grid(row=3, column=0, pady=5, padx=20, sticky="ew")


# CHECKBOX
checkbox = CTkCheckBox(
    frame_login,
    text="Recordarme",
    hover_color="#b2c6e9",
    border_color="#1F87E1",
    text_color="#212529",
    fg_color="#3c5df0"
)
checkbox.grid(row=4, column=0, pady=5)

# BOTÓN 1
bt_iniciar = CTkButton(
    frame_login,
    font=('sans serif', 12),
    border_color="#0D6EFD",
    fg_color="#FFFFFF",
    hover_color="#cddaf6",
     text_color="#054CFF",
    corner_radius=12,
    border_width=2,
    text='Iniciar Sesion',
    command=mostrar_sesion
)
bt_iniciar.grid(row=5, column=0, pady=(5, 2))

# BOTÓN 2
bt_regist = CTkButton(
    frame_login,
    font=('sans serif', 12),
    border_color="#0D6EFD",
    fg_color="#FFFFFF",
    hover_color="#b8cbf3",
     text_color="#054CFF",
    corner_radius=12,
    border_width=2,
    text='Registrarse',
    command=mostrar_registro
)
bt_regist.grid(row=6, column=0,pady=(2, 5))

# -----------------------------
# Botón para restablecer contraseña (debajo del botón de registro)
# -----------------------------
bt_restablecer_pass = CTkButton(
    frame_login,  
    font=('sans serif', 11),   # fuente un poco más chica
    width=140,                 # ancho del botón
    height=28,                 # alto del botón
    border_color="#0D6EFD",
    fg_color="#FFFFFF",
    hover_color="#b8cbf3",
    text_color="#054CFF",
    corner_radius=12,
    border_width=2,
    text='Restablecer Contraseña',
    command=restablecer_contraseña
)
bt_restablecer_pass.grid(row=7, column=0, pady=(2, 5))






ventana.mainloop()

